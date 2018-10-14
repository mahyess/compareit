

data = [{'name': 'foo', 'add': 'bar'}, {'name': 'bar', 'add': 'foo'}]

new_dict = {item['name']:item for item in data}

print(new_dict)