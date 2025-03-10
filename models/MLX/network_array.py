# coding: utf-8

"""
    Multilogin X Profile Management

    Multilogin X Profile Management API allows you to manage profiles.

    The version of the OpenAPI document: 1.0.0
    Contact: support@multilogin.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictInt
from typing import Any, ClassVar, Dict, List
from typing_extensions import Annotated
from models.MLX.network import Network
from typing import Optional, Set
from typing_extensions import Self

class NetworkArray(BaseModel):
    """
    NetworkArray
    """ # noqa: E501
    total_count: StrictInt
    networks: Annotated[List[Network], Field(min_length=1, max_length=100)]
    __properties: ClassVar[List[str]] = ["total_count", "networks"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of NetworkArray from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in networks (list)
        _items = []
        if self.networks:
            for _item_networks in self.networks:
                if _item_networks:
                    _items.append(_item_networks.to_dict())
            _dict['networks'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of NetworkArray from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "total_count": obj.get("total_count"),
            "networks": [Network.from_dict(_item) for _item in obj["networks"]] if obj.get("networks") is not None else None
        })
        return _obj


