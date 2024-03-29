import json
import yaml
import os
import re


def wrap_text(text: str, ctx, max_width: int = 300) -> str:
    result = []
    x = 0
    for token in re.findall("[A-Za-z0-9'-,.!?]+|.", text):
        if token == "\r":
            result.append("\r")
            x = 0
        elif token == " ":
            result.append(" ")
            x += ctx.font_widths[32] + 1
        else:
            width = sum(ctx.font_widths[ord(c)] + 1 for c in token)
            if x + width > max_width:
                if result[-1:] == [" "]:
                    result.pop()
                result.append("\r")
                x = 0
            result.append(token)
            x += width
    return "".join(result)


def process(text: str, file: str, ctx) -> str:
    if text.startswith("~"):
        if file == "D1": # scroll
            return wrap_text(text[1:], ctx, 400)
        else:
            return wrap_text(text[1:], ctx)
    else:
        return text


text_sections = [
    ("AHM", 0x7200, 0x7400, "ending"),
    ("AHM", 0x7400, 0x7500, "ngplus"),
    ("AHM", 0x7800, 0x7900, "magicterm"),
    ("AHM", 0x7900, 0x7B00, "autodial"),
    ("AHM", 0x8000, 0x9800, "tutorial"),
    ("AS", 0x8000, 0xA000, "game_as"),
    ("BHM", 0x8000, 0x9800, "game_bhm"),
    ("CHM", 0x8000, 0x9800, "game_chm"),
    ("D1", 0x4000, 0x5000, "scroll"),
    ("DHM", 0x8000, 0x8C00, "game_dhm"),
    ("DK", 0x8000, 0x9000, "game_dk"),
    ("DR", 0x6000, 0x6300, "credits"),
    ("DR", 0x7800, 0x7D80, "game_dr1"),
    ("DR", 0x8000, 0x9800, "game_dr2"),
    ("EG", 0x7300, 0x7500, "game_eg1"),
    ("EG", 0x8000, 0xA000, "game_eg2"),
    ("EG", 0x8000, 0xA000, "game_eg2"),
    ("GG", 0x7800, 0x7980, "the_end"),
    ("GG", 0x8000, 0x9000, "game_gg"),
    ("LN", 0x8000, 0x9000, "game_ln"),
    ("MZ", 0x8000, 0x8C00, "game_mz"),
    ("NT", 0x7A00, 0x8000, "game_nt1"),
    ("NT", 0x8000, 0x9000, "game_nt2"),
    ("PL", 0x7800, 0x8000, "game_pl1"),
    ("PL", 0x8000, 0x8C00, "game_pl2"),
    ("S2", 0x2, 0x1000, "terms"),
    ("S2", 0x1800, 0x2000, "items"),
    ("S2", 0x2000, 0x3000, "common"),
    ("S2", 0x3000, 0x4000, "battle"),
    ("S3", 0xC000, 0xE800, "s3"),
    ("SF", 0x7800, 0x7E00, "game_sf1"),
    ("SF", 0x8000, 0x9400, "game_sf2"),
]


def dump(ctx):
    def junk(text: str) -> bool:
        return all(c in "U裹" for c in text)

    for file, start, end, name in text_sections:
        buf = ctx.fs[file].data
        text = buf[start:end].decode("cp932")
        texts = text.split("\0")
        while junk(texts[-1]):
            texts.pop()
        lines = ["[\n"]
        for i, t in enumerate(texts):
            tr = json.dumps(t, ensure_ascii=False)
            if i > 0:
                lines.append("\n")
            lines.append(f"    # {i:02x} = {tr}\n")
            lines.append(f"    {tr},\n")
        lines.append("]\n")
        fn = f"text/{name}.yaml"
        if os.path.isfile(fn):
            print(f"{fn} exists, not overwriting")
            continue
        with open(fn, "w") as f:
            f.writelines(lines)
        # print(texts)


def reinsert(ctx):
    for file, start, end, name in text_sections:
        with open(f"text/{name}.yaml") as f:
            texts = yaml.safe_load(f)
        texts = [process(t, file, ctx) for t in texts]
        buf = bytearray(ctx.fs[file].data)
        tl = "\0".join(texts).encode("cp932")
        max_len = end - start
        if len(tl) <= max_len:
            print(f"[{name:9}] \x1b[32mOK\x1b[0m {len(tl):5} ≤ {max_len:5}")
            buf[start : start + len(tl)] = tl
            ctx.fs[file].data = buf
        else:
            raise ValueError(f"{name} TL too long")
