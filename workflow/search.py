#!/usr/bin/env python3
"""Alfred Script Filter for Affiliate Links.txt.

Return copies the whole product line: emoji, name, and link.
Command-Return copies the URL alone.
Option-Return copies the UK line when the entry has one.
Control-Return copies a promo note.
"""

import json
import os
import re
import sys
import unicodedata
from pathlib import Path

DEFAULT_LINKS = "~/Google Drive (Home)/Grok Ops/YouTube/Affiliate Links.txt"

PRODUCT_RE = re.compile(r"^(?P<label>.+?):\s*(?P<rest>https?://\S.*)$")
REGION_RE = re.compile(
    r"^(?P<name>[A-Za-z][A-Za-z0-9 +/().-]{0,24}):\s*(?P<url>https?://\S+)$"
)
ALT_RE = re.compile(r"^alts?:\s*(.*)$", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s|]+")
FOLD_MAP = str.maketrans(
    {
        "ø": "o",
        "æ": "ae",
        "ł": "l",
        "đ": "d",
        "ß": "ss",
    }
)


def fold(text):
    text = text.lower().translate(FOLD_MAP)
    text = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def clean_url(url):
    return url.rstrip(".,);]>\"'")


def links_path():
    raw = os.environ.get("links_file", "").strip() or DEFAULT_LINKS
    return Path(raw).expanduser()


def split_links(rest):
    parts = [part.strip() for part in rest.split("|") if part.strip()]
    if not parts or not parts[0].startswith("http"):
        return None
    primary = clean_url(parts[0])
    regions = []
    for part in parts[1:]:
        match = REGION_RE.match(part)
        if match:
            regions.append((match.group("name").strip(), clean_url(match.group("url"))))
            continue
        regions.extend(("Alt", clean_url(url)) for url in URL_RE.findall(part))
    return primary, regions


def classify_note(note):
    match = ALT_RE.match(note)
    if match:
        return "alts", [clean_url(url) for url in URL_RE.findall(match.group(1))]
    if note.lower().startswith("promo:"):
        return "promo", note
    return "note", note


def parse(text):
    products = []
    notes = []
    section = ""
    current = None

    for index, raw in enumerate(text.splitlines()):
        if not raw.strip():
            current = None
            continue
        if raw.startswith("#"):
            section = raw.lstrip("#").strip()
            current = None
            continue
        if raw[0] in " \t":
            if current is None:
                continue
            kind, payload = classify_note(raw.strip())
            if kind == "alts":
                current["alts"].extend(payload)
            elif kind == "promo":
                current["promos"].append(payload)
            else:
                current["notes"].append(payload)
            continue

        stripped = raw.strip()
        if stripped.startswith("- "):
            notes.append(
                {"text": stripped[2:].strip(), "section": section, "index": index}
            )
            current = None
            continue

        match = PRODUCT_RE.match(stripped)
        parsed = split_links(match.group("rest")) if match else None
        if parsed is None:
            urls = [clean_url(url) for url in URL_RE.findall(stripped)]
            if not urls:
                current = None
                continue
            label = stripped
            primary, regions = urls[0], [("Alt", url) for url in urls[1:]]
        else:
            label = match.group("label").strip()
            primary, regions = parsed

        current = {
            "label": label,
            "section": section,
            "primary": primary,
            "regions": regions,
            "alts": [],
            "promos": [],
            "notes": [],
            "line": stripped,
            "index": index,
        }
        products.append(current)

    return products, notes


def product_hay(product):
    parts = [
        product["label"],
        product["section"],
        product["line"],
        product["primary"],
    ]
    parts.extend(name + " " + url for name, url in product["regions"])
    parts.extend(product["alts"])
    parts.extend(product["promos"])
    parts.extend(product["notes"])
    return fold(" ".join(parts))


def match_strength(hay, tokens):
    if all(token in hay for token in tokens):
        return 2
    squashed = "".join(tokens)
    if len(squashed) >= 3 and squashed in hay.replace(" ", ""):
        return 1
    return 0


def rank(name, tokens, strength):
    phrase = " ".join(tokens)
    words = re.findall(r"[a-z0-9]+", name)
    return (
        strength,
        1 if phrase and phrase in name else 0,
        sum(token in name for token in tokens),
        1 if tokens and any(word.startswith(tokens[0]) for word in words) else 0,
    )


def item(
    *,
    title,
    url,
    subtitle,
    paste_line,
    uid,
    promo_arg="",
    region=None,
):
    result = {
        "uid": uid,
        "title": title,
        "subtitle": subtitle,
        "arg": paste_line,
        "valid": True,
        "text": {"copy": paste_line, "largetype": paste_line},
        "quicklookurl": url,
        "mods": {
            "cmd": {
                "valid": True,
                "arg": url,
                "subtitle": "Copy URL only · " + url,
            }
        },
    }
    if region is not None:
        name, region_line = region
        result["mods"]["alt"] = {
            "valid": True,
            "arg": region_line,
            "subtitle": "Copy " + name + " line · " + region_line,
        }
    if promo_arg:
        result["mods"]["ctrl"] = {
            "valid": True,
            "arg": promo_arg,
            "subtitle": "Copy promo · " + promo_arg.replace("\n", " · "),
        }
    return result


def subtitle_for(url, section, hints, promos, notes):
    parts = [url]
    if section:
        parts.append(section)
    parts.extend(hints)
    parts.extend(promos)
    parts.extend(notes)
    return " · ".join(parts)


def build_items(products, notes, query):
    tokens = [token for token in fold(query).split() if token]
    rows = []

    for product in products:
        hay = product_hay(product)
        name = fold(product["label"])
        strength = match_strength(hay, tokens) if tokens else 2
        if tokens and not strength:
            continue
        score = rank(name, tokens, strength) if tokens else (0,)
        promo_arg = "\n".join(product["promos"])
        first_region = product["regions"][0] if product["regions"] else None
        region_copy = None
        if first_region is not None:
            region_copy = (
                first_region[0],
                "{0}: {1}".format(product["label"], first_region[1]),
            )
        hints = ["⌘ URL only"]
        if region_copy is not None:
            hints.append("⌥ " + region_copy[0])
        if promo_arg:
            hints.append("⌃ promo")

        rows.append(
            (
                score,
                product["index"],
                0,
                item(
                    title=product["label"],
                    url=product["primary"],
                    subtitle=subtitle_for(
                        product["primary"],
                        product["section"],
                        hints,
                        product["promos"],
                        product["notes"],
                    ),
                    paste_line=product["line"],
                    uid="aff:{0}:{1}:primary".format(product["index"], product["primary"]),
                    promo_arg=promo_arg,
                    region=region_copy,
                ),
            )
        )

        for offset, (region_name, region_url) in enumerate(product["regions"], start=1):
            rows.append(
                (
                    score,
                    product["index"],
                    offset,
                    item(
                        title="{0} ({1})".format(product["label"], region_name),
                        url=region_url,
                        subtitle=subtitle_for(
                            region_url,
                            product["section"],
                            [region_name, "⌘ URL only"]
                            + (["⌃ promo"] if promo_arg else []),
                            product["promos"],
                            product["notes"],
                        ),
                        paste_line="{0}: {1}".format(product["label"], region_url),
                        uid="aff:{0}:{1}:{2}".format(
                            product["index"], region_name, region_url
                        ),
                        promo_arg=promo_arg,
                    ),
                )
            )

        for offset, alt_url in enumerate(product["alts"], start=1):
            alt_paste = "{0}: {1}".format(product["label"], alt_url)
            rows.append(
                (
                    score,
                    product["index"],
                    100 + offset,
                    item(
                        title="{0} (alt)".format(product["label"]),
                        url=alt_url,
                        subtitle=subtitle_for(
                            alt_url,
                            product["section"],
                            ["alt", "⌘ URL only"]
                            + (["⌃ promo"] if promo_arg else []),
                            product["promos"],
                            product["notes"],
                        ),
                        paste_line=alt_paste,
                        uid="aff:{0}:alt:{1}".format(product["index"], alt_url),
                        promo_arg=promo_arg,
                    ),
                )
            )

    rows.sort(key=lambda row: (-row[0][0], -row[0][1], -row[0][2], -row[0][3], row[1], row[2]) if tokens else (row[1], row[2]))
    items = [row[3] for row in rows]

    if tokens:
        for note in notes:
            hay = fold(note["section"] + " " + note["text"])
            if not match_strength(hay, tokens):
                continue
            items.append(
                {
                    "title": note["text"],
                    "subtitle": "Note · " + (note["section"] or "Affiliate Links.txt") + " · no link to copy",
                    "valid": False,
                    "arg": note["text"],
                }
            )

    if items:
        return items
    if tokens:
        return [
            {
                "title": "No affiliate links match",
                "subtitle": query,
                "valid": False,
            }
        ]
    return [
        {
            "title": "No affiliate links in the file",
            "subtitle": str(links_path()),
            "valid": False,
        }
    ]


def emit(items):
    json.dump({"items": items}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


def error_item(title, subtitle):
    return {"title": title, "subtitle": subtitle, "valid": False}


def main():
    query = " ".join(sys.argv[1:]).strip()
    path = links_path()
    try:
        if not path.is_file():
            emit(
                [
                    error_item(
                        "Affiliate Links.txt not found",
                        "Set the Links file in the workflow configuration · " + str(path),
                    )
                ]
            )
            return
        products, notes = parse(path.read_text(encoding="utf-8-sig"))
    except OSError as exc:
        emit([error_item("Could not read Affiliate Links.txt", str(exc))])
        return
    emit(build_items(products, notes, query))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        emit([error_item("Affiliate search failed", str(exc))])
        sys.exit(0)
