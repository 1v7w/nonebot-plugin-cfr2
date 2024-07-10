from pydantic import BaseModel

class Config(BaseModel):
    access_key: str
    secret_key: str
    bucket_name: str
    region: str
    endpoint_url: str
    custom_domain: str