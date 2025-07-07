from typing import ClassVar

from pydantic import BaseModel, ConfigDict


# API base model config
class ResourceModel(BaseModel):
    """
    Base Pydantic model used for validating and parsing API parameters
    """
    model_config: ClassVar[ConfigDict] = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True
    )


class ResponseModel(BaseModel):
    """
    Base Pydantic model used for validating responses
    """
    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True
    )