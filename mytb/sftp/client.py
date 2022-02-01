"""
mytb.sftp.client

implementation of an sftp client based on paramiko.
"""
import typing
from pathlib import Path

import paramiko
from paramiko import Transport

from mytb.sftp.helpers import SftpUrl


opt_str = typing.Optional[str]


class SftpClient:
    def __init__(
            self,
            host: opt_str = None,
            port: opt_str = None,
            username: opt_str = None,
            password: opt_str = None,
            path: opt_str = None,
            url: opt_str = None,
            verify: bool = True,
            ):
        if url:
            assert not verify, "host verification not implemented so far"
            parsed = SftpUrl(url)
            host = parsed.host
            port = parsed.port
            username = parsed.user
            password = parsed.password
            path = parsed.path
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.path = path
        self._conn = None
        self.key = None  # public key auth not implemented so far
        self.connected = False
        self.cwd = Path(".")
        self.lcwd = Path(".").resolve()

    def _resolve_path(
            self,
            path,
            is_remote: bool = True,
            ):
        """
        helper to resolve local / remote paths
        """
        if path:
            path = path if isinstance(path, Path) else Path(path)
        if is_remote:
            if path:
                # make relative except path is absolute
                if path.resolve() == (Path(".") / path).resolve():
                    path = (self.cwd / path).resolve().relative_to(
                        Path(".").resolve())
            else:
                path = self.cwd
        else:
            path = Path(".") if not path else path
            path = (self.lcwd / path).resolve()
        return path

    def connect(self):
        transport = Transport(sock=(self.host, self.port))
        assert not self.connected
        if not self.key:
            transport.connect(username=self.username, password=self.password)
            self._conn = paramiko.SFTPClient.from_transport(transport)
            self.connected = True
        return self.connected

    def cd(self, path):
        """ change remote directory """
        path = self._resolve_path(path)
        self.cwd  = path

    def lcd(self, path):
        """ change local directory """
        path = self._resolve_path(path, is_remote=False)
        self.lcwd  = path

    def ls(self, path=None):
        """ return list of files
            relative to path
        """
        path = self._resolve_path(path)
        dirs = self._conn.listdir(str(path))
        return dirs

    def get(self, path, localpath=None):
        path = self._resolve_path(path)
        lpath = self._resolve_path(localpath, is_remote=False)
        lpath = lpath / path.name
        print(f"Path {path} / {lpath}")
        self._conn.get(str(path), str(lpath))

    def put(self, localpath, rmtpath=None):
        lpath = self._resolve_path(localpath, is_remote=False)
        path = self._resolve_path(rmtpath)
        path = path / lpath.name
        print(f"Path {lpath} / {path}")
        self._conn.put(str(lpath), str(path))
