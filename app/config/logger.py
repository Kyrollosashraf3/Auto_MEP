"""
Logger module for Auto MEP.
Provides centralized logging with file + console output.
Logs are stored in app/logs/app.log for the HTML viewer.
"""
import logging
import logging.handlers
import sys
import json
import os
from pathlib import Path
from datetime import datetime


LOG_DIR = Path("app/logs")
LOG_FILE = LOG_DIR / "app.log"
MAX_BYTES = 5 * 1024 * 1024  # 5MB per file
BACKUP_COUNT = 3

_loggers = {}


def get_logger(name: str) -> logging.Logger:
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if not logger.handlers:
        LOG_DIR.mkdir(parents=True, exist_ok=True)

        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        file_handler = logging.handlers.RotatingFileHandler(
            str(LOG_FILE),
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    _loggers[name] = logger
    return logger


def read_logs(level=None, search=None, limit=200):
    if not LOG_FILE.exists():
        return []

    lines = []
    for line in LOG_FILE.read_text(encoding='utf-8').strip().split('\n'):
        if not line.strip():
            continue
        parts = line.split(' | ', 3)
        if len(parts) < 4:
            continue
        entry = {
            'timestamp': parts[0].strip(),
            'level': parts[1].strip(),
            'logger': parts[2].strip(),
            'message': parts[3].strip(),
        }
        if level and entry['level'] != level.upper():
            continue
        if search and search.lower() not in line.lower():
            continue
        lines.append(entry)

    return lines[-limit:]
