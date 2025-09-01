import argparse
import json
import os


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--eval_res", default = "E:\\2024\\SmartBench\\eval_res", type=str, help="path to save evaluation results")
    parser.add_argument("--score_save_path", default = "E:\\2024\\SmartBench\\evaluate_prompt", type=str, help="the save path for the final scores on each task.")

    args = parser.parse_args()
    
    dir_path = args.eval_res
    file_list = os.listdir(dir_path)

    for file in file_list:
        file_path = os.path.join(dir_path,file)
        task = file[:4]
        with open(file_path,"r",encoding="utf-8") as inputs:
            lines = [json.loads(line) for line in inputs.readlines()]

        total_scores = {}  # 存储每个维度的总分
        count = {}         # 存储每个维度的有效样本数

        for line in lines:
            score_text = line["response"]
            s_index = score_text.rfind("{")
            e_index = score_text.rfind("}") + len("}")
            score = score_text[s_index:e_index].replace("'", '"').replace("‘",'"').replace("’",'"')

            try:
                score_dict = json.loads(score)
            except:
                continue

            for key, value in score_dict.items():
                if isinstance(value, (int, float)):
                    total_scores[key] = total_scores.get(key, 0) + value
                    count[key] = count.get(key, 0) + 1

        average_scores = {key: total_scores[key] / count[key] for key in total_scores if count[key] != 0}

        if task == "文本纠错":
            # 将各个维度的平均分乘以10
            average_scores = {key: score * 10 for key, score in average_scores.items()}

        final_score = {"任务":task, "分数":average_scores}

        print(">>>>>>>>>>>>>>>>>>>>>>各个任务上的最终评分<<<<<<<<<<<<<<<<<<<<<<")
        print(final_score)

        # 保存最终得分至指定文件下的txt文件
        with open(args.score_save_path,"a",encoding="utf-8") as outputs:

            outputs.write(json.dumps(final_score,ensure_ascii=False) + "\n")
