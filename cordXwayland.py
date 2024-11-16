import os.path
import shutil
import subprocess
import random
import string

import pyperclip
from pydbus import SessionBus
import argparse

parser = argparse.ArgumentParser("cordXwayland", "CordX Wayland screenshot uploader")
parser.add_argument("--sxcu", "-s", help="Path to .sxcu file", required=False)
parser.add_argument("-o", "--output", help="Path to save the screenshot", required=False)

args = parser.parse_args()


if args.output is None:
    # Assume the user wants to use the default .sxcu file
    uid = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    path = os.path.expanduser(f"~/.cache/cordx.{uid}.png")
else:
    path = args.output
bus = SessionBus()
notifications = bus.get('.Notifications')

subprocess.run(["grimshot", "save", "area", path])


notifications.Notify('test', 0, 'dialog-information', "Image saved", f"Image saved to {os.path.abspath(path)}", [], {}, 5000)
if args.sxcu is not None:
    from cordx.upload import Cordx, parse_sxcu
    c = Cordx(parse_sxcu(args.sxcu))
    data = c.upload_file(path)
    if data["status"] != "OK":
        notifications.Notify('test', 0, 'dialog-error', f"Upload failed - {data['status']}", f"Upload failed\n{data['message']}\n\nSupport: {data['support']}", [], {}, 5000)
    else:
        url =data["url"]
        pyperclip.copy(url)
        notifications.Notify('test', 0, 'dialog-information', "Upload successful", f"Upload successful \n{url}", [], {}, 5000)