
from MobileActions.utils import UploadDataset2HuggingFace
from MobileActions.settings import MOBILE_ACTION_DIR, PROJECT_DIR, DATASET_DIR



if __name__ == "__main__":
    # PROJECT_DIR = Path(".").absolute()

    env_path = PROJECT_DIR / ".env"

    readme_path = MOBILE_ACTION_DIR / "Merge" / "README.md"

    dataset_dir = MOBILE_ACTION_DIR / "Dataset" / "merged_google-mobile-actions_AliRGHZ-Mobile-Actions"

    commit_message = "dataset reformed: to fix some mal messages format"

    repo_id = "AliRGHZ/mobile-actions-merged"
    UploadDataset2HuggingFace(dataset_dir, repo_id, env_path, str(readme_path), commit_message)