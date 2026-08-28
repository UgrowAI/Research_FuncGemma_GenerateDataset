import os
import json
from json_repair import repair_json

from MobileActions.LoadDataset import MobileActionsDS
from MobileActions.settings import DATASET_DIR, PROJECT_DIR
from dotenv import load_dotenv


def touch_dataset(dataset):
    # touch on the original data
    message = f"{'*' * 40}\n{'*' * 40}\nTouch on the original data\n"
    print(message)
    sample_num = 10
    # sample_num = len(dataset)
    for i in range(sample_num):
        sample = dataset[i]
        print(f"sample: {sample}")
        template_iputs = json.loads(sample['text'])
        print(f"template_iputs: {template_iputs}")


        # checks
        assert isinstance(template_iputs, dict), f"Error: template_iputs type: {type(template_iputs)}"
        assert "messages" in template_iputs, f"messages is not in template_iputs: {template_iputs.keys()}"
        assert "tools" in template_iputs, f"tools is not in template_iputs: {template_iputs.keys()}"


        messages = template_iputs["messages"]
        if(isinstance(messages, str)):
            # print(f"messages is str: {messages}")
            message_before = repair_json(messages)
            messages = json.loads(message_before)
        else:
            if(isinstance(messages, list)):
                print(f"messages is list: {messages}")

        tools = template_iputs["tools"]
        if (isinstance(tools, str)):
            tools_before = repair_json(tools)
            tools = json.loads(tools_before)




        message += f"{'=' * 40}\nMessages: \n{messages}\n"
        message += f"{'-' * 40}\nTools:\n{tools}\n{'=' * 40}\n"

        if("role" not in messages[0]):
            print("EERRRORR!!")
            break

        if (i == sample_num-1):
            message += "ALL CHECKED! "


    message += f"{'*' * 40}\n{'*' * 40}\n"

    print(message)



if __name__ == "__main__":
    # database_path = DATASET_DIR
    # get access_token
    load_dotenv(dotenv_path= PROJECT_DIR / ".env")
    access_token = os.getenv("HUG_ACCESS_TOKEN_")

    loaded_datasets = []

    dataset_id = "AliRGHZ/mobile-actions-merged"

    mobile_action_input = {
        "repo_id": dataset_id,
        "access_token": None,
        "dataset_dir_path": DATASET_DIR,
        # "force_hf": True,
        # "tokenizer": None,
        "logger": None
    }
    dataset = MobileActionsDS(**mobile_action_input).Load_Data()

    print(f"dataset: {dataset}")

    print(f"columns: {dataset.column_names} - {'text' in dataset.column_names} - {'text' in dataset.select_columns(['text']).column_names}")
    # print()
    touch_dataset(dataset)