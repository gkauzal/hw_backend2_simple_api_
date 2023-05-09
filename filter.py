def filter_list_of_dicts(list_of_dicts, fields):
  filtered_dicts = []
  for item in list_of_dicts:
    newitem = item.copy()
    for key in list(newitem.keys()):
      if key not in fields:
        del newitem[key]
    filtered_dicts.append(newitem)
  return filtered_dicts