from pathlib import Path
from MobileActions.utils import UploadDataset2HuggingFace

if __name__ == "__main__":
    PROJECT_DIR = Path(".").absolute()

    env_path = PROJECT_DIR / ".env"

    readme_path = PROJECT_DIR / "MobileActions" / "README.md"

    dataset_dir = "MobileActions/New_Generated/Ali/mobile-actions"

    repo_id = "AliRGHZ/Mobile-Actions"

    commit_message = "Fixed messages & tools in dataset.jsonl"
    UploadDataset2HuggingFace(dataset_dir, repo_id, env_path, str(readme_path), commit_message)