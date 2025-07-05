from datetime import datetime, timedelta
from decimal import Decimal
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict


# Model config
class ResourceModel(BaseModel):
    """
    Base Pydantic model used for validating and parsing API parameters
    """
    model_config: ClassVar[ConfigDict] = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True
    )


class QueryModel(BaseModel):
    """
    Base Pydantic model used for querying/filtering on database tables
    """
    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True
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


class MappingModel(BaseModel):
    """
    Base Pydantic model used for mapping model attributes
    """
    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True
    )