import pandas as pd

def weighted_edge(people_names):
    edge_list = pd.DataFrame(columns=["source","target","book_id"])

    for ind in people_names.index:
        book_id = people_names.values[ind][6]
        #print(book_id)
        for ind2 in people_names.index:
            if ind != ind2:
                book_id2 = people_names.values[ind2][6]
                
                ## if both rows belong to the same book then we know they have a connection so we can add this to the edge_list
                ## the second boolean condition checks that we are not making a link between two identical ids (e.g. a name might appear twice for one id as printer and bookseller)
                if book_id == book_id2 and people_names.values[ind][5] != people_names.values[ind2][5] and not ((edge_list['source'] == people_names.values[ind2][5]) & (edge_list['target'] == people_names.values[ind][5]) & (edge_list['book_id'] == book_id)).any() and not ((edge_list['target'] == people_names.values[ind2][5]) & (edge_list['source'] == people_names.values[ind][5]) & (edge_list['book_id'] == book_id)).any() :
                    edge_list.loc[edge_list.shape[0]] = [people_names.values[ind][5], people_names.values[ind2][5], book_id]
                    
    #edge_list = edge_list.drop_duplicates()
    print("Number of Edges:  " + str(len(edge_list.index)))
    weighted_edge_list = pd.DataFrame(columns=["source","target","weight"])

    for ind in edge_list.index:
        source = edge_list.values[ind][0]
        target = edge_list.values[ind][1]
        if not ((weighted_edge_list['source'] == (source)) & (weighted_edge_list['target'] == (target)) | (weighted_edge_list['source'] == (target)) & (weighted_edge_list['target'] == (source))).any():
            weighted_edge_list.loc[weighted_edge_list.shape[0]] = [edge_list.values[ind][0], edge_list.values[ind][1], 1]
        else:
            index = weighted_edge_list.index[(weighted_edge_list['source'] == (source)) & (weighted_edge_list['target'] == (target)) | (weighted_edge_list['source'] == (target)) & (weighted_edge_list['target'] == (source))].tolist()
            weighted_edge_list.at[index[0], 'weight'] += 1
                    
    print("Number of Weighted Edges: " + str(len(weighted_edge_list.index)))
    return weighted_edge_list