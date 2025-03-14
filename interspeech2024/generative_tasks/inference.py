import csv
import argparse
from tqdm import tqdm
from datasets import load_dataset


def get_generative_task_prompt():

    # Get the discriminative task prompt.
    generative_task_prompt = [
        "Describe the audio.",
        "What do you hear?",
        "What can be inferred from the audio?",
        "This is a sound of",
        "Generate audio caption:"
    ]

    return generative_task_prompt


def inference(audio_path, prompt_text):

    # Your model inference code here.
    pass
    return "No"


def main(args):

    # Load the dataset.
    dataset = load_dataset(args.dataset_name)

    # Evaluation results.
    evaluation_results = []

    dataset = load_dataset(args.dataset_name, split="test")
    dataset_length = len(dataset)

    results = {}

    for index in tqdm(range(dataset_length)):

        # Get the audio path.
        audio_abs_path = f"{args.audio_root_dir}/{dataset['audio'][index]['path']}"

        # Construct result dict.
        audio_index = dataset['audio'][index]['path'].replace(".wav", "")

        # Initialize the dict to store the results.
        results = {}
        results[audio_index] = {}

        # Construct prompt text.
        generative_task_prompt = get_generative_task_prompt()

        # Ground truth caption.
        ground_truth_caption = dataset['caption'][index]

        # Ground truth label.
        ground_truth_label = dataset['label'][index]

        for generative_prompt in generative_task_prompt:

            prompt_text = generative_prompt
            
            # Inference your model.
            response = inference(audio_path=audio_path, prompt_text=prompt_text)
            
            # Save results.
            results[audio_index][prompt_text] = {
                "prediction": response,
                "caption": ground_truth_caption,
                "label": ground_truth_label,
                "task": "generative",
            }

    output_results_path = f"{args.output_path}/evaluation_result.json"
    with open(output_results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_name", type=str, help="Hugging face dataset name.", default="kuanhuggingface/audiocaps_hallucination")
    parser.add_argument("--audio_root_dir", type=str, help="Audio root directory", default="./audiocaps")
    parser.add_argument("--output_path", type=str, help="Output path of csv file.", default="./evaluation_result.csv")
    args = parser.parse_args()
    main(args)