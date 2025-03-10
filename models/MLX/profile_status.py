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

from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from models.MLX.download_progress import DownloadProgress
from models.MLX.script_status import ScriptStatus
from typing import Optional, Set
from typing_extensions import Self

class ProfileStatus(BaseModel):
    """
    ProfileStatus
    """ # noqa: E501
    status: StrictStr
    download_progress: Optional[DownloadProgress] = None
    message: StrictStr
    timestamp: StrictInt
    script_data: Optional[ScriptStatus] = None
    port: Optional[StrictInt] = None
    __properties: ClassVar[List[str]] = ["status", "download_progress", "message", "timestamp", "script_data", "port"]

    @field_validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['download_browser_profile_metadata', 'download_browser_profile_data', 'download_browser_core', 'download_finished', 'download_meta_error', 'download_data_error', 'download_core_error', 'download_meta_finished', 'download_data_finished', 'download_core_finished', 'validate_proxy', 'validate_proxy_error', 'start_browser', 'start_browser_error', 'browser_running', 'stopped']):
            raise ValueError("must be one of enum values ('download_browser_profile_metadata', 'download_browser_profile_data', 'download_browser_core', 'download_finished', 'download_meta_error', 'download_data_error', 'download_core_error', 'download_meta_finished', 'download_data_finished', 'download_core_finished', 'validate_proxy', 'validate_proxy_error', 'start_browser', 'start_browser_error', 'browser_running', 'stopped')")
        return value

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
        """Create an instance of ProfileStatus from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of download_progress
        if self.download_progress:
            _dict['download_progress'] = self.download_progress.to_dict()
        # override the default output from pydantic by calling `to_dict()` of script_data
        if self.script_data:
            _dict['script_data'] = self.script_data.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ProfileStatus from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "status": obj.get("status"),
            "download_progress": DownloadProgress.from_dict(obj["download_progress"]) if obj.get("download_progress") is not None else None,
            "message": obj.get("message"),
            "timestamp": obj.get("timestamp"),
            "script_data": ScriptStatus.from_dict(obj["script_data"]) if obj.get("script_data") is not None else None,
            "port": obj.get("port")
        })
        return _obj


