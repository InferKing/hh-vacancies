import requests
import pandas as pd
from numpy import nan


class HHParser:
    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__url_by_id = self.__base_url + "/{id}"

        self.__raw_json = None
        self.__df = None

    @property
    def dataframe(self) -> pd.DataFrame:
        return self.__df


    @property
    def grid_fields(self) -> list[dict]:
        return [{"field": field} for field in self.dataframe.columns]


    def make_request_all(self, **kwargs) -> pd.DataFrame:
        kwargs["per_page"] = 100
        max_pages = kwargs.get("max_pages", 10)

        try:
            for page in range(max_pages):
                kwargs["page"] = page
                response = requests.get(self.__base_url, params=kwargs)
            self.__raw_json = response.json()
            self.__df = pd.concat([self.__df, self.__make_df()], axis=0, ignore_index=True)
        except requests.HTTPError as e:
            print(e)

        return self.__df


    def make_request_by_id(self, id: str) -> pd.DataFrame:
        response = requests.get(self.__url_by_id.format(id=id))
        self.__raw_json = response.json()

        picked_row = self.__find_row_by_id(id).reset_index(drop=True)
        picked_data = self.__make_df(by_id=True)
        d = pd.concat([picked_data, picked_row], axis=1)
        return d
    
    def __find_row_by_id(self, id: str) -> pd.DataFrame:
        return self.dataframe[self.dataframe["ID"] == id]


    def __make_df(self, by_id: bool = False) -> pd.DataFrame: 
        json_data = self.__raw_json.get("items", self.__raw_json)
        df = pd.DataFrame()

        if by_id:
            df["Описание"] = [json_data["description"]]
            data = ""

            if json_data.get("key_skills"):
                for skill in json_data["key_skills"]:
                    data += skill["name"] + ", "

                data = data[:-2]
                df["Навыки"] = [data]
            else:
                df["Навыки"] = "Не указано"

            return df

        simple_columns = {
            "id": "ID",
            "name": "Название вакансии",
            "published_at": "Дата публикации",
            "alternate_url": "Ссылка"
        }

        separate_columns = {
            "area": {"name": "Регион"},
            "salary": {
                "from": "Зарплата от",
                "to": "Зарплата до",
                "currency": "Валюта"
            },
            "employer": {"name": "Компания"},
            "schedule": {"name": "График работы"},
            "experience": {"name": "Опыт работы"},
            "employment": {"name": "Тип занятости"}
        }

        for key, value in simple_columns.items():
            df[value] = [item.get(key, "Не указано") for item in json_data]

        for field, columns in separate_columns.items():
            for key, value in columns.items():
                df[value] = [
                    item.get(field, {}).get(key, "Не указано") if item.get(field) is not None else "Не указано"
                    for item in json_data
                ]
        df["Зарплата от"] = df["Зарплата от"].replace({None: nan})
        df["Зарплата до"] = df["Зарплата до"].replace({None: nan})

        return df
