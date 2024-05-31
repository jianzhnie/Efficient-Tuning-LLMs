<div align="center">
  <img src="assets/guanaco.svg" width="300"/>
<div>&nbsp;</div>
</div>

![GitHub Repo stars](https://img.shields.io/github/stars/jianzhnie/Chinese-Guanaco?style=social)
![GitHub Code License](https://img.shields.io/github/license/jianzhnie/Chinese-Guanaco)
![GitHub last commit](https://img.shields.io/github/last-commit/jianzhnie/Chinese-Guanaco)
![GitHub pull request](https://img.shields.io/badge/PRs-welcome-blue)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<div align="center">

👋🤗🤗👋 加入我们 [WeChat](assets/wechat.jpg).

</div>

# LLamaTuner--- 低资源的大语言模型量化训练/部署方案

<div align="center">

[English](README.md) | 中文

</div>

这里是`LLamaTuner`项目的存储库，旨在构建和开源 遵循指令的`baichuan/LLaMA/Pythia/GLM`中文大模型微调训练方法，该方法可以在**单个 Nvidia RTX-2080TI**上进行训练，多轮聊天机器人可以在**单个 Nvidia RTX-3090**上进行上下文长度 2048的模型训练。

我们使用[bitsandbytes](https://github.com/TimDettmers/bitsandbytes)进行量化，并与Huggingface的[PEFT](https://github.com/huggingface/peft)和 [transformers](https://github.com/huggingface/transformers/)库集成。

本项目主要内容如下：

- 📗 支持全量参数指令微调、LoRA指令微调(后续将会提供支持)， QLoRA低成本高效指令微调。
- 📗 支持绝大部分主流的开源大模型，如百川 baichuan、Ziya、Bloom、LLaMA、Pythia、OPT等。
- 📗 支持lora与base model进行权重合并，推理更便捷。
- 📗 开源和整理指令微调数据集的数据清洗和预处理脚本。
- 📗 开源[一系列指令微调模型权重](https://huggingface.co/GaussianTech/) 。

<details><summary><b>Qlora 简介:</b></summary>

QLora 是一种有效的微调方法，可以在单个48GB GPU上微调65B参数模型，同时保持完整的16位微调任务性能。QLora 使用一种低精度的存储数据类型（NF4）来压缩预训练的语言模型。通过冻结 LM 参数，将相对少量的可训练参数以 Low-Rank Adapters 的形式添加到模型中，LoRA 层是在训练期间更新的唯一参数，使得模型体量大幅压缩同时推理效果几乎没有受到影响。从QLora的名字可以看出，QLora实际上是Quantize+LoRA技术。

我们开源的 Guanaco 模型在 Vicuna 基准测试中优于所有以前的公开发布模型，达到了 ChatGPT 的性能水平 99.3%，而在单个 GPU 上只需要 24 小时的微调。

QLora 引入了多种创新，旨在在不牺牲性能的情况下减少内存使用：

1. 4-bit NormalFloat：这是一种理论上针对正态分布数据的最优的量化数据类型，优于当前普遍使用的FP4与Int4。
2. Double Quantization：相比于当前的模型量化方法，更加节省显存空间。每个参数平均节省0.37bit，对于65B的LLaMA模型，大约能节省3GB显存空间。
3. Paged Optimizers：使用NVIDIA统一内存来避免在处理小批量的长序列时出现的梯度 Checkppints 内存峰值。
4. 增加 Adapter：4-bit NormalFloat与Double Quantization，节省了很多空间，但带来了性能损失，作者通过插入更多adapter来弥补这种性能损失。在LoRA中，一般会选择在query和value的全连接层处插入adapter。而QLora则在所有全连接层处都插入了adapter，增加了训练参数，弥补精度带来的性能损失。

完整介绍查看：[QLORA: LLamaTuner](https://jianzhnie.github.io/machine-learning-wiki/#/ai-general/quantization/qlora)

</details>

## 新闻

- [23/06/25] 我们发布了有监督的finetune baichuan-7B模型（[GaussianTech/baichuan-7b-sft](https://huggingface.co/GaussianTech/baichuan-7b-sft)）和相应的训练脚本。
- [23/06/24] 我们发布了有监督的finetune llama-7B模型（[GaussianTech/llama-7b-sft](https://huggingface.co/GaussianTech/llama-7b-sft)）和相应的训练脚本。
- [23/06/15] 现在我们在这个仓库中支持训练 baichuan-7B 模型， 尝试`--model_name_or_path baichuan-inc/baichuan-7B`使用baichuan-7B型号。
- [23/06/03] 现在我们支持量化训练和推理（又名 QLoRA），尝试`scripts/qlora_finetune/finetune_llama_guanaco7b.sh`并设置`--bits 4/8`参数以使用量化模型。
- [23/05/25] 现在支持Lora训练和推理， 尝试 `scripts/lora_finetune/lora-finetune_alpaca.sh` 在 Alpaca 数据集上使用 Lora 微调 LLAMA 模型。
- [20/05/23] 目前支持全参数调优和部分参数微调，尝试`scripts/full_finetune/full-finetune_alpaca.sh` 在Alpaca 数据集上完全微调 LLAMA 模型。

## 支持的模型

- [LLaMA](https://github.com/facebookresearch/llama) (7B/13B/33B/65B)
- [LLama2](https://huggingface.co/meta-llama) (7B/13B/33B/70B)
- [BLOOM](https://huggingface.co/bigscience/bloom) & [BLOOMZ](https://huggingface.co/bigscience/bloomz) (560M/1.1B/1.7B/3B/7.1B/176B)
- [baichuan](https://huggingface.co/baichuan-inc/baichuan-7B) (7B)
- [OPT](https://huggingface.co/docs/transformers/model_doc/opt) (125M/350M/1.3B/2.7B/6.7B/66B )

## 支持的训练方法

- (Continually) pre-training
  - Full-parameter tuning
  - Partial-parameter tuning
  - [LoRA](https://arxiv.org/abs/2106.09685)
  - [QLoRA](https://arxiv.org/abs/2305.14314)
- Supervised fine-tuning
  - Full-parameter tuning
  - Partial-parameter tuning
  - [LoRA](https://arxiv.org/abs/2106.09685)
  - [QLoRA](https://arxiv.org/abs/2305.14314)

## 提供的数据集接口

截至目前，我们支持以下数据集，这些数据集都可以在 [Hugging Face Datasets](https://huggingface.co/datasets) 上找到。我们将在未来添加更多数据集。

- For supervised fine-tuning:

  - [Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca)
  - [Stanford Alpaca (Chinese)](https://github.com/ymcui/Chinese-LLaMA-Alpaca)
  - [Hello-SimpleAI/HC3](https://huggingface.co/datasets/Hello-SimpleAI/HC3)
  - [databricks-dolly-15k](https://huggingface.co/datasets/databricks/databricks-dolly-15k)
  - [mosaicml/dolly_hhrlhf](https://huggingface.co/datasets/mosaicml/dolly_hhrlhf)
  - [GPT-4 Generated Data](https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM)
  - [Alpaca CoT](https://huggingface.co/datasets/QingyiSi/Alpaca-CoT)
  - [UltraChat](https://github.com/thunlp/UltraChat)
  - [OpenAssistant/oasst1](https://huggingface.co/datasets/OpenAssistant/oasst1)
  - [ShareGPT_Vicuna_unfiltered](https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered)
  - [BIAI/OL-CC](https://data.baai.ac.cn/details/OL-CC)
  - [timdettmers/openassistant-guanaco](https://huggingface.co/datasets/timdettmers/openassistant-guanaco)
  - [Evol-Instruct](https://huggingface.co/datasets/victor123/evol_instruct_70k)

- For reward model training:

  - [HH-RLHF](https://huggingface.co/datasets/Anthropic/hh-rlhf)
  - [Open Assistant](https://huggingface.co/datasets/OpenAssistant/oasst1)
  - [GPT-4 Generated Data](https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM)
  - [GPT-4 Generated Data (Chinese)](https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM)

请参考 [data/README.md](data/README.md) 了解如何使用这些数据集训练自己的 ChatGPT。如果您想探索更多数据集，请参考 [awesome-instruction-datasets](https://github.com/jianzhnie/awesome-instruction-datasets). 默认情况下，我们使用 [Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca) 数据集进行训练和微调。

部分数据集需要 huggingface 的账号认证确认才能使用，我们建议使用以下命令登录您的 Hugging Face 账户。

```bash
pip install --upgrade huggingface_hub
huggingface-cli login
```

### 数据预处理

我们在 [data](./chatllms/data/) 文件夹中提供了数据预处理和格式化的脚本。这些脚本可以用于将数据集转换为我们的格式，以便在训练和微调中使用。

- data_utils.py：数据预处理和格式化
- sft_dataset.py：有监督的对话数据集类
- conv_dataset.py：多轮对话数据集类

## 模型仓库

我们在 [Hugging Face ](https://huggingface.co/GaussianTech/)提供了许多模型。这些模型经过Self- Instruct 数据集的训练，可用于推理和微调：

🔔 使用本项目的训练代码，以及上述训练数据，我们训练并开源了以下模型。

| Base Model                                                       | Adapter      | Instruct Datasets                                                                          | Model on Huggingface                                                                |
| ---------------------------------------------------------------- | ------------ | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| [llama-7b](https://huggingface.co/decapoda-research/llama-7b-hf) | FullFinetune | -                                                                                          |                                                                                     |
| [llama-7b](https://huggingface.co/decapoda-research/llama-7b-hf) | QLoRA        | [openassistant-guanaco](https://huggingface.co/datasets/timdettmers/openassistant-guanaco) | [GaussianTech/llama-7b-sft](https://huggingface.co/GaussianTech/llama-7b-sft)       |
| [llama-7b](https://huggingface.co/decapoda-research/llama-7b-hf) | QLoRA        | [OL-CC](https://data.baai.ac.cn/details/OL-CC)                                             |                                                                                     |
| [baichuan7b](https://huggingface.co/baichuan-inc/baichuan-7B)    | QLoRA        | [openassistant-guanaco](https://huggingface.co/datasets/timdettmers/openassistant-guanaco) | [GaussianTech/baichuan-7b-sft](https://huggingface.co/GaussianTech/baichuan-7b-sft) |
| [baichuan7b](https://huggingface.co/baichuan-inc/baichuan-7B)    | QLoRA        | [OL-CC](https://data.baai.ac.cn/details/OL-CC)                                             | -                                                                                   |

## 安装

### 要求

- CUDA >= 11.0
- Python 3.8+ 和 PyTorch 1.13.1+
- 🤗Transformers、数据集、Accelerate、PEFT 和 bitsandbytes
- jieba、rouge_chinese 和 nltk（评估时使用）
- gradio（在gradio_webserver.py中使用）

### 安装所需的包

要使用 Transformer 和 BitsandBytes 加载 4 位模型，您必须从源代码安装加速器和 Transformer，并确保您拥有最新版本的 BitsandBytes 库 (0.39.0)。您可以使用以下命令来实现上述目的：

```shell
pip install -q -U bitsandbytes
pip install -q -U git+https://github.com/huggingface/transformers.git
pip install -q -U git+https://github.com/huggingface/peft.git
pip install -q -U git+https://github.com/huggingface/accelerate.git
```

### 克隆代码

克隆此存储库并导航到 Efficient-Tuning-LLMs 文件夹

```shell
git clone https://github.com/jianzhnie/Efficient-Tuning-LLMs.git
cd Efficient-Tuning-LLMs
```

## 快速开始

### QLora int4 微调

该`train_qlora.py`代码是对各种数据集进行微调和推理的起点。在 Alpaca 数据集上微调基线模型的基本命令：

```shell
python train_qlora.py --model_name_or_path <path_or_name>
```

对于大于13B的模型，我们建议调整学习率：

```shell
python train_qlora.py –learning_rate 0.0001 --model_name_or_path <path_or_name>
```

要查找更多用于微调和推理的脚本，请参阅该`scripts`文件夹。


## License

`LLamaTuner`根据 Apache 2.0 许可证发布。

## 致谢

我们感谢 Huggingface 团队，特别是 Younes Belkada，感谢他们支持将 QLoRA 与 PEFT 和 Transformer 库集成。

我们感谢许多开源贡献者的工作，特别是：

- [Alpaca-LoRA](https://github.com/tloen/alpaca-lora/)
- [LoRA](https://github.com/microsoft/LoRA/)
- [Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca/)
- [Hugging Face](https://huggingface.co/)
- [LLaMa](https://github.com/facebookresearch/llama/)
- [Vicuna](https://github.com/lm-sys/FastChat/)

## 引用

如果您使用此存储库中的数据或代码，请引用该存储库。

```
@misc{Chinese-Guanaco,
  author = {jianzhnie},
  title = { LLamaTuner: Easy and Efficient Fine-tuning LLMs},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/jianzhnie/LLamaTuner}},
}
```
