"""
To complete the generated message which currently contains user and assistant roles.
"""
import json
import random
from datetime import datetime
from zoneinfo import ZoneInfo
import json

import pandas as pd
from pathlib import Path
import logging
import sys




weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

developer_content = f"""You are a model that can do function calling with the following functions. 
    Current date and time given in YYYY-MM-DDTHH:MM:SS format: {datetime.now(ZoneInfo("America/Toronto")).strftime('%Y-%m-%dT%H:%M:%S %Z')}.
    Day of week is {weekdays[datetime.now().weekday()]}.
    """

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
    print("************************************************")

    for message in messages_column:
        # cast each message to list of roles
        message = json.loads(message)

        yield message




def completeDataset(generated_data_file_path, train_portion, complete_data_file_path, tools):
    complete_message_list = []
    # complementary part
    dev_message = [
        {
            "role": "developer",
            "content": f"{developer_content}",
        }
    ]
    metadata = ["train", "eval"]

    # read each row of the messages in the generated dataset
    train_size_check = 0
    for message in loadMessageDataGen(generated_data_file_path):
        assert isinstance(message, list), f"message loaded from the dataset supposed to be a list, but is {type(message)}"
        dataset_row_dict = {"metadata": metadata[0 if random.random() < train_portion else 1], "tools": tools}

        # enrich message
        message_new = []
        message_new.append(dev_message)
        message_new.append(message)

        # add message to dataset_row_dict
        dataset_row_dict.update({"messages": message_new})

        if(dataset_row_dict["metadata"] == "train"):
            train_size_check += 1

        # append to complete_message_list
        complete_message_list.append(json.dumps(dataset_row_dict))

    # create DataFrame
    complete_message_df = pd.DataFrame({"text": complete_message_list})

    # store the completed version
    complete_message_df.to_csv(complete_data_file_path)


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
    completeDataset(generated_data_file_path, train_portion, complete_data_file_path, tools)