# HEIC to PNG Batch Converter

A Windows GUI application to batch convert HEIC images to PNG format.

## Features
- Simple GUI interface
- Batch conversion of multiple HEIC files
- Option to delete original files after conversion
- Progress tracking with status updates
- Detailed conversion log

## Download
Download the executable from the [releases](https://github.com/DjSinestro1/BatchConvert_heic_png/releases) section.

## Usage
1. Download and run "HEIC Converter v2.exe"
2. Click "Browse" to select folder containing HEIC files
3. Check "Delete original HEIC files" if desired
4. Click "Convert" to start the conversion process
5. Monitor progress in the log window

## Building from Source
Requirements:
- Python 3.11 or later
- Required packages: `pip install Pillow pillow-heif pywin32`

To create executable:
```bash
pyinstaller --onefile --noconsole --name "HEIC Converter v2" --clean --uac-admin heic_png_guiv2.py