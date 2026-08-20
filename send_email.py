#!/usr/bin/env python3
"""Send one approved email via Gmail app password. Secrets in .env only."""
from __future__ import annotations

import os
import smtplib
import sys
from email.message import EmailMessage
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


def main() -> None:
    load_env()
    user = os.environ.get("GMAIL_ADDRESS", "").strip()
    pw = os.environ.get("GMAIL_APP_PASSWORD", "").replace(" ", "")
    if not user or not pw:
        sys.exit("Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD in .env (app password, not account password)")

    if len(sys.argv) < 4:
        sys.exit("Usage: python3 send_email.py TO SUBJECT < body.txt")

    to = sys.argv[1].strip()
    subject = sys.argv[2].strip()
    body = sys.stdin.read() if not sys.stdin.isatty() else " ".join(sys.argv[3:])
    if not body.strip():
        sys.exit("Empty body")

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
        smtp.login(user, pw)
        smtp.send_message(msg)
    print("sent")


if __name__ == "__main__":
    main()
