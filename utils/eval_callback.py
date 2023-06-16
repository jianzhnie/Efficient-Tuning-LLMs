from typing import Any, Dict, List, Optional

import accuracy
import numpy as np
import torch
from tqdm.auto import tqdm
from transformers import PreTrainedModel, Trainer, TrainerCallback


class MMLUEvalCallback(TrainerCallback):
    """
    A callback function called after each evaluation step during training.

    Args:
        trainer (Trainer): The trainer instance to be used.
        mmlu_dataset (Dict[str, Any]): The dataset containing MMLU data.
    """
    def __init__(self, trainer: Trainer, mmlu_dataset: Dict[str, Any]):
        self.trainer = trainer
        self.mmlu_dataset = mmlu_dataset

    def on_evaluate(self, args: Dict[str, Any], state: Dict[str, Any],
                    control: Dict[str, Any], model: PreTrainedModel,
                    **kwargs: Any) -> None:
        """
        Iterate over the batches of the evaluation dataset and make predictions for MMLU.

        Args:
            args (Dict[str, Any]): dictionary containing the evaluation arguments.
            state (Dict[str, Any]): dictionary containing the current state of the trainer.
            control (Dict[str, Any]): dictionary containing the evaluation control variables.
            model (PreTrainedModel): the model being evaluated.
        """
        # Get the evaluation data loader and set the maximum length of the source sequence.
        data_loader = self.trainer.get_eval_dataloader(self.mmlu_dataset)
        source_max_len = self.trainer.data_collator.source_max_len
        self.trainer.data_collator.source_max_len = args.mmlu_source_max_len

        # Set the trainer model in evaluation mode and initialize empty lists for predictions and references.
        model.eval()
        preds, refs = [], []
        loss_mmlu = 0

        # Iterate over the batches of the evaluation dataset and make predictions.
        for batch in tqdm(data_loader, total=len(data_loader)):
            (loss, logits, labels) = self.trainer.prediction_step(
                model,
                batch,
                prediction_loss_only=False,
            )

            # Extract the predictions for A, B, C, and D tokens.
            abcd_idx = ['A', 'B', 'C', 'D']
            for i, logit in enumerate(logits):
                label_non_zero_id = (batch['labels'][i] !=
                                     -100).nonzero()[0][0]
                logit_abcd = logit[label_non_zero_id - 1][abcd_idx]
                preds.append(torch.argmax(logit_abcd).item())

            # Extract the ground truth labels and compute the accuracy by subject.
            IGNORE_INDEX = -100
            labels = labels[labels != IGNORE_INDEX].view(-1, 2)[:, 0]
            refs += [abcd_idx.index(label) for label in labels.tolist()]
            loss_mmlu += loss.item()

        # Extract results by subject.
        results = {'mmlu_loss': loss_mmlu / len(data_loader)}
        subject = self.mmlu_dataset['subject']
        subjects = {s: {'refs': [], 'preds': []} for s in set(subject)}
        for s, p, r in zip(subject, preds, refs):
            subjects[s]['preds'].append(p)
            subjects[s]['refs'].append(r)

        # Compute the accuracy score for each subject and log the results.

        subject_scores = []
        for subject in subjects:
            subject_score = accuracy.compute(
                references=subjects[subject]['refs'],
                predictions=subjects[subject]['preds'])['accuracy']
            results[
                f'mmlu_{args.mmlu_split}_accuracy_{subject}'] = subject_score
            subject_scores.append(subject_score)

        # Compute the overall MMLU accuracy and log the results.
        results[f'mmlu_{args.mmlu_split}_accuracy'] = np.mean(subject_scores)
        self.trainer.log(results)

        # Reset the maximum length of the source sequence to its original value.
        self.trainer.data_collator.source_max_len = source_max_len