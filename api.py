import requests
import pandas as pd
from numpy import nan
from datetime import datetime


class HHParser:
    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__url_by_id = self.__base_url + "/{id}"
        self.__raw_json = None


    def make_request_all(self, **kwargs) -> pd.DataFrame:
        kwargs["per_page"] = 100
        max_pages = kwargs.get("max_pages", 10)
        df = pd.DataFrame()

        try:
            for page in range(max_pages):
                kwargs["page"] = page
                response = requests.get(self.__base_url, params=kwargs)
                self.__raw_json = response.json()
                df = pd.concat([df, self.__make_df()], axis=0, ignore_index=True)
        except requests.HTTPError as e:
            print(e)

        return df


    def make_request_by_id(self, id: str) -> pd.DataFrame:
        response = requests.get(self.__url_by_id.format(id=id))
        self.__raw_json = response.json()

        picked_data = self.__make_df(by_id=True)
        return picked_data


    def __make_df(self, by_id: bool = False) -> pd.DataFrame: 
        json_data = self.__raw_json.get("items", [self.__raw_json])
        df = pd.DataFrame()

        if by_id:
            df["Описание"] = [json_data[0]["description"]]
            data = ""
            key_skills = json_data[0].get("key_skills")

            if key_skills:
                for skill in key_skills:
                    data += skill["name"] + ", "

                data = data[:-2]
                df["Навыки"] = [data]
            else:
                df["Навыки"] = "Не указано"

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
                    item.get(field, {}).get(key, nan) if item.get(field) is not None else nan
                    for item in json_data
                ]

        df["Зарплата от"] = df["Зарплата от"].replace({None: nan})
        df["Зарплата до"] = df["Зарплата до"].replace({None: nan})

        df["Дата публикации"] = df["Дата публикации"].apply(lambda x: datetime.fromisoformat(x[:-5]).strftime("%Y-%m-%d"))
        df["Зарплата от"] = df["Зарплата от"].astype(float)
        df["Зарплата до"] = df["Зарплата до"].astype(float)

        return df
