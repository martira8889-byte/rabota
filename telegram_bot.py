#!/usr/bin/env python3
"""Private Telegram bot: answers only TELEGRAM_ALLOWED_USER_ID. Silent to everyone else."""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_env() -> None:
    path = ROOT / ".env"
    if not path.exists():
        sys.exit("Missing .env")
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def api(token: str, method: str, data: dict | None = None) -> dict:
    url = f"https://api.telegram.org/bot{token}/{method}"
    body = urllib.parse.urlencode(data or {}).encode()
    req = urllib.request.Request(url, data=body)
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        raise SystemExit(f"Telegram HTTP {e.code}") from e


def main() -> None:
    load_env()
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    allowed_raw = os.environ.get("TELEGRAM_ALLOWED_USER_ID", "").strip()
    if not token:
        sys.exit("No token")
    if not allowed_raw.lstrip("-").isdigit():
        sys.exit("Set TELEGRAM_ALLOWED_USER_ID after you send /start to the bot")

    allowed_id = int(allowed_raw)
    offset = 0
    print("private bot listening", flush=True)
    while True:
        payload = api(
            token,
            "getUpdates",
            {"timeout": "25", "offset": str(offset), "allowed_updates": json.dumps(["message"])},
        )
        for upd in payload.get("result", []):
            offset = max(offset, int(upd["update_id"]) + 1)
            msg = upd.get("message") or {}
            chat = msg.get("chat") or {}
            frm = msg.get("from") or {}
            uid = int(frm.get("id") or 0)
            cid = chat.get("id")
            if cid is None:
                continue
            if chat.get("type") != "private" or uid != allowed_id:
                continue
            text = (msg.get("text") or "").strip()
            if text in ("/start", "/help"):
                out = (
                    "Бот только для вас. Чужие сообщения бот не отвечает.\n\n"
                    "Сюда приходят пачки вакансий. В Cursor пишите: да D02 D13."
                )
            elif text in ("/id", "id"):
                out = f"id {uid} — это единственный аккаунт, которому бот отвечает."
            else:
                out = "Принял. Новую пачку вакансий запросите в чате Cursor: «пачка EU»."
            api(
                token,
                "sendMessage",
                {"chat_id": str(cid), "text": out, "disable_web_page_preview": "true"},
            )
        time.sleep(0.3)


if __name__ == "__main__":
    main()
