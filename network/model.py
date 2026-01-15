from pydantic import BaseModel, ConfigDict
from .utils import to_camel

class CamelModel(BaseModel):
    """
    Base model that automatically converts snake_case fields to camelCase aliases.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
