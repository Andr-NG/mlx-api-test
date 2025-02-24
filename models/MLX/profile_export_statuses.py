# coding: utf-8

"""
    Multilogin X Launcher API

    Launcher API is used to work with profiles in the browser (start, stop, get statuses).

    The version of the OpenAPI document: 1.0.0
    Contact: support@multilogin.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List
from models.MLX.profile_export_status import ProfileExportStatus
from typing import Optional, Set
from typing_extensions import Self

class ProfileExportStatuses(BaseModel):
    """
    ProfileExportStatuses
    """ # noqa: E501
    statuses: List[ProfileExportStatus] = Field(description="A list of statuses for multiple profile exports.")
    __properties: ClassVar[List[str]] = ["statuses"]

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
        """Create an instance of ProfileExportStatuses from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in statuses (list)
        _items = []
        if self.statuses:
            for _item_statuses in self.statuses:
                if _item_statuses:
                    _items.append(_item_statuses.to_dict())
            _dict['statuses'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ProfileExportStatuses from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "statuses": [ProfileExportStatus.from_dict(_item) for _item in obj["statuses"]] if obj.get("statuses") is not None else None
        })
        return _obj


