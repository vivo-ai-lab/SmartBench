import argparse
import json
import random
import sys

from tqdm import tqdm
sys.path.append("E:\\2025\\version1\\prompt\\code")
from qwplus import qwplus
from gemini import gemini
from qwmax import qwmax
from BlueLM import BlueLM
from docx import Document
import os
import glob


def get_request(task, eval_prompt_dict, lines):
    request_list = []
    eval_prompt = eval_prompt_dict[task].strip()
    for line in lines:
        task_content = line["request"]
        # print(task_content)
        task_answer = line["response"]
        refer_answer = line["refer_answer"]
        request = eval_prompt.replace("specific_task",task_content).replace("refer_answer",refer_answer).replace("ai_answer",task_answer)
        request_list.append(request)
    return request_list


# 1. Obtain automated evaluation prompts
def find_docx_files(root_folder):
    search_pattern = os.path.join(root_folder, '**', '*.docx')
    v1_docx_files = glob.glob(search_pattern, recursive=True)
    return v1_docx_files

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--eval_prompts_path", default = "SmartBench\\evaluate_prompt", type=str, help="the path to automated evaluation of prompts.")
    parser.add_argument("--model_res", default = "E:\\2025\\SmartBench\\model_res", type=str, help="eval date path")
    parser.add_argument("--eval_res", default = "E:\\2025\\SmartBench\\eval_res", type=str, help="path to save evaluation results")
    args = parser.parse_args()

    
    # 1. Obtain automated evaluation prompts
    eval_prompts_path = args.eval_prompts_path
    prompt_path_list = find_docx_files(eval_prompts_path)

    eval_prompt_dict = {}
    for file_path in prompt_path_list:
        file_name = os.path.basename(file_path)
        prefix = file_name[:4]
        doc = Document(file_path)
        evaluate_prompt = ""
        for para in doc.paragraphs:
            text = para.text + "\n"
            evaluate_prompt += text
        eval_prompt_dict[prefix] = evaluate_prompt
    

    # 2.Obtain the results of the model to be evaluated, along with the corresponding tasks and reference answers.
    for filename in os.listdir(args.eval_date_path):
        if not filename.endswith("json"): continue
        task = filename[:4]
        test_file_path = os.path.join(args.eval_date_path, filename)
        with open(test_file_path,"r",encoding="utf-8") as test_inputs:
            lines = [json.loads(line) for line in test_inputs.readlines()]

        # 3.Obtain the request
        request_list = get_request(task, eval_prompt_dict, lines)

        # 3.Evaluate
        print(f"[{task}]任务--开始评估>>>>>>>>>>>")
        for request in tqdm(request_list):
            request_num, request_success, response = 0, False, ""
            while request_num <= 5 and request_success == False:
                request_num += 1
                try:
                    response = qwmax(request)
                    request_success = True
                except:
                    request_success = False
            final_res = {
                "request":request,
                "response":response,
                "domain":"qwmax"
            }

            with open(f"{args.eval_res_path}\\{task}_eval_res.json","a",encoding="utf-8") as outputs:

                outputs.write(json.dumps(final_res,ensure_ascii=False) + "\n")


