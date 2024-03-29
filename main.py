# files start at 0x13010
# COMMAND.COM: len 0xd6cc, sector 0xd0 → 0x2e810 = 0xdc * 512 + 0x13010

from dataclasses import dataclass
from typing import Dict, List
from codec import decrypt, encrypt
from dump import dump, reinsert

encrypted = {
    "AHM",
    "AS",
    "BHM",
    "CHM",
    "D1",
    "DHM",
    "DK",
    "DR",
    "EG",
    "GG",
    "LN",
    "MZ",
    "NT",
    "PL",
    "S2",
    "S3",
    "SF",
}


@dataclass
class Entry:
    index: int
    name: str
    start: int
    end: int
    data: bytes


@dataclass
class Context:
    fs: Dict[str, Entry]
    font_widths: List[int]


if __name__ == "__main__":
    # rom_name = "Insiders - Network no Bouken - Eve ga Inai.nfd"
    rom_name = "saved.nfd"
    with open(rom_name, "rb") as f:
        rom = bytearray(f.read())

    fs = {}
    START = 0x13010
    k = -1
    for i in range(50):
        header = rom[START + 32 * i : START + 32 * i + 32]
        name = bytes(header[:8]).decode().strip()
        sector = int.from_bytes(header[26:28], byteorder="little")
        length = int.from_bytes(header[28:32], byteorder="little")
        start = (sector + 0xC) * 512 + START
        end = start + length
        data = rom[start:end]
        if name == "D1":
            font_widths = data[0x1100:0x1180]
        if name in encrypted:
            data = decrypt(data)
        fs[name] = Entry(i, name, start, end, data)

    ctx = Context(fs, font_widths)
    reinsert(ctx)

    for entry in fs.values():
        assert len(entry.data) == entry.end - entry.start
        if entry.name in encrypted:
            entry.data = encrypt(entry.data)
        rom[entry.start : entry.end] = entry.data

    with open("patched.nfd", "wb") as f:
        f.write(rom)
