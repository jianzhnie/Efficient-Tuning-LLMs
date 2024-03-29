python train_lora.py \
    --model_name_or_path facebook/opt-125m \
    --dataset_name 100PoisonMpts \
    --output_dir work_dir/lora-finetune \
    --num_train_epochs 3 \
    --per_device_train_batch_size 4 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 8 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 500 \
    --save_total_limit 5 \
    --learning_rate 1e-4 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --optim "adamw_torch" \
    --lr_scheduler_type "cosine" \
    --model_max_length 1024 \
    --logging_steps 1 \
    --do_train \
    --do_eval \
    --gradient_checkpointing True
