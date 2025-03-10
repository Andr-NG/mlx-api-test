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

from pydantic import BaseModel, ConfigDict, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Set
from models.MLX.profile_meta_core import ProfileMetaCore
from models.MLX.proxy import Proxy
from typing_extensions import Self

class ReadyProfileCore(BaseModel):
    """
    ReadyProfileCore
    """ # noqa: E501
    browser: ProfileMetaCore
    proxy: Optional[Proxy] = None
    browser_version: Optional[StrictStr] = None
    abort_start_if_proxy_leaks: Optional[StrictBool] = None
    timezone_fill_based_on_external_ip: Optional[StrictBool] = None
    geolocation_fill_based_on_external_ip: Optional[StrictBool] = None
    auto_update_core: StrictBool
    __properties: ClassVar[List[str]] = ["browser", "proxy", "browser_version", "abort_start_if_proxy_leaks", "timezone_fill_based_on_external_ip", "geolocation_fill_based_on_external_ip", "auto_update_core"]

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
        """Create an instance of ReadyProfileCore from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of browser
        if self.browser:
            _dict['browser'] = self.browser.to_dict()
        # override the default output from pydantic by calling `to_dict()` of proxy
        if self.proxy:
            _dict['proxy'] = self.proxy.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ReadyProfileCore from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "browser": ProfileMetaCore.from_dict(obj["browser"]) if obj.get("browser") is not None else None,
            "proxy": Proxy.from_dict(obj["proxy"]) if obj.get("proxy") is not None else None,
            "browser_version": obj.get("browser_version"),
            "abort_start_if_proxy_leaks": obj.get("abort_start_if_proxy_leaks"),
            "timezone_fill_based_on_external_ip": obj.get("timezone_fill_based_on_external_ip"),
            "geolocation_fill_based_on_external_ip": obj.get("geolocation_fill_based_on_external_ip"),
            "auto_update_core": obj.get("auto_update_core")
        })
        return _obj


