import json
import os
from tqdm import tqdm
import argparse
import pandas as pd


def load_json(json_path):
    with open(json_path, "r") as f:
        json_data = json.load(f)
    return json_data


def cal_CHAIRscore(label_object_set, prediction_object_set):

    CHAIRscore = 1 - (len(prediction_object_set.intersection(label_object_set)) / len(prediction_object_set)) if len(prediction_object_set) != 0 else -1
    return CHAIRscore


def cal_Cover_score(label_object_set, prediction_object_set):

    Cover_score = (len(prediction_object_set.intersection(label_object_set)) / len(label_object_set))
    return Cover_score


def cal_Hal_score(CHAIRscore):

    if CHAIRscore == -1:
        Hal_score = -1

    else:
        Hal_score = 1 if CHAIRscore != 0 else 0

    return Hal_score


def metric_average(result_dir_list, specified_prompt=None):

    CHAIR_score_list = []
    Cover_score_list = []
    Hal_score_list = []

    for result_dir_path in result_dir_list:
        eval_results = load_json(json_path=result_dir_path)
            
        for yt_id in tqdm(eval_results):
            for prompt in eval_results[yt_id]:
                label = eval_results[yt_id][prompt]["label"]
                prediction = eval_results[yt_id][prompt]["prediction"]
                label = set(label)
                prediction = set(prediction)
                CHAIR_score = cal_CHAIRscore(label_object_set=label, prediction_object_set=prediction)
                Cover_score = cal_Cover_score(label_object_set=label, prediction_object_set=prediction)
                Hal_score = cal_Hal_score(CHAIRscore=CHAIR_score)
                CHAIR_score_list.append(CHAIR_score)
                Cover_score_list.append(Cover_score)
                Hal_score_list.append(Hal_score)
    
    average_chair_score = round((sum(CHAIR_score_list) / len(CHAIR_score_list) * 100), 2)
    average_cover_score = round((sum(Cover_score_list) / len(Cover_score_list) * 100), 2)
    average_hal_score = round((sum(Hal_score_list) / len(Hal_score_list) * 100), 2)

    print("{:<10} | {:<10} | {:<10}".format("CHAIR", "Cover", "Hal"))
    print("{:<10.2f} | {:<10.2f} | {:<10.2f}".format(average_chair_score, average_cover_score, average_hal_score))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--results_dir_list", type=str, default=["/my_model_results.json"])
    
    # Example:
    # python evaluation_generative.py --result_dir_list ["your_model_results.json"]
    # The format of "your_model_results.json" should be like below:
    # {
    #     "yt_id1": {
    #         "prompt1": {
    #               "label": ["object1", "object2", ...],
    #               "prediction": ["object1", "object2", ...]
    #         },
    #         "prompt2": {
    #               "label": ["object1", "object2", ...],
    #               "prediction": ["object1", "object2", ...]
    #         },...
    #     },...
    # }

    args = parser.parse_args()

    metric_average(result_dir_list=args.results_dir_list)


if __name__ == "__main__":
    main()