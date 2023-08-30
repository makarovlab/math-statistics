import re
import pickle
import json
import datetime
import tiktoken
import requests
from typing import List
import logging


class AttributesClassifier():

    def __init__(self):
        self.__encoding = tiktoken.get_encoding("cl100k_base")
        # Load the model and vectorizer
        with open('model_autoparse/model.pkl', 'rb') as model_file:
            self.__model = pickle.load(model_file)
            logging.debug("Loaded model")

        with open('model_autoparse/vectorizer.pkl', 'rb') as vectorizer_file:
            self.__vectorizer = pickle.load(vectorizer_file)
            logging.debug("Loaded vectorizer")


        with open('model_autoparse/label_encoder.pkl', 'rb') as label_encoder_file:
            self.__label_encoder = pickle.load(label_encoder_file)
            logging.debug("Loaded label")


    def __replace_punctuation_with_space(self, input_string: str) -> str:
        return re.sub(r'[\.\!\-\_]', ' ', input_string)


    def tokenize(self, input_string: str) -> List[str]:
        no_symbols = self.__replace_punctuation_with_space(
            input_string).lower()
        no_symbols = no_symbols.replace(" ", "")
        tokens = self.__encoding.encode(no_symbols)

        return [self.__encoding.decode_single_token_bytes(token).decode("utf-8") for token in tokens]


    def predict(self, input_string: str) -> str:
        word = self.__vectorizer.transform([input_string])
        prediction = self.__model.predict(word)
        return self.__label_encoder.classes_[prediction[0]]


    def transform_dict(self, input_dict: dict) -> dict:
        def recursive_transform(data, key):
            prediction = self.predict(key)
            if isinstance(data, dict):
                transformed = {"data_type": "dict",
                               "prediction": prediction, "value": {}}
                for sub_key, value in data.items():
                    transformed["value"][sub_key] = recursive_transform(
                        value, sub_key)
                return transformed
            elif isinstance(data, list):
                transformed = {"data_type": "list",
                               "prediction": prediction, "value": []}
                for item in data:
                    transformed["value"].append(recursive_transform(item, key))
                return transformed
            else:
                return {"data_type": type(data).__name__, "prediction": prediction, "value": data}

        transformed_dict = recursive_transform(input_dict, "root")
        return transformed_dict
    

    def trasform_dict_to_file(self, input_dict: dict):
        transformed_json = self.transform_dict(input_dict)
        filestamp = str(datetime.datetime.now().timestamp()).split(".")[0]

        with open(f"transformed-{filestamp}.json", 'w') as file:
            file.writelines(json.dumps(transformed_json, indent="\t"))


    def transform_dict_from_url(self, url: str, headers:dict = {}) -> dict:
        res_json = requests.get(url, headers=headers).json()
        return self.transform_dict(res_json)