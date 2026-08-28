---
license: cc-by-4.0
name: Mobile Action
tags:
- function-calling
- mobile-actions
- google
- functiongemma
formats:
- json
Languages:
- English
---

## Mobile Action
This dataset is meade by concatenating these two mobile-actions datasets: [Extended Mobile Actions](https://huggingface.co/datasets/AliRGHZ/Mobile-Action)
and [Google Mobile Actions](https://huggingface.co/datasets/google/mobile-actions).


## Dataset Format

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

