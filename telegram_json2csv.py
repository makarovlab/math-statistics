# Example: python3 telegram_json2csv.py -f ./datasets/newdvatch.json

import pandas as pd
import sys

def check_dict_type(dictionary: dict):
    if type(dictionary) == dict and dictionary.get('type', None) == 'text':
        return dictionary['text']
    else:
        return ""

def parse_text(message_list: str | list):
    output = []

    if type(message_list) == str:
        return message_list

    else:
        for msg in message_list:
            if type(msg) == dict:
                output.append(check_dict_type(msg))
            elif type(msg) == str:
                output.append(msg)
        
        return " ".join(output)
    
def main():
    flag, filepath = sys.argv[1:]

    if flag == '-f' and filepath != None:
        df = pd.read_json(filepath)
        df['messages'] = df['messages'].apply(lambda x: parse_text(x['text']))
        df.to_csv("./datasets/example.csv")

if __name__ == "__main__":
    main()