# Software for predicting the outcomes of CS2 matches 

## You can test it out here - point516.xyz  
![Demo](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTNtaXNmbDg0OWpscW5sNmdudmVlaTJ5N3BxOGZ2dzF5c2p0eWZpeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/23mIZ6vR4V6hjlUS8Y/source.gif)

### Here's a brief breakdown of what's in this repository:
models - final fine-tuned versions of various machine learning models  
web - landing and prediction web pages with CSS styling  
create-tables.py - postgresql scripts to create tables I used for collected data  
cs_pipeline.pkl - pipeline for feature scaling  
data_science.ipynb - forming dataset + data analysis-visualizations + minor feature engineering, scaling + fine-tuning prediction models  
database.py - python class for postgresql operations to fill the database  
main.py - FastAPI web-application  
parse.py - script for parsing the upcoming matches  
parsing.py - python class with functions to parse HLTV.org
train_data.csv - whole dataset
