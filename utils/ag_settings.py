class AGColumnSettings:
    def __init__(self) -> None:
        self.__base_match_fields = [
            {"field": " ", "cellRenderer": "GetMoreInfo", "sortable": False, "width": 60, "resizable": False},
            {"field": "Название вакансии", "cellRenderer": "VacancyLink", "filter": True},
            {"field": "Дата публикации", "filter": True, "width": 150},
            {"field": "Регион", "filter": True},
            {"field": "Зарплата от", "cellDataType": "number", "filter": True, "width": 140},
            {"field": "Зарплата до", "cellDataType": "number", "filter": True, "width": 140},
            {"field": "Валюта", "filter": True, "width": 90},
            {"field": "Компания", "filter": True},
            {"field": "Опыт работы", "filter": True},
            {"field": "График работы", "filter": True},
            {"field": "Тип занятости", "filter": True}
        ]


    @property
    def grid_fields(self) -> list[dict]:
        return self.__base_match_fields
    
    
    @property
    def grid_fields_by_id(self) -> list[dict]:
        return self.__base_match_fields[1:]