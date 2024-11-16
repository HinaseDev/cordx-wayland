# CordX-Wayland

CordX Client for Wayland

## Installation

```bash
git clone https://github.com/hinasedev/CordX-Wayland.git
cd CordX-Wayland
pip install -r requirements.txt
```

Also make sure `grimshot` is installed on your system.

## Usage

You don't need to use CordX to use this tool. Calling `cordXwayland.py` with no arguments will take a screenshot and save it into .cache

### Options
`-o` or `--output` to specify the output file. Default is .cache/cordx.XXXXXXXX.png

`-s` or `--sxcu` to specify your ShareX Custom Uploader file. If specified, the screenshot will be uploaded to the specified uploader.

