# SmartBench: Is Your LLM Truly a Good Chinese Smartphone Assistant? [EMNLP 2025]

## 项目简介

SmartBench 是第一个专门针对中文智能手机场景下设备端大语言模型（LLM）能力评估的基准。它通过分析智能手机制造商提供的功能，将设备端 LLM 功能分为五个类别，共 20 个具体任务，涵盖了文本摘要、文本问答、信息抽取、内容创作和通知管理等实际应用场景。SmartBench 提供高质量的数据集和定制化的评估标准，旨在标准化评估设备端 LLM 的能力，推动其在实际移动应用中的进一步发展和优化。



## 研究背景

随着大语言模型（LLM）在智能手机上的广泛应用，其作为智能助手的能力受到了广泛关注。然而，现有的 LLM 评估基准大多侧重于英语中的客观任务，如数学和编程，这些任务并不能完全反映设备端 LLM 在实际移动场景中的使用情况，尤其是对于中文用户。为了填补这一空白，SmartBench 应运而生。

## SmartBench 基准

![alt text](https://github.com/vivo-ai-lab/SmartBench/blob/main/assets/pipline.jpg)



### 数据组成

SmartBench 将设备端 LLM 功能分为以下五个类别，共 20 个具体任务：

![alt text](https://github.com/vivo-ai-lab/SmartBench/blob/main/assets/task.jpg)


### 数据来源

数据主要来源于三个渠道：
1. 通过人工收集和 LLM 生成手机应用真实场景问答对，并进行人工筛选和编辑以确保数据质量。
2. 补充收集、筛选与智能手机应用真实场景相关的开源数据集。
3. 部分收集数据集，利用先进的 LLM（如 Qwen-Max、Gemini Pro）为缺乏适当问答的数据集生成答案。

### 数据筛选

由具有多年端侧 AI 经验的数据专家进行验证，重点关注以下五个核心标准：
1. 与真实世界智能手机交互场景的一致性。
2. 检测有毒或有害信息。
3. 识别潜在的隐私泄露风险。
4. 标记社会争议性或极化性话题。
5. 全面评估参考答案的正确性与指令遵循能力。

### 评估协议

采用“LLM-as-a-Judge”方法进行主观问题评估。为每个功能类别精心设计不同的 LLM 评估提示，特别是对于内容创作、信息抽取和通知管理，为每个任务设计了独特的评分提示，使评分更符合人类感知。每个问题总分为 10 分，并为每个任务的评估提示提供详细的评分维度和标准，以文本续写为例：

![alt text](https://github.com/vivo-ai-lab/SmartBench/blob/main/assets/text_continue.jpg)

## 实验

### BF16 精度评估

评估了 BlueLM-3B、InternVL2.5-4B、MiniCPM3-4B、Qwen2.5-3B 和 Qwen2-VL-2B 等代表性设备端 LLM/MLLM 在 SmartBench 上的表现（BF16 参数精度）。使用 GPT-4 Turbo（gpt-4-turbo-04-09）作为评判 LLM。
![alt text](https://github.com/vivo-ai-lab/SmartBench/blob/main/assets/BF16.jpg)

### INT4 精度评估

将 BlueLM-3B 和 Qwen2.5-3B 模型部署在搭载高通骁龙 8 Gen 3 SoC 的 vivo iQOO 12 智能手机的 NPU 上，量化模型为 W4A16。量化模型保留了超过 80% 的原始能力，整体平均保留率约为 90%。

![alt text](https://github.com/vivo-ai-lab/SmartBench/blob/main/assets/INT4.jpg)

### 人类测试

通过多位人类专家对不同设备端模型的输出进行排名，验证 LLM-as-a-Judge 评估方法的有效性。结果显示，SmartBench 设计的评估提示在所有类别中均优于 MT-Bench 的评估提示。



## 代码运行步骤

### 1. 生成待评估的结果

```bash
# 生成评估结果
cd code

python generate_results.py --test_model_path <path_to_model> --data_path <path_to_data> --model_res <path_to_eval_date>
```

### 2. 采用自动化评估的方式对结果进行评估

```bash
# 运行自动化评估
python evaluate_results.py --eval_prompts_path <path_to_eval_prompts> --model_res <path_to_eval_date> --eval_res <path_to_eval_res>
```

### 3. 对评估结果进行处理获取最后结果

```bash
# 处理评估结果
python process_results.py --eval_res <path_to_eval_res> --score_save_path <path_to_final_results>
```



## 数据许可

SmartBench 使用的开源数据集及其许可信息如下表所示：

| 数据集来源 | 许可证 |
| --- | --- |
| nlp_chinese_corpus | [MIT License](https://github.com/brightmart/nlp_chinese_corpus) |
| WenetSpeech | [CC BY 4.0](https://wenet.org.cn/WenetSpeech/) |
| LCCC | [MIT License](https://github.com/thu-coai/CDial-GPT) |
| Alimeeting4MUG | [CC BY 4.0](https://modelscope.cn/datasets/modelscope/Alimeeting4MUG/) |
| VCSum | [MIT License](https://github.com/hahahawu/VCSum) |
| CMRC 2018 | [CC BY-SA 4.0](https://ymcui.com/cmrc2018/) |
| DuReader-2.0 | [Apache License 2.0](https://github.com/baidu/DuReader/tree/master/DuReader-2.0) |
| Weibo | [CC BY-SA 3.0](https://github.com/hltcoe/golden-horse) |
| MSRA | [CC BY 4.0](https://tianchi.aliyun.com/dataset/144307) |
| OntoNotes Release 4.0 | [Apache License 2.0](https://www.modelscope.cn/datasets/yingxi/cross_ner) |
| CSCD-NS | [MIT License](https://github.com/nghuyong/cscd-ns) |



## 限制

1. 随着技术的进步，设备端 LLM 的功能将持续演变。我们将继续根据新功能的发布更新数据集。

2. SmartBench 是专门为中文用户使用场景设计的。不同国家的智能手机用户的使用习惯和方法可能差异显著。未来，我们将继续支持多种语言。

## 引用
```bash
@article{lu2025smartbench,
  title={SmartBench: Is Your LLM Truly a Good Chinese Smartphone Assistant?},
  author={Lu, Xudong and Gao, Haohao and Wu, Renshou and Ren, Shuai and Chen, Xiaoxin and Li, Hongsheng and Li, Fangyuan},
  journal={arXiv preprint arXiv:2503.06029},
  year={2025}
}
```








