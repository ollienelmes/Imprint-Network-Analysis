import pandas as pd
import re

def estc_cleaner(text):

    record_list = text.split("Record number")

    i = 1
    title = re.compile(r'   245[0-9]{2}')

    title_list = pd.DataFrame(columns=["title","author","imprint","estc_id"])
    author_line=""

    while i < len(record_list):
        lines = record_list[i].split("\n")
        for line in lines:
            #title match
            if title.search(line):
                title_line = re.sub(r'\|[a-c]','',line)
                title_line = re.sub(title,"",title_line).strip()

            #author match
            elif '     1001' in line:
                author_line = re.sub(r'     10010{0,1}','',line).strip()

            #imprint match
            elif '     260' in line:
                imprint_line = re.sub(r'     260','',line).strip()
                
            #estc no
            elif '     009' in line:
                estc_line = re.sub(r'     009','',line).strip()
        
        title_list.loc[title_list.shape[0]] = [title_line, author_line, imprint_line, estc_line]
        i +=1
        author_line = ""

    return title_list