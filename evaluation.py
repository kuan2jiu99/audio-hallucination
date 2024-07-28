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
    
    return answer


def evaluation(evaluation_result_csv_path):
    
    totoal_positive = 0 # All question with "Yes" label.
    total_negative = 0 # All question with "No" label.
    answer_right = 0 # Number of questions the model answered correctly
    answer_wrong = 0 # Number of questions the model answered incorrectly
    answer_right_negative = 0 # Number of correct answers that were "No"
    answer_positive = 0 # Number of answers the model gave as "Yes"
    answer_negative = 0 # Number of answers the model gave as "No"

    with open(evaluation_result_csv_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)

        for row in csvreader:
            entry_id = row[0]
            audio_index = row[1]
            label = row[2].lower()
            response = row[3]
            
            # Normalize the output.
            normalized_output = parse_response(response=response)

            if normalized_output == "yes":
                answer_positive += 1
            else:
                answer_negative += 1

            if label == "yes":
                totoal_positive += 1
                if normalized_output == label:
                    answer_right += 1
                else:
                    answer_wrong += 1

            else: # label == "no"
                total_negative += 1
                if normalized_output == label:
                    answer_right += 1
                    answer_right_negative += 1
                else:
                    answer_wrong += 1

    accuracy = answer_right / (answer_right + answer_wrong)
    accuracy = round(accuracy * 100, 2)

    precision = answer_right_negative / (answer_negative)
    precision = round(precision * 100, 2)

    recall = answer_right_negative / (total_negative)
    recall = round(recall * 100, 2)

    f1_score = (2 * precision * recall) / (precision + recall)
    f1_score = round(f1_score, 2)
        
    yes_rate = answer_positive / (answer_positive + answer_negative)
    yes_rate = round(yes_rate * 100, 2)

    return accuracy, precision, recall, f1_score, yes_rate


def main(args):

    accuracy, precision, recall, f1_score, yes_rate = evaluation(args.evaluation_result_csv_path)

    # Save evaluation results.
    with open(args.output_path, "w") as f:
        f.write(f"Accuracy: {accuracy}%\n")
        f.write(f"Precision: {precision}%\n")
        f.write(f"Recall: {recall}%\n")
        f.write(f"F1 Score: {f1_score}%\n")
        f.write(f"Yes Rate: {yes_rate}%\n")
    
    print(f"Accuracy: {accuracy}%")
    print(f"Precision: {precision}%")
    print(f"Recall: {recall}%")
    print(f"F1 Score: {f1_score}%")
    print(f"Yes Rate: {yes_rate}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--evaluation_result_csv_path", type=str, help="Hugging face dataset name.", default="./evaluation_result.csv")
    parser.add_argument("--output_path", type=str, help="Output path of csv file.", default="./evaluation_metrics.txt")
    args = parser.parse_args()
    main(args)