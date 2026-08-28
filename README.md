
# Generate Dataset
This script is aiming to work on a generated raw dataset and put it in a complete dataset shape needed to feed the FunctionGemma models.



## How the original dataset made:
Prompt used to generate new dataset:


```description
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
'''
``` 


The raw dataset contains messages with user and assistant roles. First, it needs to be validated such that assure us it contains valid function names and corresponding parameters (using MobileActions/New_Generated/validate_generated_dataset.py).
Then each record which currently contains messages with user and assistant roles to get the following columns (using MobileActions/New_Generated/complete_dataset.py):
```commandline
| -------------- | ---------- | ---------------- |
|    metadata    |    tools   |     messages     |
| -------------- | ---------- | ---------------- |
| train OR valid | tools list | roles: developer,|
|                |            | user, assistant  |
| -------------- | ---------- | ---------------- |

```

## Upload to HuggingFace 
publish.py will upload the dataset along with README.md within MobileAction folder.

## To Combine New Dataset With the Old One
merge_dataset.py within MobileActions/Merge is responsible to merge the new version with the old one.




## Mobile Action
Mobile Actions is the dataset designed to fine-tune function calling models such as FunctionGemma 270M over mobile functionalities.
The dataset contains conversational traces over current 15 Android OS system capabilities.
Fine-tuned model is able to execute on-device's functions with the following provided tools:
```list
- Turning the flashlight on
- Turning the flashlight off
- Send email
- Check battery status
- Check bluetooth status
- Make a phone call
- Send sms message
- Take a picture,
- Take a screenshot
- Get current_brightness
- Decrease brightness
- Increase brightness
- Set brightness
- List installed application
- Open an application

```


## Dataset Format
Dataset contains 9500 records, each represents a data sample in JSON format. Each record is distinguished for training 
and evaluation (90/10 split) purposes using metadata field assigned to ```train``` and ```eval```, respectively. 

Record's fields:
- ```metadata:``` A flag to determine the sample type assigned among training and evaluation datasets.
- ```tools:``` Contains a list of available tools (functions) schema that the model literally is able to call and made of the following elements:
  - ```function:``` An object corresponding to a function:
    - ```name:``` name of the function.
    - ```description:``` A description to the function.
    - ```parameters:``` An object to represent the function's parameters:
      - ```type:``` It's usually OBJECT: Used to encapsulate complex, structured data.
      - ```properties:``` A details on the parameters:
        - ```type:``` Type of the parameter, usually among ```[STRING, NUMBER/INTEGER, BOOLEAN, ARRAY, DATE/TIME]```.
        - ```description:``` A description to the parameter.
      - ```required:``` A list of required properties. 

- ```messages:``` A list of messages contain of different roles. Each message contains:
  - ```role:``` The role among ```[developer, user, assistant]```. The ```user``` role encapsulate the user prompt and ```assistant``` is used for function call by the model.
  - ```content:``` It's used for the ```developer``` and ```user``` role and indicates the content of the developer and user's message, respectively.
  - ```tool_calls:``` It's used for the ```assistant``` role and determines the functions to be called.
    - ```function:``` An object representing a function to be called:
      - ```name:``` The name of the function. It should be among the tools' function name
      - ```arguments:``` A list of the parameters to pass over the function.

