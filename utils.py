from huggingface_hub import login, HfApi
from datasets import load_dataset, Dataset, load_from_disk
from pathlib import Path

import dotenv
import os
import json



def UploadDataset2HuggingFace(dataset_dir: str, env_path, readme_path:str):

    dotenv.load_dotenv(dotenv_path= env_path)

    # loging to HF
    login(os.getenv("HUG_ACCESS_TOKEN"))
    print("Logged in.")


    # load dataset
    dataset = load_from_disk(dataset_dir)

    # # check the dataset
    # df = dataset.to_pandas()
    # # print(df)
    # # print(json.loads(df["text"].iloc[0]))

    repo_id = "AliRGHZ/Mobile-Action"
    dataset.push_to_hub(repo_id)

    api = HfApi()

    api.upload_file(
        path_or_fileobj= str(readme_path),
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="dataset",
    )




if __name__ == "__main__":
    PROJECT_DIR = Path(".").absolute()

    env_path = PROJECT_DIR / ".env"

    readme_path = PROJECT_DIR / "MobileActions" / "New_Generated" / "Ali" / "mobile-actions" / "README.md"

    dataset_dir = "MobileActions/New_Generated/Ali/mobile-actions"

    UploadDataset2HuggingFace(dataset_dir, env_path, str(readme_path))