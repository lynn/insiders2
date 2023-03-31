import os


def decrypt(enc: bytes, dx=0x4B5A, start=0):
    bs = list(enc[:start])
    ax = 0
    for cursor in range(start, len(enc), 2):
        ax = (enc[cursor + 1] << 8) + enc[cursor]
        ax, dx = ax ^ dx, ax
        bs.append(ax & 255)
        bs.append(ax >> 8)
    return bytes(bs)


def encrypt(enc: bytes, dx=0x4B5A, start=0):
    bs = list(enc[:start])
    for cursor in range(start, len(enc), 2):
        dx ^= (enc[cursor + 1] << 8) + enc[cursor]
        bs.append(dx & 255)
        bs.append(dx >> 8)
    return bytes(bs)
