"""
mytp.sftp.helpers

Helper classes for mytp.sftp
"""

import typing


class SftpUrl:
    """
    helper for parsing an sftp url
    """
    def __init__(
            self,
            url: str,
            key: typing.Optional[str] = None
            ):
        if not url.lower().startswith("sftp://"):
            url = "sftp://" + url
        self.url = url

        _proto, user_path = url.split("//", 1)
        user_pass, host_path = user_path.split('@', 1)
        if ':' in user_pass:
            user, password = user_pass.split(':', 1)
        else:
            user = user_pass
            password = None

        host, path = host_path.split('/', 1)
        port = 22
        if ":" in host:
            host, portstr = host.split(":")
            port = int(portstr)

        self.key = key
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.path = path
