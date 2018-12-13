flat_list  = []
nested_list =[[1,2,[3]],4]

def flatten(nested_list, flat_list):
    for item in nested_list:
        if isinstance(item, list):
            flatten(item, flat_list)
        else:
            flat_list.append(item)

flatten(nested_list, flat_list)
print(flat_list)