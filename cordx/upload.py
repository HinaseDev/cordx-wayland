import requests
import json
#curl -X POST -H "secret: your-secret" -H "userid: your-userid" -F "file=@path-to-your-file" https://cordx.lol/api/upload/sharex
import typing as t
import logging

@t.overload
def upload_file(file_path, url, secret, userid):
    pass

@t.overload
def upload_file(file_path, url, auth: dict[str, str]):
    pass

@t.overload
def upload_file(file_path, auth: t.Tuple[str, str]):
    pass

def upload_file(file_path, url, secret=None, userid=None, auth=None):
    if auth is None:
        auth = {"secret": secret, "userid": userid}
    elif isinstance(auth, tuple):
        auth = {"secret": auth[0], "userid": auth[1]}
    elif not isinstance(auth, dict):
        raise TypeError("auth must be a dict or a tuple")
    with open(file_path, "rb") as f:
        print(f"POSTing {file_path} to {url}")
        r = requests.post(url, files={"sharex": f}, headers=auth)
    return r.json()

class __version_info__:
    major = 0
    minor = 1
    patch = 0

    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

class ShareXConfig:
    def __init__(self, version: __version_info__, name: str, destination_type, request_method, request_url, headers, body, file_form_name, url):
        self.version = version
        self.name = name
        self.destination_type = destination_type
        self.request_method = request_method
        self.request_url = request_url
        self.headers = headers
        self.body = body
        self.file_form_name = file_form_name
        self.url = url

class Cordx:
    def __init__(self, sxconfig: ShareXConfig):
        self.sxconfig = sxconfig

    def upload_file(self, file_path):
        res = (upload_file(file_path, url=self.sxconfig.request_url, auth=(self.sxconfig.headers["secret"], self.sxconfig.headers["userid"])))
        return res

def parse_sxcu(sxcu_path):
    with open(sxcu_path, "r") as f:
        data = json.load(f)

    dv = data["Version"]
    return ShareXConfig(
        version=__version_info__(*dv.split(".")),
        name=data["Name"],
        destination_type=data["DestinationType"],
        request_method=data["RequestMethod"],
        request_url=data["RequestURL"],
        headers=data["Headers"],
        body=data["Body"],
        file_form_name=data["FileFormName"],
        url=data["URL"]
    )