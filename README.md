## dynamic-form
A simple package to set dynamic fields for a form.

### Features :
1. It contains **7 field types** - Text, TextArea, Radio, Checkbox, Dropdown, File Upload.
2. It contains **7 models** (logically grouped into **2-set** of models) - \
  a. **The first group of 4 models is used to create a custom form with fields**, its field options (for radio/checkbox/dropdown field_types), and fieldvalidations. 
     Below is the relation representation of models. \
    ![image](https://github.com/Assystant/dynamic-form/assets/156311082/e26fbe0d-662f-4ff1-a2b3-739a4ab6ed95)
 
  b. **The second group of 3 models is used to store user values for generated form**. \
     User Input data can either be in the form of text (that will be stored in **_UserInputText_** Model), or fieldOptions (predefined in **_FieldOption_** Model), or attachments (that willl be stored in **_UserInputFileUpload_** Model). \
   **_UserInput_** Model - This is the main model to store user-filled data. It contains 4 fields (all foreign keys) - 
   1. _user_ (to identify which user's data),
   2. _template_ (to identify which template is used),
   3. _field_ (to identify which field is filled in that template),
   4. _GenericForeignKey_ (actual foreignkey of user-entered-value : can be _UserInputText/ FieldOption/ UserInputFileUpload_).
5. It contains features like **sorting of fields** for every template, a boolean value to declare **field is required or not**.

### TODO :
1. Automatic setting scores for sorting the fields.
2. Adding restrictions for GenericForeignKey content_type field to these 3 models only UserInputText/ FieldOption/ UserInputFileUpload.
   
### Installation guide :
```
pip install git+https://github.com/Assystant/dynamic-form.git
```

### Documentation :
[link](https://docs.google.com/document/d/11isJUPVus579HuufeBlJTHpt62TYIpW5Jej7DiPnQVs/edit?usp=sharing)
