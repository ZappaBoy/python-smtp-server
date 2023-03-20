from models.orm_base_model import ORMBaseModel


class SMTPConfigModel(ORMBaseModel):
    host: str
    port: int
    address: str
    password: str
