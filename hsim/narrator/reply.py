"""Parse the narrator's reply and turn its engine block into a command."""
from __future__ import annotations

import hashlib
import re

import yaml

BLOCK = re.compile(r"```(?:engine|yaml)\s*\n(.*?)```", re.S)


class ReplyError(ValueError):
    pass


def extract(text: str) -> dict:
    """Find the last engine block in a narrator reply."""
    blocks = [b for b in BLOCK.findall(text) if "reply_to" in b]
    if not blocks:
        raise ReplyError("No ```engine block with 'reply_to' found in the reply.")
    try:
        data = yaml.safe_load(blocks[-1]) or {}
    except yaml.YAMLError as e:
        raise ReplyError(f"Engine block is not valid YAML: {e}") from e
    if not isinstance(data, dict):
        raise ReplyError("Engine block must be a mapping.")
    data.setdefault("decisions", [])
    data.setdefault("proposals", [])
    data.setdefault("notes", [])
    for k in ("decisions", "proposals", "notes"):
        if data[k] is None:
            data[k] = []
        if not isinstance(data[k], list):
            raise ReplyError(f"'{k}' must be a list.")
    return data


def block_hash(data: dict) -> str:
    import json
    return hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()[:16]
