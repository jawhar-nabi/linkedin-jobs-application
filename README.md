# linkedin-jobs-application
The following repository allow you to apply to jobs selected by keywords, you can also define a blacklist so that the script will not apply to jobs including this words

## prerequists
make sure to have python installed
You have to download chromedriver from [here](https://chromedriver.chromium.org/downloads), select the version compatible with your local chrome version, place the path of your chrome driver in the main.py file on line 142 (executable_path).
So the script can acces you chrome session, add the path to User Data on line 136 that you can find under your local chrome configuration example : C:/Users/USER/AppData/Local/Google/Chrome/User Data/

## To run the project 
all you have to do is : 
- pip install -r requirements.txt
- main.py

## Bonus
Copy a search url in linkedin that you already have done to the line 15 to access directly to that search page

# Important 
make sure to be connected at your local chrome and to add chrome session in line 136 like what is mentionned in prerequists
