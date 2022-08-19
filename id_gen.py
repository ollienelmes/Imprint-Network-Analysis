import pandas as pd

def id_gen(people_names):

    names_dict = {}

    id_counter = 1


    for ind in people_names.index:
        # if the first_name column is empty then we will only take the surname
        #print(str(people_names.values[ind][1]))
        if str(people_names.values[ind][1]) == "":
            name = str(people_names.values[ind][2]).strip()
        else:
            #this splices the first letter of the first_name and adds it to the surname
            name = str(people_names.values[ind][1])[0] + " " + str(people_names.values[ind][2]).strip()
        
        #creates an id for each concat as specified above
        if name not in names_dict:
            names_dict[name] = "p" + str(id_counter)
            people_names.at[ind, 'person_id'] = "p" + str(id_counter)
            id_counter += 1
        else:
            people_names.at[ind, 'person_id'] = str(names_dict[name])


    return people_names
