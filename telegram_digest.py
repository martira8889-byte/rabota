#!/usr/bin/env python3
"""Send a digest to ILia via Telegram. Token lives in .env — never commit it."""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_env() -> None:
    path = ROOT / ".env"
    if not path.exists():
        sys.exit("Create .env from .env.example and put TELEGRAM_BOT_TOKEN there. Do not paste the token into git.")
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def api(token: str, method: str, data: dict) -> dict:
    url = f"https://api.telegram.org/bot{token}/{method}"
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def main() -> None:
    load_env()
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        sys.exit("TELEGRAM_BOT_TOKEN is empty")

    if len(sys.argv) > 1 and sys.argv[1] == "--whoami":
        me = api(token, "getMe", {})
        print(me.get("result", {}).get("username", me))
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--chat-id":
        updates = api(token, "getUpdates", {"timeout": "0"})
        chats = []
        for u in updates.get("result", []):
            msg = u.get("message") or u.get("edited_message") or {}
            chat = msg.get("chat") or {}
            if chat.get("id"):
                chats.append(f"{chat['id']}\t{chat.get('username') or chat.get('first_name')}")
        if not chats:
            print("Write /start to the bot in Telegram, then run: python3 telegram_digest.py --chat-id")
            return
        print("\n".join(dict.fromkeys(chats)))
        return

    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    allowed = os.environ.get("TELEGRAM_ALLOWED_USER_ID", "").strip()
    if allowed and chat_id != allowed:
        sys.exit("Refuse: TELEGRAM_CHAT_ID must equal TELEGRAM_ALLOWED_USER_ID (private, owner only)")
    if not chat_id:
        sys.exit("Set TELEGRAM_CHAT_ID in .env after: python3 telegram_digest.py --chat-id")

    text = " ".join(sys.argv[1:]).strip()
    if not text and not sys.stdin.isatty():
        text = sys.stdin.read().strip()
    if not text:
        sys.exit("Pass message as args or pipe stdin")

    out = api(token, "sendMessage", {"chat_id": chat_id, "text": text, "disable_web_page_preview": "true"})
    if not out.get("ok"):
        sys.exit(str(out))
    print("sent")


if __name__ == "__main__":
    main()
