import sys

import pytest


@pytest.mark.skipif(
    sys.version_info < (3, 4),
    reason="requires python3.4+")
def test_aio_compat():
    """ can patch old asyncios """
    import asyncio
    import mytb.aio.compat
    mytb.aio.compat.patch()

    assert asyncio.run
    assert asyncio.all_tasks

    patched = mytb.aio.compat.patched
    if sys.version_info < (3, 7):
        assert "asyncio.run" in patched
        assert "asyncio.all_tasks" in patched
