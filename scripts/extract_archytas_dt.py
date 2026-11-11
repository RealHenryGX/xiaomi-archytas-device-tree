#!/usr/bin/env python3
"""Extract Archytas main DTB and DTBO from Android partition images."""

from __future__ import annotations

import argparse
import struct
import subprocess
import sys
from pathlib import Path


MAGIC = b"\xd0\x0d\xfe\xed"


def extract_boot(path: Path) -> bytes:
    data = path.read_bytes()
    kernel_size = struct.unpack_from("<I", data, 8)[0]
    kernel_region = data[2048 : 2048 + kernel_size]
    offset = kernel_region.rfind(MAGIC)
    if offset < 0:
        raise ValueError(f"no appended DTB found in {path}")
    total_size = struct.unpack_from(">I", kernel_region, offset + 4)[0]
    return kernel_region[offset : offset + total_size]


def extract_dtbo(path: Path) -> bytes:
    data = path.read_bytes()
    offset = data.find(MAGIC)
    if offset < 0:
        raise ValueError(f"no DTB found in {path}")
    total_size = struct.unpack_from(">I", data, offset + 4)[0]
    return data[offset : offset + total_size]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("boot", type=Path)
    parser.add_argument("dtbo", type=Path)
    parser.add_argument("--output", type=Path, default=Path("extracted"))
    args = parser.parse_args()

    dtb_dir = args.output / "dtb"
    dts_dir = args.output / "dts"
    dtb_dir.mkdir(parents=True, exist_ok=True)
    dts_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "archytas-main": extract_boot(args.boot),
        "archytas-dtbo": extract_dtbo(args.dtbo),
    }
    dumper = Path(__file__).with_name("dtb_dump.py")
    for name, blob in outputs.items():
        dtb_path = dtb_dir / f"{name}.dtb"
        dts_path = dts_dir / f"{name}.dts"
        dtb_path.write_bytes(blob)
        completed = subprocess.run(
            [sys.executable, str(dumper), str(dtb_path), str(dts_path)],
            check=True,
        )
        assert completed.returncode == 0
        print(f"{name}: {len(blob)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
