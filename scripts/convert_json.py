import json

def load_data():
    with open('data.json', 'r') as file:
        content = ''.join(file.readlines())
        return json.loads(content)

def convert_data(data):
    header = ','.join(data[0].keys())
    main_content = []

    for item in data:
        values = [str(value) for value in item.values()]
        main_content.append(','.join(values))
    
    return header, '\n'.join(main_content)

data = load_data()

with open('data.csv', 'w') as file:
    converted_data = convert_data(data)

    file.write('\n'.join(converted_data))
