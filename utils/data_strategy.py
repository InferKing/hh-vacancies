from abc import ABC, abstractmethod
import json
import os


class IData(ABC):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self, data):
        pass


class JSONData(IData):
    __filename = "data.json"

    def load(self):
        if os.path.exists(self.__filename):
            with open(self.__filename, encoding="utf-8") as f:
                data = json.load(f)

            return data

        return {}                

    def save(self, data):
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(data, f)