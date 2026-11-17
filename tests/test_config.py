from pathlib import Path

import pytest
from pydantic import ValidationError

from instagram_automation.config import AccountConfig, load_account_config


EXAMPLE = Path(__file__).parents[1] / "configs/examples/account.example.yaml"


def test_example_account_config_loads() -> None:
    config = load_account_config(EXAMPLE)
    assert config.account_id == "account_001"
    assert config.schedule.timezone == "Asia/Kolkata"
    assert config.approval.required is True


def test_unknown_fields_are_rejected() -> None:
    data = {
        "account_id": "account_001",
        "instagram": {"username": "demo", "instagram_user_id": "123"},
        "brand": {"name": "Demo", "niche": "tech"},
        "unexpected_secret": "should-not-be-accepted",
    }
    with pytest.raises(ValidationError):
        AccountConfig.model_validate(data)


def test_invalid_timezone_is_rejected() -> None:
    data = {
        "account_id": "account_001",
        "instagram": {"username": "demo", "instagram_user_id": "123"},
        "brand": {"name": "Demo", "niche": "tech"},
        "schedule": {"timezone": "Mars/Olympus"},
    }
    with pytest.raises(ValidationError):
        AccountConfig.model_validate(data)


def test_invalid_publish_time_is_rejected() -> None:
    data = {
        "account_id": "account_001",
        "instagram": {"username": "demo", "instagram_user_id": "123"},
        "brand": {"name": "Demo", "niche": "tech"},
        "schedule": {"publish_times": ["25:90"]},
    }
    with pytest.raises(ValidationError):
        AccountConfig.model_validate(data)


def test_carousel_min_cannot_exceed_max() -> None:
    data = {
        "account_id": "account_001",
        "instagram": {"username": "demo", "instagram_user_id": "123"},
        "brand": {"name": "Demo", "niche": "tech"},
        "content": {"carousel_min_slides": 8, "carousel_max_slides": 5},
    }
    with pytest.raises(ValidationError):
        AccountConfig.model_validate(data)
