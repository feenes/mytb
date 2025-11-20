import getpass
import os

from os import PathLike
from pathlib import Path
from typing import Union

from mytb.sentinels import NO_PARAM
from mytb.sentinels import Sentinel

from pykeepass import PyKeePass
from pykeepass.entry import Entry

import pyotp


class KeePass:
    def __init__(
        self,
        fpath: 'Union[str, PathLike[str], None]' = None,
        password: 'str | None | Sentinel' = NO_PARAM,
    ):
        tpath = fpath if fpath is not None else os.environ.get("KEE_FILE")
        assert tpath is not None, "need a path for keypass file"
        self.path: 'PathLike[str]' = Path(tpath)

        self.password: str
        prompt_for_pwd = False
        if password is NO_PARAM:
            self.password = os.environ.get("KEE_PASSWD")
            prompt_for_pwd = self.password is None
        elif password is not None:
            self.password = str(password)

        if prompt_for_pwd:
            print("PWD: ", end="")
            self.password = getpass.getpass()

        assert self.path.exists()
        self.kp: PyKeePass = PyKeePass(self.path, self.password)

    @property
    def entries(self):
        return self.kp.entries

    def get_totp_string(self, entry):
        otp = entry.otp
        if otp and len(otp) > 10:
            if "secret=" in otp:
                otp_secret = otp.split("secret=",)[1].split("&")[0]
            else:
                otp_secret = otp
            totp = pyotp.TOTP(otp_secret).now()
        else:
            props = entry.custom_properties
            # print(f"otp by prop {props}")
            otp_secret = props.get("TimeOtp-Secret-Base32", "")
            assert props["TimeOtp-Algorithm"] == "HMAC-SHA-1"
            assert props["TimeOtp-Length"] == '6'
            assert props["TimeOtp-Period"] == '30'
        if otp_secret:
            totp = pyotp.TOTP(otp_secret).now()
        else:
            totp = ""
        return totp

    def filter_entries(
        self,
        name: 'str | None' = None,
        num: 'int | None' = None,
        url: 'str | None' = None,
    ) -> 'tuple[int, Entry]':
        if name:
            name = name.lower()
            matches = [
                (idx, entry) for (idx, entry) in enumerate(self.entries)
                if name in str(entry.title).lower()
            ]
        elif num:
            try:
                matches = list(self.entries)[num]
            except IndexError:
                matches = []
        elif url:
            matches = [
                (idx, entry) for (idx, entry) in enumerate(self.entries)
                if url.lower() == (entry.url or "").lower()
            ]
        return matches

    def entry(
        self,
        name: 'str | None' = None,
        num: 'int | None' = None,
        url: 'str | None' = None,
        print_choices: bool = False,
    ):
        """
        tries to find an entry if exactly one can be found
        otherwise return None
        if print_choices is True show all
        entries that fulfilled the search criteria
        """
        matches = self.filter_entries(
            name=name,
            num=num,
            url=url,
        )
        if len(matches) == 1:
            return matches[0][1]

        if print_choices:
            for idx, entry in matches:
                print(f"{idx:3}: {entry}")

        return None
