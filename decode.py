import os


def decode(enc: bytes, MAGIC_DX=0x4B5A, decompression_start=0):
    cursor = 0
    bs = b""
    while cursor < decompression_start:
        bs += enc[cursor].to_bytes(length=1, byteorder="little")
        cursor += 1
    cursor = decompression_start
    ax = 0
    dx = MAGIC_DX
    while cursor < len(enc):
        ax = (enc[cursor + 1] << 8) + enc[cursor]
        ax, dx = ax ^ dx, ax
        bs += ax.to_bytes(length=2, byteorder="little")
        cursor += 2
    return bs


def encode(enc: bytes, MAGIC_DX=0x4B5A, decompression_start=0):
    cursor = 0
    bs = b""
    while cursor < decompression_start:
        bs += enc[cursor].to_bytes(length=1, byteorder="little")
        cursor += 1
    cursor = decompression_start
    ax = 0
    dx = MAGIC_DX
    while cursor < len(enc):
        ax = (enc[cursor + 1] << 8) + enc[cursor]
        dx = dx ^ ax
        bs += dx.to_bytes(length=2, byteorder="little")
        cursor += 2
    return bs


if __name__ == "__main__":
    for filename in os.listdir("contents"):
        f = os.path.join("contents", filename)
        if os.path.isfile(f):
            b = open(f, "rb").read()
            d = decode(b)
            if "る".encode("shift-jis") in d:
                open(os.path.join("decoded", filename), "wb").write(d)
