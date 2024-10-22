import inspect


class EnumReflector:
    @staticmethod
    def reflect(obj) -> list[str]:
        return [member[1] for member in inspect.getmembers(obj) if not member[0].startswith("__") and not inspect.isfunction(member[1]) and not inspect.ismethod(member[1])]


class Currency:
    USD = "USD"
    EUR = "EUR"
    RUB = "RUR"
    UZS = "UZS"
    KZT = "KZT"


class Experience:
    INTERN = "Нет опыта"
    JUNIOR = "От 1 года до 3 лет"
    MIDDLE = "От 3 до 6 лет"
    SENIOR = "От 6 лет и более"