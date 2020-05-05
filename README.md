# Speaker Identification 
Speaker identification + Sidekit

## Installation:
1. Clone repo

2. Create a virtual environment in a convenient location
  python3 -m venv env
  
    Use as reference [this link](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
  
3. Enable the created virtual environment in cmd. This step must be done each time the project goes to be run.
  
  ```
  source env/bin/activate
  ```

4. Install requirements
   pip install -r requirements.txt
   
5. Download dataset es_co_female.zip  from http://openslr.org/72/

6. Save it in dataset folder inside repo folder 

7. Update conf.yaml file
 - inpath
 - outpath
 
   **DON'T MOVE THE REST**
 
 8. Run in cmd
 ```
 sh ./dataset.sh -s 1 -d ../dataset/crowdsourced-colombian-spanish/es_co_female
 ```
 Check inside folder tools: speakers_id.txt
 
  9. Run in cmd
 ```
 sh ./dataset.sh -s 2 -d ../dataset/crowdsourced-colombian-spanish/es_co_female
 ```
 Check inside folder tools: dict_speakers.txt
 
 10. In root repo folder run:
 ```
 python data_init.py
 ```
 Verify results folder contains: audio and task folders
 
