# Xiaomi Archytas device tree

Device-tree sources and binary blobs extracted from the Xiaomi Archytas Wi-Fi readback backup.

## Contents

- `dtb/archytas-main.dtb` — main DTB extracted from the readback `boot.img`.
- `dtb/archytas-dtbo.dtb` — DTBO overlay extracted from the readback `dtbo.img`.
- `dts/archytas-main.dts` — decompiled main DTB.
- `dts/archytas-dtbo.dts` — decompiled DTBO overlay.
- `scripts/extract_archytas_dt.py` — reproducible extractor for `boot.img` and `dtbo.img`.
- `scripts/dtb_dump.py` — standalone DTB-to-DTS dumper with no external dependency.
- `metadata/SHA256SUMS` — hashes for the published artifacts.

## Provenance

The files were extracted from:

```text
artifacts/readback/GeekFlashTool_Readback_20261110192413681/boot.img
artifacts/readback/GeekFlashTool_Readback_20261110192413681/dtbo.img
```

The extracted blobs match the existing Archytas Wi-Fi reference blobs byte-for-byte. The main DTB is 84,032 bytes and the overlay DTB is 38,759 bytes.

This repository contains device-tree data only. It does not contain boot, vendor, system, modem, NVRAM, or other partition images.

## Re-extract

From a checkout of this repository:

```powershell
python scripts/extract_archytas_dt.py path\to\boot.img path\to\dtbo.img --output extracted
```

The script extracts the appended main DTB from the Android boot image, the first DTB from the DTBO image, and decompiles both into DTS using the bundled dumper.
