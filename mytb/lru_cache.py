"""
former py2 / py3 compatibility helper for functools.lru_cache

exists now only to avoid breaking old projectgs using this function
"""
from functools import lru_cache  # noqa: F401
