!pip install --user selenium
!pip install --user webdriver_manager
import pandas as pd
import datetime
import pickle 

from src.functions_to_run import main as solomain

saved_posts='src/fb_saved_posts.pkl'

EMAIL = "XXX"
PASSWORD = "XXX"

query='I want this post'
words=['company name','war','environment','financial']

with open(saved_posts, 'rb') as f:
    already_saved=pickle.load(f)
    
database,already_saved=solomain(query,words,EMAIL,PASSWORD,already_saved)

with open(saved_posts, "wb") as output_file:
    pickle.dump(already_saved, output_file)
    
now=datetime.datetime.now()
day=f'{now.year}-{now.month}-{now.day}'
hour=f'{now.hour}e{now.minute}'
datestr=day+'_'+hour
    
writer = pd.ExcelWriter(f'output/{query}_{datestr}.xlsx')
database.to_excel(writer, sheet_name=f'{datestr}', startrow = 2)
writer.close()
