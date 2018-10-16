

data = [{'name': 'foo', 'add': 'bar', 'opt': [{'1': '1'}, {'2':'2'}]}, {'name': 'bar', 'add': 'foo', 'opt': [{'3': '3'}, {'4':'4'}]}]

for idx, item in enumerate(data):
    data[idx]['opt'] = {'5':'5'}

print(data)

# print(len('hello'))