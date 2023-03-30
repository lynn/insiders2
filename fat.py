# files start at 0x13010
# COMMAND.COM: len 0xd6cc, sector 0xd0 → 0x2e810 = 0xdc * 512 + 0x13010

from dataclasses import dataclass
from decode import decode, encode
from dump import dump, reinsert


@dataclass
class Entry:
    index: int
    name: str
    start: int
    end: int
    data: bytes


if __name__ == "__main__":
    with open("Insiders - Network no Bouken - Eve ga Inai.nfd", "rb") as f:
        rom = bytearray(f.read())

    fs = {}
    START = 0x13010
    for i in range(50):
        header = rom[START + 32 * i : START + 32 * i + 32]
        name = bytes(header[:8]).decode().strip()
        sector = int.from_bytes(header[26:28], byteorder="little")
        length = int.from_bytes(header[28:32], byteorder="little")
        start = (sector + 0xC) * 512 + START
        end = start + length
        fs[name] = Entry(i, name, start, end, rom[start:end])

    # fs["D1"].data = bytearray(decode(fs["D1"].data))
    # fs["D1"].data[0x4000:0x4010] = b"im a cool hacker"
    # fs["D1"].data = encode(fs["D1"].data)
    # dump(fs)
    reinsert(fs)

    for entry in fs.values():
        assert len(entry.data) == entry.end - entry.start
        rom[entry.start : entry.end] = entry.data

    with open("patched.nfd", "wb") as f:
        f.write(rom)
