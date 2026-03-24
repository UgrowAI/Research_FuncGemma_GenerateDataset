"""
Generated dataset should be validated in the following senses:
- Generated data contains valid functions and corresponding parameters.


"""
import json

import pandas as pd
from pathlib import Path
import time
import logging
import sys




def get_generated_dataset(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df




class Validate:
    def __init__(self, tools):
        self.tools = tools

    def look_up_check(self, function_name, arguments):
        print(" - To look up the function name in the tools. ", end="")
        time.sleep(0.001)
        try:
            found_tool = None
            for tool in self.tools:
                tool_func = tool["function"]["name"]
                if (function_name == tool_func):  # found the tool in the tools
                    found_tool = tool
                    # check arguments
                    arguments_list = list(arguments.keys())
                    tool_parameters = tool["function"]["parameters"]["properties"]
                    assert all(argument in tool_parameters for argument in
                               arguments_list), f"At least one argument in the generated message/arguments (i.e. of {arguments_list}) is not in tool parameter {tool}."

                    # check required parameter to be within arguments_list
                    required_parameters = tool["function"]["parameters"]["required"]
                    if (required_parameters):
                        assert all(req_par in arguments_list for req_par in
                                   required_parameters), f"At least one required parameter in the found tool is not within the generated message/arguments (i.e. of {arguments_list}). Found tool is: {tool}."

                    # you might need to check the type of each argument with the parameter
            assert found_tool, f"None of the tools used in the generated message / function name (i.e. {function_name}). tools: {tools}"
        except Exception as e:
            time.sleep(0.1)
            print(f"\u2718 Invalid function name. {function_name} not found. Error: {e}")
            raise e

        # print(f"\r \N{HEAVY CHECK MARK} tool found.", end= "", flush= True)
        print(f" - \N{HEAVY CHECK MARK} tool found.", end="")
        time.sleep(0.001)

    def validate_tool_call(self,tool_call):
        # print("validate_tool_call")
        try:
            assert isinstance(tool_call, dict), f"tool_calls {tool_call} is not dict."
            assert "function" in tool_call, f"function item is not in tool_call {tool_call}."
            assert "name" in tool_call["function"], f"name item is not in tool_call {tool_call}."
            assert "arguments" in tool_call["function"], f"arguments item is not in tool_call {tool_call}."

            # search the name within the tools
            self.look_up_check(tool_call["function"]["name"], tool_call["function"]["arguments"])
        except Exception as e:
            time.sleep(0.01)

            print(f"\u2718 Invalid tool_call: {tool_call}. Error: {e}")
            raise e

    def validate_message(self, message, logger: logging = None):
        try:
            assert "role" in message, f"role item is not in {message}."
            assert isinstance(message, dict), f"message {message} is not dict."

            if(message["role"] == "user" ): # validate user role message.
                assert "content" in message, f"content item is not in {message}."

            elif(message["role"] == "assistant"): # validate assistant role message.
                assert "tool_calls" in message, f"tool_calls item is not in {message}."
                tool_calls = message["tool_calls"]
                assert isinstance(tool_calls, list), f"tool_calls {tool_calls} is not list."
                list(map(self.validate_tool_call, tool_calls))

            else:
                mes = f"INVALID message: {message}"
                raise Exception(mes)
        except Exception as e:
            time.sleep(0.01)

            print(f"\u2718 Invalid message: {e}")
            if(logger):
                logger.error(f"Invalid message: {e}")
            raise e


    def validate_messages(self, index_messages):
        index, messages = index_messages
        if(isinstance(messages, str)):
            messages = json.loads(messages)

        print(f"{index} To validate messages ..", end="")
        # print(f"To validate message of type {type(messages)}")

        # print(f"To validate {messages}")
        try:
            assert isinstance(messages, list), f"messages is not list (it is: {type(messages)})."

            list(map(self.validate_message, messages))

            time.sleep(0.01)

            print(f" *** \r \N{HEAVY CHECK MARK} {index} Data Validated ***", end="")
            # print(f"\r \N{HEAVY CHECK MARK} Data Row / Messages Validated.")
            return ("Passed", 1)
        except Exception as e:
            time.sleep(0.01)

            print(f"\u2718 {index} Invalid messages: {e}" , flush=True)
            return ("Failed", index)


    def validate_dataset(self, generate_data_file_path):

        generated_ds_df = get_generated_dataset(generate_data_file_path)
        print(f"Generated dataset: {generated_ds_df}")

        # get messages column
        messages = generated_ds_df["messages"].values.tolist()
        print(f"messages type: {type(messages)}")
        print(f"messages len: {len(messages)}")
        print(f"messages[0] example: {messages[0]}")
        print(f"messages[0] type: {type(messages[0])}")

        try:
            print("Start validation . . .")
            validation_result = map(self.validate_messages, enumerate(messages))

            time.sleep(1)
            # print(f"\n Data rows check overview: {list(validation_result)}")

            # check if there is a Failed elements
            passed_list = map(lambda r: r[0] if(r[0] == "Passed") else None , list(validation_result))
            passed = all(list(passed_list))
            if(passed):
                print(f"\n Validated: {passed}")
                return True, 1
            else:
                failed_index_list = list(filter(lambda r: r[0] == "Failed", list(validation_result)))

                print(f"\n Validated: {passed}")
                return False, failed_index_list


        except Exception as e:
            time.sleep(1)
            print(f"\n \u2718 Invalid generated dataset: {generate_data_file_path}): {e}")
            raise e

if __name__ == "__main__":
    GENERATED_DIR = Path('.').absolute().parent / "New_Generated"
    print(f"GENERATED_DIR: {GENERATED_DIR}")

    MOBILEACTIONS_DIR = GENERATED_DIR.parent
    print(f"MOBILEACTIONS_DIR: {MOBILEACTIONS_DIR}")

    FUNCTION_DIR = MOBILEACTIONS_DIR / "Functions"
    print(f"FUNCTION_DIR: {FUNCTION_DIR}")


    generate_data_file_name = "gpt_generated_with_15_tools_2026_03_19.csv"
    generate_data_file_path = GENERATED_DIR / generate_data_file_name


    sys.path.append(str(FUNCTION_DIR))
    from plyer_mobile_functions import tools

    # validate
    validated = Validate(tools).validate_dataset(generate_data_file_path)
    if(validated[0]):
        print("Validation done!")
    else:
        print("Validation failed!")
        print(f"Record indexes that failed: {validated[1]}")


