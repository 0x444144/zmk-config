#!/usr/bin/env python3
"""Compare a built .uf2 against the bootloader's CURRENT.UF2 readback.

CURRENT.UF2 dumps the whole application flash region, so it is larger and
padded. A match means every block of the built image is present at the same
address with identical payload bytes.
"""
import sys

BLOCK, MAGIC0, MAGIC1, MAGIC_END = 512, 0x0A324655, 0x9E5D5157, 0x0AB16F30


def blocks(path):
    """address -> payload bytes, for each valid UF2 block."""
    out = {}
    with open(path, "rb") as f:
        data = f.read()
    if len(data) % BLOCK:
        raise SystemExit(f"{path}: not a whole number of UF2 blocks")
    for i in range(0, len(data), BLOCK):
        b = data[i:i + BLOCK]
        m0 = int.from_bytes(b[0:4], "little")
        m1 = int.from_bytes(b[4:8], "little")
        me = int.from_bytes(b[508:512], "little")
        if (m0, m1, me) != (MAGIC0, MAGIC1, MAGIC_END):
            raise SystemExit(f"{path}: bad UF2 magic in block {i // BLOCK}")
        addr = int.from_bytes(b[12:16], "little")
        size = int.from_bytes(b[16:20], "little")
        out[addr] = b[32:32 + size]
    return out


def main():
    built, current = sys.argv[1], sys.argv[2]
    a, b = blocks(built), blocks(current)
    missing = [ad for ad in a if ad not in b]
    differing = [ad for ad in a if ad in b and a[ad] != b[ad]]

    print(f"built   {built}: {len(a)} blocks")
    print(f"on-board {current}: {len(b)} blocks")

    if not missing and not differing:
        print("\nMATCH -- the board is running this exact build")
        return 0
    print(f"\nMISMATCH -- {len(missing)} block(s) absent, "
          f"{len(differing)} block(s) differ")
    for ad in sorted(differing)[:3]:
        print(f"  first difference at 0x{ad:08x}")
        break
    return 1


if __name__ == "__main__":
    sys.exit(main())
