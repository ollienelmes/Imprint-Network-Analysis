# Imprint-Network-Analysis
This package generates a network of named individuals extracted from the imprint line found within catalogue data (MARC format).  Named individuals and relationships are exported as a nodes and edges list from which they can be used for network analysis.

***Loading Data***

Catalogue data can be downloaded from the English Short Title Catalogue (ESTC): http://estc.bl.uk/

Using the advanced search function you can limit the time period considered and also filter by place of publication.
Having selected the appropriate records you can export them by clicking on "Email/print/save", and then changing the
format to "MARC tags" from the drop down and pressing "Go", making sure to leave the "Email" field blank. From there
you can copy the fields by clicking on the "Print" button. All records should be saved in a text file, with the file name
formatted as "raw_" + the city name of the dataset. 

N.B. Only 1000 records can be exported at a time, so you may need to do multiple exports and stitch them together in one file

***Limitations***

The name extraction algorithm used is not 100% accurate and there will be some names that are missed out due to edge cases within the catalogue data.
Certain locations may be incorrectly identified as names, any misidentified names can be appended to either the "street_names" or "place_names" text files
to ensure that they are not incorrectly added to the nodes list.
