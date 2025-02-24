# coding: utf-8

"""
    Multilogin X Profile Access Management API

    Multilogin X Profile Access Management API allows you to control everything related to permissions, workspaces, team members.

    The version of the OpenAPI document: 1.0.0
    Contact: support@multilogin.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class BrowserType(str, Enum):
    """
    BrowserType
    """

    """
    allowed enum values
    """
    MIMIC = 'mimic'
    STEALTHFOX = 'stealthfox'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of BrowserType from a JSON string"""
        return cls(json.loads(json_str))


