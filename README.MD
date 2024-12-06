# HEIC to PNG Converter

A GUI tool to batch convert HEIC image files to PNG format with option to delete original files after conversion.

## Features
- Browse folders containing HEIC files
- Convert multiple HEIC files to PNG
- Option to delete original HEIC files after conversion
- Progress tracking
- Detailed conversion log

## Requirements
- Python 3.x
- Pillow
- pillow-heif
- pywin32

## Usage
1. Run the executable or Python script
2. Browse to select folder containing HEIC files
3. Choose whether to delete original files
4. Click Convert to start the process

## Building from Source
To create executable:
```bash
pyinstaller --onefile --noconsole --name "HEIC Converter v2" --clean --uac-admin heic_png_guiv2.py