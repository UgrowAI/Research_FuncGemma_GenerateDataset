#
# from datasets import load_dataset, load_from_disk, Dataset
# from huggingface_hub import hf_hub_download, login
# from pathlib import Path
# import datasets
# import logging
# import dotenv
# import os
# from MobileActions.settings import MOBILE_ACTION_DIR, PROJECT_DIR, DATASET_DIR
#
# class MobileActionsDS:
#     def __init__(self, repo_id, logger: logging = None):
#         self.repo_id = repo_id
#         self.dataset = None
#         self.logger = logger
#
#
#     def Load_Data(self, path2load: Path):
#         self.data_path = path2load/ self.repo_id
#
#         # load local pre-stored dataset or load it from remote repo
#         if(self.data_path.is_dir()):
#             self.dataset = load_from_disk(self.data_path)
#         else:
#             raise Exception("ERROR: First you need to save the model locally.")
#
#         return self.dataset
#
#     def Save_Data(self, access_token, path2save:Path):
#         login(access_token)
#
#         self.data_path = path2save / repo_id
#
#         # load local pre-stored dataset or load it from remote repo
#         if(self.data_path.is_dir()):
#             print(f"{self.repo_id} dataset has already saved.")
#         else:
#             data_file = hf_hub_download(repo_id= self.repo_id, filename="dataset.jsonl", repo_type="dataset")
#
#             self.dataset = load_dataset("text", data_files=data_file)
#             # self.dataset = load_dataset(repo_id)
#             print(f"dataset type: {type(self.dataset)}")
#             self.dataset = self.dataset["train"].shuffle()
#
#             print(f"dataset: {self.dataset}")
#
#             self.dataset.save_to_disk(self.data_path)
#
#
#
#
#
#
# if __name__ == "__main__":
#
#
#     env_path =  PROJECT_DIR / ".env"
#     dotenv.load_dotenv(dotenv_path=env_path)
#
#     # use Hugging Face Access Token and login
#     HUG_ACCESS_TOKEN_NAME = "HUG_ACCESS_TOKEN"
#     access_token = os.environ.get(HUG_ACCESS_TOKEN_NAME)
#
#
#     path2save = DATASET_DIR
#     if(not path2save.is_dir()):
#         path2save.mkdir(parents= True, exist_ok= True)
#
#     repo_id = "google/mobile-actions"
#     MobileActionsDS(repo_id).Save_Data(access_token, path2save)


import json
from random import randint
from datasets import load_dataset, load_from_disk, Dataset
from transformers import AutoTokenizer

import datasets
from transformers import AutoTokenizer, PreTrainedTokenizer
from huggingface_hub import hf_hub_download, login
# from src.Evaluation.utils.dataset.parse_messages import str_messages_to_json
from json_repair import repair_json
# from huggingface_hub import login
import json
import logging
from pathlib import Path





class MobileActionsDS:
    def __init__(self,
                 repo_id: str = "",
                 access_token: str = "",
                 dataset_dir_path:Path = None,
                 force_hf = None,
                 # tokenizer: PreTrainedTokenizer = None,
                 logger: logging = None
                 ):
        self.repo_id = repo_id
        self.database_dir_path = dataset_dir_path
        # self.tokenizer = tokenizer
        self.dataset = None
        self.force_hf = force_hf
        self.logger = logger
        # assert access_token, "access_token is not provided."
        self.access_token = access_token


        self.Print(f"MobileActionsDS initiated to get access to dataset {repo_id}, on the Hugging Face Repo or stored locally.")

    def Load_Data(self):
        # repo_id = "google/mobile-actions"
        data_path = self.database_dir_path / self.repo_id
        # self.Print(f"To load data: first check the datapath: {data_path}")

        message = f"To load data: first check the datapath: {data_path} \n"
        self.Print(message)
        # load local pre-stored dataset or load it from remote repo
        # if(data_path.is_dir() and any(list(data_path.iterdir()))):
        if(not self.force_hf and data_path.is_dir()):
            # self.Print(f"Load from local dir: {data_path}")
            message += f"To load from local dir: {data_path}\n"
            self.Print(message)
            try:
                self.dataset = load_from_disk(data_path)
                # print(f"Dataset loaded from local disk: {data_path}")
                message += f"Dataset loaded from local disk: {data_path}\n"
                self.Print(message)
            except Exception as e:
                # self.Print(f"Exception occured in Loading local database: {e}")
                message += f"Exception occured in Loading local database: \n{e}\n"
                self.Print(message)
            finally:
                message = f"Reached to finally section: {message}"
                self.Print(message)


        else:

            message += "To Load from remote repository.\n"
            self.Print(message)

            if not self.access_token:
                self.access_token = input("Enter your HuggingFace access token:\n")
                # access_token = getpass.getpass(prompt="Enter your HuggingFace access token: ", echo_char="*")
                # access_token = pwinput.pwinput(prompt="Enter your HuggingFace access token: ", mask='*')

            # login
            try:
                login(self.access_token)
            except Exception as e:
                self.Print(f"Exception occurred in login: {e}")


            try:
                data_file = hf_hub_download(repo_id= self.repo_id, filename="dataset.jsonl", repo_type="dataset")
                message += "data_file created!\n"
                # data_file = hf_hub_download(repo_id= repo_id, filename="data/train-00000-of-00001.parquet", repo_type="dataset")
                # data_file = hf_hub_download(repo_id= repo_id, repo_type="dataset")
                # self.dataset = load_dataset("text", data_files=data_file, encoding="utf-8")
                self.Print(message)

                self.dataset = load_dataset("text", data_files=data_file)
                message += "called dataset.\n"
                # self.dataset = load_dataset(repo_id)
                print(f"dataset type: {type(self.dataset)}")
                self.Print(message)

                self.dataset = self.dataset["train"].shuffle()
                message += "dataset[train] shuffled.\n"
                self.Print(message)

                self.dataset.save_to_disk(data_path)
                message += "dataset saved.\n"
                self.Print(message)

            except Exception as e:
                message += f"Error in loading the dataset from Remote Repository.\n{e}"
                self.Print(message)

            finally:
                self.Print(f"{message}\nFinally")

        # apply format
        # print(f"dataset type: {type(self.dataset)}")
        # print(f"dataset: {self.dataset}")
        # print(f"len process dataset text: {len(self.dataset['text'])}")
        # self.processed_dataset = self.dataset.map(self.apply_format)

        return self.dataset

    def Sample_Data(self):
        if(self.dataset):
            # return f"\n\033[1mHere's an example from your dataset:\033[0m \n{json.dumps(json.loads(self.dataset[randint(0, len(self.dataset) - 1)]['text']), indent=2)}"
            return f"\n\033[1mHere's an example from your dataset:\033[0m \n{json.dumps(json.loads(self.dataset[randint(0, len(self.dataset) - 1)]['text']), indent=2)}"
        else:
            return f"First load data by calling Load_Data method."


    def max_sequence_length(self):

        if(self.processed_dataset):
            longest_example = max(self.processed_dataset, key=lambda example: len(example['prompt'] + example['completion']))
            longest_example_token_count = len(self.tokenizer.tokenize(longest_example['prompt'] + longest_example['completion']))
        else:
            raise ValueError("processed_dataset is empty. First call Load_Data.")

        max_token_count = longest_example_token_count + 100

        return max_token_count


    def apply_format(self, sample):
        # print(f"sample: {sample}")
        prompt_and_completion = None
        prompt = None

        message = "Within apply_format: \n"

        # template_iputs = json.loads(repair_json(sample['text']))
        template_iputs = json.loads(sample['text'])
        # message += f"sample text recognized. \n"

        assert isinstance(template_iputs, dict), f"Error: template_iputs type: {type(template_iputs)}"
        assert "messages" in template_iputs, f"messages is not in template_iputs: {template_iputs.keys()}"
        assert "tools" in template_iputs, f"tools is not in template_iputs: {template_iputs.keys()}"
        # message += f"assert passed: There are  messages and tools in the json format of the sample. \n"
        # cast message part if required
        # message += f"messages: {template_iputs['messages']}\n"
        # message += f"messages type: {type(template_iputs['messages'])}\n"
        if (isinstance(template_iputs['messages'], str)):
            # custom replaces to make it compatible with json
            # code = "~*~|$*@!|~"
            message_before = template_iputs['messages']

            try:
                # messages = str_messages_to_json(message_before)
                message_before = repair_json(message_before)

                messages = json.loads(message_before)
                template_iputs['messages'] = messages
            except Exception as e:
                message += f"Error in loading messages using json: \n{e}\n>> Original messages: {template_iputs['messages']}\nmessage_before: {message_before}"
                self.Print(message)
            finally:
                # self.Print(message)
                pass

        assert isinstance(template_iputs['messages'], list), f"messages in template_iputs is not in list type, but {type(template_iputs['messages'])}."
        message += f"json loaded messages: {template_iputs['messages']}\n"

        # cast tools part if required
        # message += f"tools: {template_iputs['tools']}\n"
        # message += f"tools type: {type(template_iputs['tools'])}\n"
        if(isinstance(template_iputs['tools'], str)):
            try:

                # template_iputs['tools'] = template_iputs['tools'].replace("\'", "\"")
                template_iputs['tools'] = repair_json(template_iputs['tools'])

                tools = json.loads(template_iputs['tools'])
                template_iputs['tools'] = tools
            except Exception as e:
                message += f"Error in loading tools using json: \n{e}\n"
                self.Print(message)

            finally:
                # self.Print(message)
                pass
        assert isinstance(template_iputs['tools'], list), f"tools in template_iputs is not in list type, but {type(template_iputs['tools'])}."

        message += f"json loaded tools: {template_iputs['tools']}\n"

        # self.Print("Message: {}")
        # Apply Tokenizer Chat Template
        try:
            prompt_and_completion = self.tokenizer.apply_chat_template(
                template_iputs['messages'],
                tools=template_iputs['tools'],
                tokenize=False,
                # tokenize=True,
                # add_generation_prompt is False since we don't need model output after all
                # messages.
                add_generation_prompt=False)
            message += f"prompt and completion gained by tokenizer.apply_chat_template.\n"
            # message += f"prompt_and_completion: {prompt_and_completion}\n"

        except Exception as e:
            message += f"Error in gaining prompt and completion by tokenizer.apply_chat_template.\n{e}\n"
            self.Print(message)

        finally:
            # self.Print(message)
            pass

        # print("to get prompt template..")
        try:
            prompt = self.tokenizer.apply_chat_template(
                template_iputs['messages'][:-1],
                tools=template_iputs['tools'],
                tokenize=False,
                # tokenize=True,
                # add_generation_prompt is True since we would like to include
                # "<start_of_turn>model" in the prompt, if needed.
                add_generation_prompt=True)

            message += f"prompt gained by tokenizer.apply_chat_template.\n "
            message += f"prompt: {prompt}\n"
        except Exception as e:
            message += f"Error in gaining prompt by tokenizer.apply_chat_template.\n{e}\n"
            self.Print(message)

        finally:
            # self.Print(message)
            pass

        # print("to get completion..")

        if(prompt_and_completion and prompt):
            completion = prompt_and_completion[len(prompt):]
            message += f"completion: {completion}\n"

        else:
            raise Exception(message)

        message += f"completion gained by tokenizer.apply_chat_template.\n"

        message += f"To pack prompt, completion, split into return variable dict.\n"

        # self.Print(message)

        return {
            "prompt": prompt,
            "completion": completion,
            "split": template_iputs["metadata"],
        }
    def train_eval_split(self):
        if (not self.processed_dataset):
            raise ValueError("processed_dataset is empty. First call Load_Data.")

        train_dataset = self.processed_dataset.filter(lambda example: example['split'] == 'train')
        eval_dataset = self.processed_dataset.filter(lambda example: example['split'] == 'eval')

        return train_dataset, eval_dataset


    def __str__(self):
        border = f"{'=' * 40}\n"

        message = "{message}"
        return f"{border}Repo_id: {self.repo_id}\nDatabase dir: {str(self.database_dir_path)}\n{message}{border}"

    def Print(self, message:str):
        message = f"{str(self).format(message = message)}"
        if self.logger:
            if ('error' in message.lower()):
                self.logger.error(message)
            else:
                self.logger.info(message)

        print(message)