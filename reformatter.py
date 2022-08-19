import pandas as pd
import re



def estc_reformatter(estc_dump):

    titles = pd.DataFrame(columns=["title","author","place","stmt_resp","date","clean_date","estc_id"])

    dollara = '\|a [^\|]*'
    dollarb = '\|b [^\|]*'
    dollarc = '\|c [^\|]*'

    for ind in estc_dump.index:
        imprint_line = estc_dump.values[ind][2]
        place = re.search(dollara, imprint_line).group(0)[3:]
        
        stmt_resp = re.search(dollarb, imprint_line)
        date = re.search(dollarc, imprint_line)

        if stmt_resp:
            stmt_resp = re.search(dollarb, imprint_line).group(0)[3:]
        else: 
            stmt_resp = ""
        
        if date:
            date = re.search(dollarc, imprint_line).group(0)[3:]
        else:
            date = ""
        
        if re.search(r'[0-9]{4}', date):
            clean_date = re.search('[0-9]{4}', date).group(0)
        else:
            clean_date = ""
        
        

        titles.loc[titles.shape[0]] = [estc_dump.values[ind][0], estc_dump.values[ind][1], place, stmt_resp, date, clean_date, estc_dump.values[ind][3]]
        
    print("Total Number of Titles: " + str(len(titles.index)))
    
    return titles