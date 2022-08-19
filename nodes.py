import pandas as pd

def nodes_gen(people_names):

    node_list = pd.DataFrame(columns = ["Id","name","roles","dom_role"])

    nodes_dict = {}

    for ind in people_names.index:
        person_id = people_names.values[ind][5]
        first_name = people_names.values[ind][1]
        last_name = people_names.values[ind][2]
        role = people_names.values[ind][3]
        if person_id not in nodes_dict:
            nodes_dict[person_id] = [first_name, last_name, {role : 1}]
        elif role not in nodes_dict[person_id][2]:
            nodes_dict[person_id][2][role] = 1
        else:
            nodes_dict[person_id][2][role] += 1

    for id in nodes_dict:
        roles = ", ".join([str(role) for role in nodes_dict[id][2].keys()])
        dom_role = max(nodes_dict[id][2], key=nodes_dict[id][2].get)
        if str(nodes_dict[id][0]) == "":
            node_list.loc[node_list.shape[0]] = [id, nodes_dict[id][1], roles, dom_role]
        else:
            node_list.loc[node_list.shape[0]] = [id, str(nodes_dict[id][0]) + " " + str(nodes_dict[id][1]), roles, dom_role]

    
    print("Number of nodes: " + str(len(node_list.index)))
    
    return node_list

