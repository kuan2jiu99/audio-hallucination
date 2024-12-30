import csv
import argparse


def parse_response(response):
    ''' Parse response. '''

    answer = ""

    if "Yes" in response or "yes" in response:
        answer = "yes"

    elif "No" in response:
        answer = "no"

    elif "there is no sound" in response or "there is no sound of" in response or "there is no" in response:
        answer = "no"

    elif "does not contain" in response or "doesn't contain" in response:
        answer = "no"
    
    elif "contain" in response or "contains" in response:
        answer = "yes"
    
    elif "not" in response or "unable" in response or "can't" in response:
        answer = "no"
    
    else:
        answer = "unknown"
    
    return answer


def check_answer(response, ground_truth):
    response = parse_response(response)
    
    if response == "yes" and ground_truth == "yes":
        answer_type = "TP"
    elif response == "no" and ground_truth == "no":
        answer_type = "TN"
    elif response == "yes" and ground_truth == "no":
        answer_type = "FP"
    elif response == "no" and ground_truth == "yes":
        answer_type = "FN"
    else:
        answer_type = "unknown"
    
    return answer_type


def evaluation(evaluation_result_csv_path):

    answer_type_dict = {
        "TP": 0,
        "TN": 0,
        "FP": 0,
        "FN": 0,
        "unknown": 0
    }
    analysis = {
        "TPTN": 0,
        "FNFP": 0,
        "TPFP": 0,
        "FNTN": 0
    }
    yes_num = 0
    no_follow = 0
        
    with open(evaluation_result_csv_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)

        for index, row in enumerate(csvreader):
            entry_id = row[0]
            audio_index = row[1]
            ground_truth = row[2].lower()
            response = row[3]
            
            answer_type = check_answer(response, ground_truth)
            answer_type_dict[answer_type] += 1

            if parse_response(response) == "yes":
                yes_num += 1

            if parse_response(response) == "unknown":
                no_follow += 1
            
            if index % 2 == 0:
                analysis_before_after = ""
                if answer_type not in ["TN", "FP", "unknown"]: # TP, FN
                    analysis_before_after += answer_type
            else:
                if answer_type not in ["TP", "FN", "unknown"] and len(analysis_before_after) != 0 and "unknown" not in answer_type: # TN, FP
                    analysis_before_after += answer_type
                    analysis[analysis_before_after] += 1
                analysis_before_after = ""
    
    accuracy = (answer_type_dict["TP"] + answer_type_dict["TN"]) / sum(answer_type_dict.values())
    precision = answer_type_dict["TN"] / (answer_type_dict["TN"] + answer_type_dict["FN"])
    recall = answer_type_dict["TN"] / (answer_type_dict["TN"] + answer_type_dict["FP"])
    f1_score = 2 * (precision * recall) / (precision + recall)

    accuracy = round(accuracy * 100, 2)
    precision = round(precision * 100, 2)
    recall = round(recall * 100, 2)
    f1_score = round(f1_score * 100, 2)

    correct_correct = round(100 * (analysis['TPTN'] / sum(analysis.values())), 2)
    incorrect_incorrect = round(100 * (analysis['FNFP'] / sum(analysis.values())), 2)
    correct_incorrect = round(100 * (analysis['TPFP'] / sum(analysis.values())), 2)
    incorrect_correct = round(100 * (analysis['FNTN'] / sum(analysis.values())), 2)

    yes_rate = round(100 * (yes_num / sum(answer_type_dict.values())), 2)
    instruction_follow_rate = round(100 * ((sum(answer_type_dict.values()) - no_follow) / sum(answer_type_dict.values())), 2)

    return accuracy, precision, recall, f1_score, yes_rate, instruction_follow_rate, correct_correct, incorrect_incorrect, correct_incorrect, incorrect_correct


def main(args):

    accuracy, precision, recall, f1_score, yes_rate, instruction_follow_rate, correct_correct, incorrect_incorrect, correct_incorrect, incorrect_correct = evaluation(args.evaluation_result_csv_path)

    # Save evaluation results.
    with open(args.output_path, "w") as f:
        f.write(f"Accuracy: {accuracy}%\n")
        f.write(f"Precision: {precision}%\n")
        f.write(f"Recall: {recall}%\n")
        f.write(f"F1 Score: {f1_score}%\n")
        f.write(f"Yes Rate: {yes_rate}%\n")
        f.write(f"Instruction Follow Rate: {instruction_follow_rate}%\n")
        f.write(f"Correct Correct: {correct_correct}%\n")
        f.write(f"Incorrect Incorrect: {incorrect_incorrect}%\n")
        f.write(f"Correct Incorrect: {correct_incorrect}%\n")
        f.write(f"Incorrect Correct: {incorrect_correct}%\n")
    
    print(f"Accuracy: {accuracy}%")
    print(f"Precision: {precision}%")
    print(f"Recall: {recall}%")
    print(f"F1 Score: {f1_score}%")
    print(f"Yes Rate: {yes_rate}%")
    print(f"Instruction Follow Rate: {instruction_follow_rate}%")
    print(f"Correct Correct: {correct_correct}%")
    print(f"Incorrect Incorrect: {incorrect_incorrect}%")
    print(f"Correct Incorrect: {correct_incorrect}%")
    print(f"Incorrect Correct: {incorrect_correct}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--evaluation_result_csv_path", type=str, help="Hugging face dataset name.", default="./evaluation_result.csv")
    parser.add_argument("--output_path", type=str, help="Output path of csv file.", default="./evaluation_metrics.txt")
    args = parser.parse_args()
    main(args)