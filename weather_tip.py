"""Fetch Wuxi's tomorrow forecast and write the Dongyun guest tip."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.request import urlopen


API_URL = (
    "https://api.open-meteo.com/v1/forecast?latitude=31.58&longitude=120.46"
    "&daily=temperature_2m_max,weathercode&timezone=Asia%2FShanghai"
)
OUTPUT_PATH = Path(r"D:\东韵门面\今日提示.txt")
RAIN_CODES = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99}
SUNNY_CODES = {0, 1}


def fetch_tomorrow_weather() -> tuple[str, float, int]:
    with urlopen(API_URL, timeout=15) as response:
        forecast = json.load(response)

    daily = forecast["daily"]
    if len(daily["time"]) < 2:
        raise RuntimeError("天气接口未返回明天的预报")
    return daily["time"][1], daily["temperature_2m_max"][1], daily["weathercode"][1]


def make_tip(forecast_date: str, maximum_temperature: float, weather_code: int) -> str:
    if weather_code in RAIN_CODES:
        message = "明日有雨，东韵提供免费停车场，室内恒温舒适，欢迎来店畅玩！"
    elif weather_code in SUNNY_CODES:
        message = "明日晴好，正适合约上亲友聚会，来东韵畅享棋牌时光！"
    else:
        message = "明日天气适宜，东韵室内恒温舒适，欢迎约上亲友聚会！"

    return (
        "东韵今日提示\n"
        + "=" * 18
        + f"\n无锡明日（{forecast_date}）最高温：{maximum_temperature:g}℃\n"
        + f"{message}\n"
    )


def main() -> None:
    forecast_date, maximum_temperature, weather_code = fetch_tomorrow_weather()
    OUTPUT_PATH.write_text(
        make_tip(forecast_date, maximum_temperature, weather_code), encoding="utf-8-sig"
    )
    print(f"提示已生成：{OUTPUT_PATH}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    main()
