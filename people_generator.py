import pandas as pd
import re

def people_extractor(newcastle):

    #LOADS THE CHECKING DATA
    with open(r'street_names.txt', 'r', encoding="utf-8") as f:
        input1 = f.read()

    london_streets = input1.split("\n")

    with open(r'place_names.txt', 'r', encoding="utf-8") as f:
        input2 = f.read()

    location_list = input2.split("\n")

    def location_check(input):

        if name_stripper(input) in location_list or name_stripper(input).lower() in london_streets or input =="Printers" or "street" in input or 'Street' in input:
            status = True
        elif bool(re.search(r'\d', input)):
            status = True
        elif "Bookseller" in input:
            status = True
        else:
            status = False 

        return not status

    #Checks that two named entities are in fact real names (i.e. both are proper nouns)
    def name_check(input):
        name = name_cleaner(input).strip()
        if " " in name:
            nameslist = [names for names in name.split(" ") if names != ""]
            if nameslist[0][0].isupper() and nameslist[1][0].isupper():
                return True
        elif len(name) > 0:
            if name[0].isupper():
                return True

        return False

    def name_cleaner(input):
        name = input.replace("Mr. ", "").replace("and Company", "")
        name = name.replace("Mr ", "").replace("and Co.","")
        name = name.replace("and Sons", "").replace("and Co","")
        name = name.replace("and Son", "")
        return name

    def name_stripper(input):
        name = []
        for char in input:
            if char.isalpha():
                name.append(char) 
        return "".join(name)

    def name_splitter(input):
        name = name_cleaner(input)
        if " " in name:
            nameslist = name.split(" ")
            first_name = name_stripper(nameslist[0].strip())
            second_name = name_stripper(nameslist[1].strip())
        else:
            first_name = ""
            second_name = name_stripper(name.strip())
        return first_name, second_name

    newcastle_people = pd.DataFrame(columns=["book_id","first_name", "second_name","role","location","person_id","estc_id", "source_chunk", "full_source"])
    for ind in newcastle.index:
        imprint_line = str(newcastle.values[ind][3])
        if 's.n.' not in imprint_line:
            ##AUTHOR PARSER
            author_field = re.match(r'\|a [^\|]*', str(newcastle.values[ind][1]))
            if author_field:
                author_field = author_field.group(0)[3:]
                if " " not in author_field:
                    author_surname = author_field
                    author_forename = ""
                else:
                    author_names = author_field.split(",")
                    if len(author_names) > 1:
                        author_surname = author_names[0]
                        author_forename = author_names[1].strip()
                    else:
                        author_surname = author_names[0]
                        author_forename = ""
                
                newcastle_people.loc[newcastle_people.shape[0]] = ["", name_stripper(author_forename), name_stripper(author_surname), "author", "no_loc", "", newcastle.values[ind][6], author_field, str(newcastle.values[ind][1])]

            ###PRINTER PARSER
            if re.match("[P|p]rinted by [A-Z]{1}[^,|;|:]*",imprint_line):
                name = re.search("[P|p]rinted by [A-Z]{1}[^,|;|:]*",imprint_line).group(0)[11:].replace("&","and")
                
                #**No "Ands"**
                #Given the presence of a space we can assume that there will be two names in this group
                #These are then split into first and second name accordingly
                if "and" not in name and " " in name and name_check(name) and "And " not in name:
                    first_name, second_name = name_splitter(name)
                    newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "printer", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                elif " " not in name:
                    pass
                elif "and" in name or "And " in name:
                    if "and" in name:
                        names = name.split("and")
                    else:
                        names = name.split("And")
                    group_1 = names[0]
                    group_2 = names[1].strip()
                    #**Sorting Group 1**
                    #First Case: There is one full word before the first "and"
                    #We can assume that this a surname
                    first_name, second_name = name_splitter(group_1)

                    if second_name == "":
                        newcastle_people.loc[newcastle_people.shape[0]] = ["", "", first_name, "printer", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                    else:
                        newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "printer", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                    
                    #**Sorting Group 2**
                    #If the second group after the first "and" is one word it could mean something else
                    if 'ompany' in group_2 or "Co" in group_2 or group_2 == "son" or 'Son' in group_2:
                        pass
                    elif name_check(group_2):

                        if " " not in group_2:
                            newcastle_people.loc[newcastle_people.shape[0]] = ["", "", group_2, "printer", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                        else:
                            first_name, second_name = name_splitter(group_2)
                            newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "printer", "no_loc", "", newcastle.values[ind][6], name, imprint_line]


            if bool(re.search("[P|p]rinted and sold by [A-Z]{1}[^,|;|:]*",imprint_line)):
                name = re.search("[P|p]rinted and sold by [A-Z]{1}[^,|;|:]*",imprint_line).group(0)[20:].replace("&","and")
                if "and" not in name:
                    if location_check(name) and name_check(name):
                        first_name, second_name = name_splitter(name)
                        newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "printer", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                        newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "bookseller", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                else:
                    names = name.split("and")
                    group_1 = names[0].strip()
                    group_2 = names[1].strip()

                    #**Sorting Group 1**
                    #First Case: There is one full word before the first "and"
                    #We can assume that this a surname
                    first_name, second_name = name_splitter(group_1)

                    if second_name == "":
                        newcastle_people.loc[newcastle_people.shape[0]] = ["", "", first_name, "printer", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                        newcastle_people.loc[newcastle_people.shape[0]] = ["", "", first_name, "bookseller", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                    else:
                        newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "printer", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                        newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "bookseller", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                    
                    #**Sorting Group 2**
                    #If the second group after the first "and" is one word it could mean something else
                    if 'ompany' in group_2 or "Co" in group_2 or group_2 == "son" or 'Son' in group_2:
                        pass
                    elif name_check(group_2):

                        if " " not in group_2:
                            newcastle_people.loc[newcastle_people.shape[0]] = ["", "", group_2, "printer", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                            newcastle_people.loc[newcastle_people.shape[0]] = ["", "", group_2, "bookseller", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                        else:
                            first_name, second_name = name_splitter(group_2)
                            newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "printer", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                            newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "bookseller", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
            
            #PUBLISHER PARSER
            if 'for ' in imprint_line:
                publisher_chunk = imprint_line.split("for ")[1].replace("&", "and").replace("Sold","sold")
                if 'the author' in publisher_chunk:
                    newcastle_people.loc[newcastle_people.shape[0]] = ["", name_stripper(author_forename), name_stripper(author_surname), "publisher", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                else:
                    if "sold " not in publisher_chunk:
                        names = [name.strip() for name in re.findall("[^,|;|:]*", publisher_chunk) if name != "" and name != " " and 'by ' not in name]
                        for name in names:
                            if " and " in name:
                                name = name_cleaner(name) 
                                if name[:4] == "and ":
                                    name = name[4:]
                                nameslist = name.split(" and ")
                                for nam in nameslist:
                                    if nam[0].isupper() and location_check(nam):
                                        first_name, second_name = name_splitter(nam)
                                        newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "publisher", "no_loc", "", newcastle.values[ind][6], name, imprint_line]

                            elif name[0].isupper() and location_check(name):
                                name = name.replace("Mr. ","")
                                name = name.replace("Mr ", "")
                                first_name, second_name = name_splitter(name)
                                newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "publisher", "no_loc", "", newcastle.values[ind][6], name, imprint_line]

                    elif "sold" in publisher_chunk:
                        publisher_chunk = publisher_chunk.split("sold")
                        #Eliminates the final and (if present)
                        if publisher_chunk[0][-4:] == "and " and publisher_chunk[0][:-4] != "" and publisher_chunk[0][0].isupper():
                            first_name, second_name = name_splitter(publisher_chunk[0][:-4])
                            if location_check(first_name) and location_check(second_name):
                                newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "publisher", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                        elif publisher_chunk[0][0].isupper():
                            #doesn't find multiple itmes
                            names = re.findall("[A-Z]{1}[^,|;|:]*", publisher_chunk[0])
                            for name in names:
                                if 'and' in name:
                                    names_pair = name.split("and ")
                                    for n in names_pair:
                                        first_name, second_name = name_splitter(n)
                                        if location_check(n) and name_check(n):
                                            newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "publisher", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                                else:
                                    first_name, second_name = name_splitter(name)
                                    if location_check(name) and name_check(name):
                                        newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "publisher", "no_loc", "", newcastle.values[ind][6], name, imprint_line]

                        #PRINTED FOR AND SOLD BY section 
                        elif publisher_chunk[0] == 'and ':
                            names = re.findall("[A-Z]{1}[^,|;|:]*", publisher_chunk[1])
                            for name in names:
                                if location_check(name) and name_check(name):
                                    if 'and' in name:
                                        names_pair = name.split("and ")
                                        for n in names_pair:
                                            first_name, second_name = name_splitter(n)
                                            newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "publisher", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                                            newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "bookseller", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                                    else:
                                        first_name, second_name = name_splitter(name)
                                        newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "publisher", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                                        newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "bookseller", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                    
                    #PRINTED BY AND FOR (adding simply printer tag)
                    if 'by' in imprint_line.split("for ")[0].replace("&", "and").replace("Sold","sold") or 'By' in imprint_line.split("for ")[1].replace("&", "and").replace("Sold","sold"):
                        #ADD THE PRINTER TAG TO THE FIRST NAME GROUP
                        pass

            #BOOKSELLER PARSER
            if 'sold by ' in imprint_line:
                #the case when sold by appears twice in an imprint
                if re.match('sold [also ]?by .*sold', imprint_line):
                    pass
                #sold only appears once
                else:
                    bookseller_chunk = imprint_line.split("sold by ")[1].replace("&", "and")
                    names = [name_cleaner(name) for name in re.findall("[A-Z]{1}[^,|;|:]*", bookseller_chunk)]

                    for name in names:
                        if location_check(name) and name_check(name):
                            if 'and' in name:
                                names_pair = name.split("and ")
                                for n in names_pair:
                                    if location_check(n) and name_check(n):
                                        first_name, second_name = name_splitter(n)
                                        newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "bookseller", "no_loc", "", newcastle.values[ind][6], name, imprint_line]
                            else:
                                if location_check(name) and name_check(name):
                                    first_name, second_name = name_splitter(name)
                                    newcastle_people.loc[newcastle_people.shape[0]] = ["", first_name, second_name, "bookseller", "no_loc", "", newcastle.values[ind][6], name, imprint_line]

    return newcastle_people

