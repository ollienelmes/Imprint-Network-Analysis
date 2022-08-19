import timeit
import os.path

from reformatter import estc_reformatter
from estc_cleaner import estc_cleaner
from people_generator import people_extractor
from id_gen import id_gen
from nodes import nodes_gen
from edge_gen import weighted_edge

if __name__ == "__main__":
    start_time = timeit.default_timer()
    
    print("All inputs are required as MARC data stored within a .txt file")
    print("These files should be formatted with the title 'raw_' + city name")
    city = input("Enter city name: ").lower()

    file_exists = os.path.exists('raw_' + city + '.txt')
    while file_exists == False:
        print("File not found in the directory")
        city = input("Please enter city name again: ").lower()
        file_exists = os.path.exists('raw_' + city + '.txt')

    print("***File Found!***")

    with open(r'raw_' + city + '.txt', 'r', encoding="utf-8") as f:
        input = f.read()
    
    print("***RAW INPUT DATA LOADED***")

    #STAGE 1: Reformat data from the ESTC into standard catalog data 
    catalog_unsorted = estc_cleaner(input)
    catalog_data = estc_reformatter(catalog_unsorted)

    print("STAGE 1 COMPLETE")
    print("***Catalogue data loaded***")
    print(catalog_data.head(3))
    catalog_data.to_csv(city + "_cat.csv", index=False)

    #STAGE 2: Extract People and Roles from imprint data
    people_list = people_extractor(catalog_data)

    print("STAGE 2 COMPLETE")
    print("***Names extracted***")

    #STAGE 3: Add People IDs to main list
    people_list_id = id_gen(people_list)

    print("STAGE 3 COMPLETE")
    print("***People IDs generated***")

    #STAGE 4: Generate Node List
    nodes = nodes_gen(people_list_id)
    nodes.to_csv("nodes_" + city + ".csv", index=False)

    print("STAGE 4 COMPLETE")
    print("***Node list generated***")

    #STAGE 5: Generate Edge List
    weighted_edges = weighted_edge(people_list_id)
    weighted_edges.to_csv("weighted_edges_" + city + ".csv", index=False)

    print("STAGE 5 COMPLETE")
    print("***Weighted edge list generated***")
    print(" ")
    print("***Network created***")

    print("Time taken: %s" % (round(timeit.default_timer() - start_time, 8)))