import csv
import argparse
from tqdm import tqdm
from datasets import load_dataset


def inference(audio_path, prompt_text):

    # Your model inference code here.
    pass
    return "No"


def main(args):

    # Load the dataset.
    dataset = load_dataset(args.dataset_name)

    # Evaluation results.
    evaluation_results = []

    for sample in tqdm(dataset['test']):

        # Entry ID for the dataset.
        entry_id = sample["entry_id"]

        # The ID in AudioCaps, e.g., Y7fmOlUlwoNg corresponds to Y7fmOlUlwoNg.wav
        audio_index = sample["audio_index"]

        # The absolute path of audio.
        audio_path = f"{args.audio_root_dir}/{audio_index}.wav"

        # The input text prompt.
        prompt_text = sample["prompt_text"]

        # The correct answer corresponding to the prompt_text.
        label = sample["label"]

        # Inference model and get response.
        response = inference(audio_path=audio_path, prompt_text=prompt_text)

        # Record evaluation result.
        evaluation_result = [entry_id, audio_index, label, response]
        evaluation_results.append(evaluation_result)
    
    # Writing the data to CSV using csv module
    with open(args.output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["entry_id", "audio_index", "label", "response"])
        writer.writerows(evaluation_results)
    
    print(f"Inference results are saved to {args.output_path}")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_name", type=str, help="Hugging face dataset name.", default="kuanhuggingface/AudioHallucination_AudioCaps-Random-v2")
    parser.add_argument("--audio_root_dir", type=str, help="Audio root directory", default="./audiocaps")
    parser.add_argument("--output_path", type=str, help="Output path of csv file.", default="./evaluation_result.csv")
    args = parser.parse_args()
    main(args)