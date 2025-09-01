import json
import xmltodict


def parse_xml_to_dict(xml_file):
    with open(xml_file, 'rb') as f:
        file_name = f'{xml_file}'.split('/')[-1].split('.')[0]
        data_dict = xmltodict.parse(f.read())
        json_data = json.dumps(data_dict)
        with open(f'./data/{file_name}.json', "w") as json_file:
            json_file.write(json_data)