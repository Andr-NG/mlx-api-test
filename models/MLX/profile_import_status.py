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

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class ProfileImportStatus(BaseModel):
    """
    ProfileImportStatus
    """ # noqa: E501
    import_id: StrictStr = Field(description="A unique identifier for the import process. This ID is used to track the status and details of the import. The import ID is typically generated at the start of the import process. ")
    export_id: StrictStr = Field(description="A unique identifier for the export process. This ID is used to track the status and details of the export. The export ID is typically generated at the start of the export process. ")
    new_profile_id: Optional[StrictStr] = Field(default=None, description="The unique identifier for the newly created profile after the import process is completed successfully. This field remains empty until the import is complete. ")
    status: StrictStr = Field(description="The current status of the import process. Possible values include: - \"running\": The import process is currently in progress. - \"done\": The import process has completed successfully. - \"failed\": The import process encountered an error and did not complete successfully. ")
    timestamp: StrictInt = Field(description="The timestamp indicating when the status of the import process was last updated. This field helps in tracking the exact time of status changes. ")
    message: StrictStr = Field(description="Providing additional information about the import process. If the status is \"failed\", this field contains details about the error encountered. ")
    import_path: StrictStr = Field(description="The location or path where the archive file (containing the profile to be imported) is stored before it is processed")
    extracted_path: Optional[StrictStr] = Field(default=None, description="The location or path where the contents of profile data are extracted during the import process.")
    __properties: ClassVar[List[str]] = ["import_id", "export_id", "new_profile_id", "status", "timestamp", "message", "import_path", "extracted_path"]

    @field_validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['running', 'done', 'failed']):
            raise ValueError("must be one of enum values ('running', 'done', 'failed')")
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
        """Create an instance of ProfileImportStatus from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ProfileImportStatus from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "import_id": obj.get("import_id"),
            "export_id": obj.get("export_id"),
            "new_profile_id": obj.get("new_profile_id"),
            "status": obj.get("status"),
            "timestamp": obj.get("timestamp"),
            "message": obj.get("message"),
            "import_path": obj.get("import_path"),
            "extracted_path": obj.get("extracted_path")
        })
        return _obj


