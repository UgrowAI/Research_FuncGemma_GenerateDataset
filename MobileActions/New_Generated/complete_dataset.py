"""
To complete the generated message which currently contains user and assistant roles.
"""
import json
import random
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import datasets

import pandas as pd
from pathlib import Path
import logging
import sys




weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

developer_content = f"""You are a model that can do function calling with the following functions. 
    Current date and time given in YYYY-MM-DDTHH:MM:SS format: {datetime.now(ZoneInfo("America/Toronto")).strftime('%Y-%m-%dT%H:%M:%S %Z')}\n.
    Day of week is {weekdays[datetime.now().weekday()]}\n.
    """



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


    #     # checks
    #     assert isinstance(template_iputs, dict), f"Error: template_iputs type: {type(template_iputs)}"
    #     assert "messages" in template_iputs, f"messages is not in template_iputs: {template_iputs.keys()}"
    #     assert "tools" in template_iputs, f"tools is not in template_iputs: {template_iputs.keys()}"
    #
    #
    #     messages = template_iputs["messages"]
    #     tools = template_iputs["tools"]
    #     message += f"{'=' * 40}\nMessages: \n{messages}\n"
    #     message += f"{'-' * 40}\nTools:\n{tools}\n{'=' * 40}\n"
    #
    # message += f"{'*' * 40}\n{'*' * 40}\n"

    # print(message)


def get_dataset(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df

def loadMessageDataGen(generate_data_file_path):
    generated_ds_df = get_dataset(generate_data_file_path)
    print(f"Generated dataset: {generated_ds_df}")

    # get messages column
    messages_column = generated_ds_df["messages"].values.tolist()
    print("**** Message Column of the generated data ****")
    print(f"messages_column type: {type(messages_column)}")
    print(f"messages_column len: {len(messages_column)}")
    print(f"messages_column[0] example: {messages_column[0]}")
    print(f"messages_column[0] type: {type(messages_column[0])}")
    # print(f"messages_column[0] type: {type(json.loads(messages_column[0]))}")
    print("************************************************")

    for message in messages_column:
        # cast each message to list of roles
        message = json.loads(message)

        yield message




def completeDataset(generated_data_file_path, train_portion, complete_data_file_path, json_path, tools):
    complete_message_list = []
    # complementary part
    dev_message = [
        {
            "role": "developer",
            "content": f"{developer_content}",
        }
    ]
    metadata = ["train", "eval"]
    complete_message_list_dataset = [] # to be used in dataset.Dataset.from_list()

    # read each row of the messages in the generated dataset
    train_size_check = 0
    for message in loadMessageDataGen(generated_data_file_path):
        assert isinstance(message, list), f"message loaded from the dataset supposed to be a list, but is {type(message)}"
        # dataset_row_dict = {"metadata": metadata[0 if random.random() < train_portion else 1], "tools": f"{tools}"}
        dataset_row_dict = {"metadata": metadata[0 if random.random() < train_portion else 1], "tools": tools}
        dataset_row_dict_dataset = {"metadata": metadata[0 if random.random() < train_portion else 1], "tools": str(tools)}

        # enrich message
        message_new = []
        message_new += dev_message
        message_new += message

        # add message to dataset_row_dict
        # dataset_row_dict.update({"messages": f"{message_new}"})
        dataset_row_dict.update({"messages": message_new})
        dataset_row_dict_dataset.update({"messages": str(message_new)})

        if(dataset_row_dict["metadata"] == "train"):
            train_size_check += 1

        # append string of dict format to complete_message_list
        # complete_message_list.append(json.dumps(dataset_row_dict))

        # append dict format to complete_message_list
        complete_message_list.append(dataset_row_dict)
        complete_message_list_dataset.append(dataset_row_dict_dataset)



    # print
    print(f"A few samples from complete_message_list: \n{complete_message_list[2]}\n{'-'*40}")
    print(f"A few samples from complete_message_list_dataset: \n{complete_message_list_dataset[2]}\n{'-'*40}")
    # create DataFrame with text column
    # complete_message_df = pd.DataFrame({"text": complete_message_list})

    # create DataFrame with dict keys as its column
    complete_message_df = pd.DataFrame(complete_message_list)

    # store the completed version
    complete_message_df.to_csv(complete_data_file_path)

    # complete_message_df.to_json(json_path)
    # dataset = datasets.Dataset.from_pandas(complete_message_df)
    # datasets.Dataset.from_dict()
    # dataset.to_json(json_path)
    # print(f"dataset: {dataset} stored as jsonl.")

    # You need make dataset directly from list of dicts in order to create json file needed to be fed to the model in the fine-tuning.
    dataset = datasets.Dataset.from_list(complete_message_list_dataset)
    print("dataset created from the list of dicts.")
    # print(dataset)
    touch_dataset(dataset)
    print("Now convert it to json.")
    dataset.to_json(json_path)
    print(f"dataset stored in {json_path}.")

    # with open(json_path, "w") as json_file:
    #     json.dump(complete_message_list, json_file)

    print("Done!")


if __name__=="__main__":
    GENERATED_DIR = Path('.').absolute().parent / "New_Generated"
    print(f"GENERATED_DIR: {GENERATED_DIR}")

    MOBILEACTIONS_DIR = GENERATED_DIR.parent
    print(f"MOBILEACTIONS_DIR: {MOBILEACTIONS_DIR}")

    FUNCTION_DIR = MOBILEACTIONS_DIR / "Functions"
    print(f"FUNCTION_DIR: {FUNCTION_DIR}")

    sys.path.append(str(FUNCTION_DIR))

    from plyer_mobile_functions import tools

    generated_data_file_name = "gpt_generated_with_15_tools_2026_03_19.csv"
    generated_data_file_path = GENERATED_DIR / generated_data_file_name

    train_portion = 0.9

    complete_generated_data_file_name = "(complete)_gpt_generated_with_15_tools_2026_03_19.csv"
    complete_data_file_path = GENERATED_DIR / complete_generated_data_file_name

    json_path_directory = GENERATED_DIR / "Ali/mobile-actions"
    if (not (write_dir_path := Path(json_path_directory)).is_dir()):
        write_dir_path.mkdir(parents=True, exist_ok=True)
    json_path = json_path_directory / "dataset.jsonl"

    completeDataset(generated_data_file_path, train_portion, complete_data_file_path, json_path, tools)