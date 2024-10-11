class BaseConfig:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 8055
        self.debug = True
    
    def to_dict(self):
        return self.__dict__


class ProductionConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.host = "0.0.0.0"
        self.port = 8055
        self.debug = False


class DevelopmentConfig(BaseConfig):
    def __init__(self):
        super().__init__()
    