import argparse
import json
import os
import sys
import glob
from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument("--test_model_path", default = "E:\\2024\\version1\\prompt\\code", type=str, help="interface path of the model to be evaluated.")
parser.add_argument("--data_path", default = "E:\\2024\\给徐东\\data - 副本", type=str, help="test data path.")
parser.add_argument("--model_res", default = "E:\\2024\\SmartBench\\model_res", type=str, help="path to save model inference results.")

args = parser.parse_args()

sys.path.append(args.test_model_path)

from qwmax import qwmax


if __name__ == '__main__':

    folder_path = args.data_path
    file_paths = glob.glob(os.path.join(folder_path, '*'))
    for file_path in file_paths:
        task = os.path.basename(file_path)[:4]

        if os.path.isfile(file_path):
            with open(file_path, 'r',encoding="utf-8") as file:
                lines = [json.loads(line) for line in file.readlines()]

            for index, line in enumerate(tqdm(lines)):
                request, refer_answer = line["inputs"], line["targets"]
                response = ""
                request_num, request_success = 0, False
                while request_num <= 10 and request_success is False:
                    request_num += 1
                    try:
                        response = qwmax(request)
                        request_success = True
                    except:
                        request_success = False

                if request_success == False:

                    print(f">>> Request number {index + 1} in the {task} task failed ...")

                single_save_file = {"request":request,"response":response,"refer_answer":refer_answer}

                with open(f"{args.model_res}\\{task}_res.json","a",encoding="utf-8") as outputs:
                    outputs.write(json.dumps(single_save_file,ensure_ascii=False) + "\n")
