from __future__ import annotations

from functools import cache
from typing import overload, Literal, TYPE_CHECKING
from collections.abc import Sequence
from threading import RLock
import pickle
import os
import gzip
import logging

from amulet.core.version import VersionNumber


if TYPE_CHECKING:
    from .abc import GameVersion
    from .universal import UniversalVersion
    from .java import JavaGameVersion
    from .bedrock import BedrockGameVersion

_log = logging.getLogger(__name__)
_versions: dict[str, list[GameVersion]] | None = None
_lock = RLock()


def _get_versions() -> dict[str, list[GameVersion]]:
    global _versions
    with _lock:
        if _versions is None:
            _log.debug("Loading Minecraft translations")
            pkl_path = os.path.join(os.path.dirname(__file__), "versions.pkl.gz")
            with open(pkl_path, "rb") as pkl:
                _versions = pickle.loads(gzip.decompress(pkl.read()))
            _log.debug("Finished loading Minecraft translations")

    assert _versions is not None
    return _versions


def game_platforms() -> list[str]:
    """
    Get a list of all the platforms there are Version classes for.
    These are currently 'java' and 'bedrock'
    """
    return list(_get_versions().keys())


@overload
def game_versions(platform: Literal["java"]) -> Sequence[JavaGameVersion]: ...


@overload
def game_versions(platform: Literal["bedrock"]) -> Sequence[BedrockGameVersion]: ...


@overload
def game_versions(platform: str) -> Sequence[GameVersion]: ...


def game_versions(platform: str) -> Sequence[GameVersion]:
    """
    Get all known version classes for the platform.

    :param platform: The platform name (use :attr:`platforms` to get the valid platforms)
    :return: The version classes for the platform
    :raises KeyError: If the platform is not present.
    """
    if platform not in _get_versions():
        raise KeyError(f'The requested platform "{platform}" is not present')
    return tuple(_get_versions()[platform])


@overload
def get_game_version(
    platform: Literal["universal"], version_number: VersionNumber
) -> UniversalVersion: ...


@overload
def get_game_version(
    platform: Literal["java"], version_number: VersionNumber
) -> JavaGameVersion: ...


@overload
def get_game_version(
    platform: Literal["bedrock"], version_number: VersionNumber
) -> BedrockGameVersion: ...


@overload
def get_game_version(platform: str, version_number: VersionNumber) -> GameVersion: ...


@cache  # type: ignore
def get_game_version(platform: str, version_number: VersionNumber) -> GameVersion:
    """
    Get a Version class for the requested platform and version number

    :param platform: The platform name (use ``TranslationManager.platforms`` to get the valid platforms)
    :param version_number: The version number or DataVersion (use ``TranslationManager.version_numbers`` to get version numbers for a given platforms)
    :return: The Version class for the given inputs.
    :raises KeyError: If it does not exist.
    """
    if platform not in _get_versions():
        raise KeyError(f'The requested platform "{platform}" is not present')
    for version in _get_versions()[platform]:
        if version.supports_version(platform, version_number):
            return version
    raise KeyError(f"Version {platform}, {version_number} is not supported")
