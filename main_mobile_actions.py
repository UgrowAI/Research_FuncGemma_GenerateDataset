from MobileActions.ingest_model import acceptable_format
from MobileActions.New_Generated.validate_generated_dataset import Validate
from MobileActions.New_Generated.complete_dataset import completeDataset
from utils import UploadDataset2HuggingFace
from pathlib import Path
import sys

PROJECT_DIR = Path(".").absolute()

MOBILEACTIONS_DIR = PROJECT_DIR / "MobileActions"
print(f"MOBILEACTIONS_DIR: {MOBILEACTIONS_DIR}")

GENERATED_DIR = MOBILEACTIONS_DIR / "New_Generated"
print(f"GENERATED_DIR: {GENERATED_DIR}")



FUNCTION_DIR = MOBILEACTIONS_DIR / "Functions"
print(f"FUNCTION_DIR: {FUNCTION_DIR}")


if __name__ == "__main__":
    sys.path.append(str(FUNCTION_DIR))
    from plyer_mobile_functions import tools

    validated = False
    try:
        generate_data_file_name = "gpt_generated_with_15_tools_2026_03_19.csv"
        generate_data_file_path = GENERATED_DIR / generate_data_file_name

        # validate
        validation = Validate(tools).validate_dataset(generate_data_file_path)
        print("Main: \N{HEAVY CHECK MARK} Validation done!")
    except Exception as e:
        print(f"Main: \u2718 Validation failed: {e}")
        raise e

    if(not validation[0]):
        raise Exception(f"Original generated dataset is not valid. {generate_data_file_path} \n Invalid data records: {validation[1]}")

    final_dataset_directory = GENERATED_DIR / "Ali/mobile-actions"
    # complete the generated dataset (by adding metadata and developer role)
    try:
        generated_data_file_name = "gpt_generated_with_15_tools_2026_03_19.csv"
        generated_data_file_path = GENERATED_DIR / generated_data_file_name

        train_portion = 0.9

        complete_generated_data_file_name = "(complete)_gpt_generated_with_15_tools_2026_03_19.csv"
        complete_data_file_path = GENERATED_DIR / complete_generated_data_file_name

        json_path_directory = final_dataset_directory
        if (not (write_dir_path := Path(json_path_directory)).is_dir()):
            write_dir_path.mkdir(parents=True, exist_ok=True)

        json_path = json_path_directory / "dataset.jsonl"

        completeDataset(generated_data_file_path, train_portion, complete_data_file_path, json_path, tools)
        print("Main: Dataset completed and stored.")
    except Exception as e:
        print(f"Main: There is an error in completting the dataset: {e}")
        raise e


    # to convert csv to .arrow and store
    try:

        if (not (write_dir_path := Path(final_dataset_directory)).is_dir()):
            write_dir_path.mkdir(parents=True, exist_ok=True)

        acceptable_format(str(complete_data_file_path), str(final_dataset_directory))
        print(f"Main: Dataset converted to .arrow and stored in {final_dataset_directory}")
    except Exception as e:
        print(f"Main: There is an error in converting the dataset to .arrow and store it: {e}")
        raise e

    # upload dataset to hugging face
    env_path = PROJECT_DIR / ".env"
    dataset_dir = GENERATED_DIR / "Ali/mobile-actions"
    readme_path = PROJECT_DIR / "MobileActions" / "README.md"

    commit_message = ""

    try:
        UploadDataset2HuggingFace(str(dataset_dir), env_path, str(readme_path), commit_message)
        print("Main: uploaded to hugging face")
    except Exception as e:
        print(f"Main: There is an error in uploading the dataset to the hugging face: {e}")






# Prompt used to generate new dataset:


"""
Given tools list, I want you to generate user prompt samples with right answer (assistant role). Right answer should provide right function calls in right order along with its required parameters. An example to this request could be:

Example:
"
tools:
[{"function": {"name": "turn_off_flashlight", "description": "Turns the flashlight off.", "parameters": {"type": "OBJECT", "properties": {}}}}, {"function": {"name": "show_map", "description": "Shows a location on the map.", "parameters": {"type": "OBJECT", "properties": {"query": {"type": "STRING", "description": "The location to search for. May be the name of a place, a business, or an address."}}, "required": ["query"]}}}, {"function": {"name": "create_calendar_event", "description": "Creates a new calendar event.", "parameters": {"type": "OBJECT", "properties": {"title": {"type": "STRING", "description": "The title of the event."}, "datetime": {"type": "STRING", "description": "The date and time of the event in the format YYYY-MM-DDTHH:MM:SS."}}, "required": ["title", "datetime"]}}}, {"function": {"name": "turn_on_flashlight", "description": "Turns the flashlight on.", "parameters": {"type": "OBJECT", "properties": {}}}}, {"function": {"name": "send_email", "description": "Sends an email.", "parameters": {"type": "OBJECT", "properties": {"to": {"type": "STRING", "description": "The email address of the recipient."}, "subject": {"type": "STRING", "description": "The subject of the email."}, "body": {"type": "STRING", "description": "The body of the email."}}, "required": ["to", "subject"]}}}, {"function": {"name": "open_wifi_settings", "description": "Opens the Wi-Fi settings.", "parameters": {"type": "OBJECT", "properties": {}}}}, {"function": {"name": "create_contact", "description": "Creates a contact in the phone's contact list.", "parameters": {"type": "OBJECT", "properties": {"phone_number": {"type": "STRING", "description": "The phone number of the contact."}, "last_name": {"type": "STRING", "description": "The last name of the contact."}, "first_name": {"type": "STRING", "description": "The first name of the contact."}, "email": {"type": "STRING", "description": "The email address of the contact."}}, "required": ["first_name", "last_name"]}}}]

message containing the original developer, user roles as well as assistant role:
[{"role": "developer",
  "content": "Current date and time given in YYYY-MM-DDTHH:MM:SS format: 2025-04-02T08:13:21\nDay of week is Wednesday\nYou are a model that can do function calling with the following functions\n"},
 {"role": "user",
  "content": "Please send an email to jessica.moraes@examplecorp.com with the subject \"Lunch tomorrow?\" and the message body \"Are you free to grab a bite at the new caf\u00e9 near the office around 1 PM?\"."},
 {"role": "assistant", "tool_calls": [{"function": {"name": "send_email", "arguments": {
     "body": "Are you free to grab a bite at the new caf\u00e9 near the office around 1 PM?",
     "to": "jessica.moraes@examplecorp.com", "subject": "Lunch tomorrow?"}}}]}
 ]
"

So given this example, please produce valid user and assistant roles.
for producing user prompt to put in content section of the assistant role, please follow the following instruction:
- produce around 300 user prompts for each tool in the provided tool list.
- produce around 5000 user prompts to capture reasonable combination of tool calls.
- Generate your response in as a list of messages contains two elements in a JSON format (python dictionary):
Messages = [Message_1, Message_2, ...]
Message: [{"role": "user", "content": USER_QUERY_GENERATE}, {"role": "assistant", "tool_calls":[Functions]} 
Functions: {"function": {"name": "FUNCTION_NAME", "arguments": {KWARGS}}}

tool list: 
[{'function': {'name': 'list_application', 'description': 'To list the applications installed on this android platform.', 'parameters': {'type': 'OBJECT', 'properties': {}, 'required': []}}}, {'function': {'name': 'open_application', 'description': 'To list the applications installed on this android platform.', 'parameters': {'type': 'OBJECT', 'properties': {'application_name': {'type': 'STRING', 'description': 'Name of the application to be opened.'}}, 'required': ['application_name']}}}, {'function': {'name': 'set_brightness', 'description': 'To set a specific level to the current brightness.', 'parameters': {'type': 'OBJECT', 'properties': {'level': {'type': 'STRING', 'description': 'The brightness level in the range of 0 to 100.'}}, 'required': ['level']}}}, {'function': {'name': 'decrease_brightness', 'description': 'To level down the current brightness.', 'parameters': {'type': 'OBJECT', 'properties': {}, 'required': []}}}, {'function': {'name': 'increase_brightness', 'description': 'To level up the current brightness.', 'parameters': {'type': 'OBJECT', 'properties': {}, 'required': []}}}, {'function': {'name': 'get_current_brightness', 'description': 'To get the current level of brightness.', 'parameters': {'type': 'OBJECT', 'properties': {}, 'required': []}}}, {'function': {'name': 'send_email', 'description': 'Sends an email.', 'parameters': {'type': 'OBJECT', 'properties': {'to': {'type': 'STRING', 'description': 'The recipient email address.'}, 'subject': {'type': 'STRING', 'description': 'The email subject.'}, 'body': {'type': 'STRING', 'description': 'The email body.'}, 'create_chooser': {'type': 'BOOLEAN', 'description': 'Whether to display a program chooser to handle the message.'}}, 'required': ['to', 'subject']}}}, {'function': {'name': 'battery_status', 'description': 'Provides information about the battery of your device.', 'parameters': {'type': 'OBJECT', 'properties': {}, 'required': []}}}, {'function': {'name': 'bluetooth_status', 'description': 'To get the bluetooth status info.', 'parameters': {'type': 'OBJECT', 'properties': {}, 'required': []}}}, {'function': {'name': 'phone_call', 'description': 'Make a call with number or open phone dial.', 'parameters': {'type': 'OBJECT', 'properties': {'number': {'type': 'STRING', 'description': 'The number to which we want to call.'}, 'dial_call': {'type': 'BOOLEAN', 'description': 'True if you want to dial call via phone, and False if you want to call the number directly.'}}, 'required': ['number', 'dial_call']}}}, {'function': {'name': 'phone_sms', 'description': 'Send a sms message.', 'parameters': {'type': 'OBJECT', 'properties': {'sms_recipient': {'type': 'STRING', 'description': 'The recipient number.'}, 'sms_message': {'type': 'STRING', 'description': 'The message body.'}}, 'required': ['sms_recipient']}}}, {'function': {'name': 'take_picture', 'description': 'To take a picture using camera.', 'parameters': {'type': 'OBJECT', 'properties': {}, 'required': []}}}, {'function': {'name': 'take_screenshot', 'description': 'To capture a digital image of what is currently visible on the monitor.', 'parameters': {'type': 'OBJECT', 'properties': {}, 'required': []}}}, {'function': {'name': 'turnOff_light', 'description': 'Turn off the light.', 'parameters': {'type': 'OBJECT', 'properties': {}, 'required': []}}}, {'function': {'name': 'turnOn_light', 'description': 'Turn on the light.', 'parameters': {'type': 'OBJECT', 'properties': {}, 'required': []}}}]

"""
