#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zipfile
import shutil
from pathlib import Path

skills_dir = Path('05_Outputs/skills/packages')
claude_dir = Path.home() / '.claude' / 'skills'
claude_dir.mkdir(parents=True, exist_ok=True)

count = 0
for zip_file in skills_dir.glob('*.zip'):
    if zip_file.is_file():
        dest_dir = claude_dir / zip_file.stem
        shutil.unpack_archive(str(zip_file), str(dest_dir))
        count += 1
        print(f"Installed: {zip_file.name}")

print(f"\nTotal: {count} skills installed to {claude_dir}")
