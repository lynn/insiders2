import os


def decrypt(enc: bytes, MAGIC_DX=0x4B5A, decompression_start=0):
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


def encrypt(enc: bytes, MAGIC_DX=0x4B5A, decompression_start=0):
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

