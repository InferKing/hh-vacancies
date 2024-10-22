from utils.enums import Currency, Experience


class User:
    def __init__(self, experience: Experience, currency: Currency, pay_from: int, pay_to: int) -> None:
        self.experience = experience
        self.currency = currency
        self.pay_from = pay_from
        self.pay_to = pay_to