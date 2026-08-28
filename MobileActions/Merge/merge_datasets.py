import os

from MobileActions.LoadDataset import MobileActionsDS
from MobileActions.settings import DATASET_DIR, PROJECT_DIR
from dotenv import load_dotenv
from datasets import load_dataset, concatenate_datasets
import json
import datasets



DATASET_ID_LIST = [
    "google/mobile-actions",
    "AliRGHZ/Mobile-Actions"
]



def touch_dataset(dataset):
    # touch on the original data
    message = f"{'*' * 40}\n{'*' * 40}\nTouch on the original data\n"
    print(message)
    sample_num = 10
    for i in range(sample_num):
        sample = dataset[i]
        print(f"sample: {sample}")
        # template_iputs = json.loads(sample['text'])
        # print(f"template_iputs: {template_iputs}")


if __name__ == "__main__":
    # database_path = DATASET_DIR
    # get access_token
    load_dotenv(dotenv_path= PROJECT_DIR / ".env")
    access_token = os.getenv("HUG_ACCESS_TOKEN_")

    loaded_datasets = []

    templ_dataset = None
    for dataset_id in DATASET_ID_LIST:
        mobile_action_input = {
            "repo_id": dataset_id,
            "access_token": access_token,
            "dataset_dir_path": DATASET_DIR,
            # "tokenizer": None,
            "logger": None
        }
        dataset = MobileActionsDS(**mobile_action_input).Load_Data()

        # to ignore existing text column
        print(f"dataset text type:{type(dataset)}")

        dataset_list = dataset.to_pandas()["text"].to_list()
        print(f"sample dataset list: {dataset_list[0]}")


        # loaded_datasets += list(map(lambda x: {x: y if(isinstance(y, str)) else str(y) for x,y in json.loads(x).items()}, dataset_list))
        loaded_datasets += list(map(lambda x: {x: y if(isinstance(y, str)) else json.dumps(y) for x,y in json.loads(x).items()}, dataset_list))

    print("All Datasets loaded. Now merge them...")

    print(f"loaded_datasets: {loaded_datasets[0:2]}")
    merged_dataset = datasets.Dataset.from_list(loaded_datasets)
    print("Merged dataset.")
    touch_dataset(merged_dataset)

    merged_dataset_dir = DATASET_DIR / f"merged_{'_'.join(list(map(lambda x: x.replace('/', '-'), DATASET_ID_LIST)))}"
    merged_dataset.save_to_disk(merged_dataset_dir)

    merged_dataset.to_json(merged_dataset_dir/"dataset.jsonl", lines=True)

    print(f"Merged dataset stored:\n{merged_dataset}")

    print("Done!")

    #  THE OLD WAY OF CONCATENATING DATASETS. It leaded to extra 'text' column in the dataset.
    # try:
    #     merged_dataset = concatenate_datasets(loaded_datasets)
    #
    #     print("Merged dataset.")
    #
    #     if("text" in merged_dataset.select_columns(["text"]).column_names):
    #         # if("text" in merged_dataset.select_columns(["text"]).column_names):
    #         merged_dataset = merged_dataset.select_columns(["text"]).select_columns(["text"]).select_columns(["text"])
    #         print(f"got ride of the text column..: {merged_dataset} - ")
    #
    #     touch_dataset(merged_dataset)
    #
    #     merged_dataset_dir = DATASET_DIR / f"merged_{'_'.join(list(map(lambda x: x.replace('/', '-'), DATASET_ID_LIST)))}"
    #     merged_dataset.save_to_disk(merged_dataset_dir)
    #
    #     merged_dataset.to_json(merged_dataset_dir/"dataset.jsonl", lines=True)
    #
    #     print(f"Merged dataset stored:\n{merged_dataset}")
    #
    #     print("Done!")
    # except Exception as e:
    #     print(f"Error! : {e}")
    #     raise e
