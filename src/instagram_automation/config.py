"""Validated account configuration loading."""

from __future__ import annotations

from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class InstagramConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(min_length=1)
    instagram_user_id: str = Field(min_length=1)


class BrandConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    niche: str = Field(min_length=1)
    language: str = "en"
    tone: str = "educational"
    visual_style: str = "minimal"


class ContentConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    posts_per_day: int = Field(default=1, ge=1, le=10)
    formats: list[Literal["single_image", "carousel"]] = Field(
        default_factory=lambda: ["single_image", "carousel"]
    )
    carousel_min_slides: int = Field(default=4, ge=2, le=10)
    carousel_max_slides: int = Field(default=7, ge=2, le=10)

    @field_validator("formats")
    @classmethod
    def formats_must_not_be_empty(
        cls, value: list[Literal["single_image", "carousel"]]
    ) -> list[Literal["single_image", "carousel"]]:
        if not value:
            raise ValueError("at least one content format must be enabled")
        if len(set(value)) != len(value):
            raise ValueError("content formats must be unique")
        return value

    @model_validator(mode="after")
    def carousel_range_must_be_ordered(self) -> ContentConfig:
        if self.carousel_min_slides > self.carousel_max_slides:
            raise ValueError("carousel_min_slides cannot exceed carousel_max_slides")
        return self


class ScheduleConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timezone: str = "Asia/Kolkata"
    publish_times: list[str] = Field(default_factory=lambda: ["10:30"])

    @field_validator("timezone")
    @classmethod
    def timezone_must_exist(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError(f"unknown IANA timezone: {value}") from exc
        return value

    @field_validator("publish_times")
    @classmethod
    def publish_times_must_be_valid(cls, values: list[str]) -> list[str]:
        if not values:
            raise ValueError("at least one publish time is required")
        for value in values:
            try:
                hour, minute = value.split(":")
                if len(hour) != 2 or len(minute) != 2:
                    raise ValueError
                if not (0 <= int(hour) <= 23 and 0 <= int(minute) <= 59):
                    raise ValueError
            except (ValueError, TypeError) as exc:
                raise ValueError(f"invalid publish time {value!r}; expected HH:MM") from exc
        if len(set(values)) != len(values):
            raise ValueError("publish times must be unique")
        return values


class ApprovalConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    required: bool = True


class AccountConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    account_id: str = Field(pattern=r"^[a-zA-Z0-9_-]+$")
    enabled: bool = True
    instagram: InstagramConfig
    brand: BrandConfig
    content: ContentConfig = Field(default_factory=ContentConfig)
    schedule: ScheduleConfig = Field(default_factory=ScheduleConfig)
    approval: ApprovalConfig = Field(default_factory=ApprovalConfig)


def load_account_config(path: str | Path) -> AccountConfig:
    """Load one YAML account file and validate its complete schema."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as file:
        raw = yaml.safe_load(file)
    if not isinstance(raw, dict):
        raise ValueError(f"account config must contain a YAML mapping: {config_path}")
    return AccountConfig.model_validate(raw)
