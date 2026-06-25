from enum import Enum


class DisabilityMode(str, Enum):
    visual = "visual"
    hearing = "hearing"
    developmental = "developmental"
    default = "default"


# F02_S04~S07: 모드별 프론트 적용 설정 프리셋
MODE_SETTINGS: dict[str, dict] = {
    "visual": {"font_scale": 1.5, "high_contrast": True, "tts": True, "keyboard_nav": True},
    "hearing": {"captions": True, "vibration": True, "visual_alerts": True},
    "developmental": {"simplified": True, "large_icons": True, "one_item_feed": True},
    "default": {"font_scale": 1.0, "high_contrast": False},
}


def settings_for(mode: str | None, overrides: dict | None = None) -> dict:
    """모드 + 사용자별 미세조정(overrides)을 합친 최종 설정."""
    base = dict(MODE_SETTINGS.get(mode or "default", MODE_SETTINGS["default"]))
    if overrides:
        base.update(overrides)
    return base
