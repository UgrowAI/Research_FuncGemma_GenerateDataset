---
license: cc-by-4.0
name: Mobile Action
tags:
- function-calling
- mobile-actions
- functiongemma
formats:
- json
Languages:
- English
---

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

