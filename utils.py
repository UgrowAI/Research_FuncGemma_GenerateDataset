from huggingface_hub import login, HfApi
from datasets import load_dataset, Dataset, load_from_disk
from pathlib import Path

import dotenv
import os
import json



def UploadDataset2HuggingFace(dataset_dir: str, env_path, readme_path:str, commit_message:str = ""):

    dotenv.load_dotenv(dotenv_path= env_path)

    # loging to HF
    login(os.getenv("HUG_ACCESS_TOKEN"))
    print("Logged in.")


    # load dataset
    dataset = load_from_disk(dataset_dir)
    # dataset = load_from_disk(dataset_dir)
    dataset = dataset.remove_columns('Unnamed: 0')
    print(f"dataset: {dataset}")

    # check the dataset
    # columns = ["metadata", "tools", "messages"]
    # df = dataset.to_pandas()
    # df= df[columns]
    # print(df)

    # print(json.loads(df.iloc[0]))
    # df_dict = df["text"].to_dict()
    # df_list = df.to_list()

    # dict_list = [json.loads(item) for item in df_list] # A list of converted string dicts to dict
    # dict_list_json = json.dumps(dict_list) # make string like json acceptable format
    # df_list_json = json.dumps(df_list[0:10])
    # dict_str_list = [f"{json.loads(item)}" for item in df_list[0:10]]
    # print("df dict: \n", df_dict.keys())
    # print("df list dumps: \n", df_list_json)
    # print("df list loads: \n", json.loads(df_list_json))
    # print("dict list dumps: \n", dict_list_json)
    # print("dict list loads: \n", json.loads(dict_list_json))
    # print("df list: \n", json.loads(f'{df_list[0:10]}'))
    # dataset.from_pandas(df["text"])
    # dataset.fr
    # print(f"dataset: {dataset.from_dict(df['text'].to_dict())}")
    # dataset.from_json(json.loads(df['text'].to_dict()))
    # print(dataset)

    # dataset.from_pandas(df)


    repo_id = "AliRGHZ/Mobile-Action"
    dataset.push_to_hub(repo_id)

    # from huggingface_hub import DatasetCard, DatasetCardData

    api = HfApi()

    api.upload_file(
        path_or_fileobj= str(readme_path),
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="dataset",
    )

    api.upload_folder(
        folder_path= dataset_dir,
        repo_id=repo_id,
        repo_type="dataset",
        commit_message= commit_message

    )

    print("Dataset pushed successfully to the HuggingFace repository.")




if __name__ == "__main__":
    PROJECT_DIR = Path(".").absolute()

    env_path = PROJECT_DIR / ".env"

    readme_path = PROJECT_DIR / "MobileActions" / "README.md"

    dataset_dir = "MobileActions/New_Generated/Ali/mobile-actions"

    commit_message = "adjusted dataset.jsonl"
    UploadDataset2HuggingFace(dataset_dir, env_path, str(readme_path), commit_message)