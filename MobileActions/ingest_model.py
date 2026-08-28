"""
To make a complete version of Dataset, usually in csv, to Hugging Face datasets.Dataset object – a format that the model
, here Function Gemma, can ingest.
"""
import os
from pathlib import Path
import pandas as pd
from datasets import Dataset


def get_dataset(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df


def acceptable_format(complete_dataset_path:str, write_directory:str):
    """Convert DataFrame to Hugging Face Dataset"""

    convert = True
    # if (any(Path(write_directory).iterdir())):
    #     while True:
    #         user = input("Destination directory is not empty. Do you want to clean and generate new .arrow file it? Yes/N")
    #         if(user == "Yes"):
    #             for file in Path(write_directory).iterdir():
    #                 os.remove(file)
    #             break
    #         elif(user == "N"):
    #             convert = False
    #             break

    if(convert):
        # load complete dataset
        df = get_dataset(complete_dataset_path)

        # convert it to .arrow file in a separate directory
        dataset = Dataset.from_pandas(df)
        dataset.save_to_disk(write_directory)
        # dataset.to_json(Path(write_directory)/"dataset.jsonl")

        # check
        if(any(Path(write_directory).iterdir())):
            print("\u2714 Done!")
    else:
        print("\u2714 Files exists, so ignored to generate a new one!")





if __name__ == "__main__":
    complete_dataset_path = "New_Generated/(complete)_gpt_generated_with_15_tools_2026_03_19.csv"
    write_directory = "New_Generated/Ali/mobile-actions"
    if(not (write_dir_path := Path(write_directory)).is_dir()):
        write_dir_path.mkdir(parents= True, exist_ok= True)

    acceptable_format(complete_dataset_path, write_directory)