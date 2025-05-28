import os
import subprocess
import sys
from pathlib import Path
import requirements

from setuptools import setup, Extension, Command
from setuptools.command.build_ext import build_ext
from packaging.version import Version

import versioneer


def fix_path(path: str) -> str:
    return os.path.realpath(path).replace(os.sep, "/")


dependencies = requirements.get_fixed_runtime_dependencies()

cmdclass: dict[str, type[Command]] = versioneer.get_cmdclass()


class CMakeBuild(cmdclass.get("build_ext", build_ext)):
    def build_extension(self, ext):
        import pybind11
        import amulet.pybind11_extensions
        import amulet.io
        import amulet.nbt
        import amulet.core

        ext_dir = (
            (Path.cwd() / self.get_ext_fullpath("")).parent.resolve()
            / "amulet"
            / "game"
        )
        game_src_dir = (
            Path.cwd() / "src" / "amulet" / "game" if self.editable_mode else ext_dir
        )

        platform_args = []
        if sys.platform == "win32":
            platform_args.extend(["-G", "Visual Studio 17 2022"])
            if sys.maxsize > 2**32:
                platform_args.extend(["-A", "x64"])
            else:
                platform_args.extend(["-A", "Win32"])
            platform_args.extend(["-T", "v143"])

        if subprocess.run(
            [
                "cmake",
                *platform_args,
                f"-DPYTHON_EXECUTABLE={sys.executable}",
                f"-Dpybind11_DIR={pybind11.get_cmake_dir().replace(os.sep, '/')}",
                f"-Damulet_pybind11_extensions_DIR={fix_path(amulet.pybind11_extensions.__path__[0])}",
                f"-Damulet_io_DIR={fix_path(amulet.io.__path__[0])}",
                f"-Damulet_nbt_DIR={fix_path(amulet.nbt.__path__[0])}",
                f"-Damulet_core_DIR={fix_path(amulet.core.__path__[0])}",
                f"-Damulet_game_DIR={fix_path(game_src_dir)}",
                f"-DAMULET_GAME_EXT_DIR={fix_path(ext_dir)}",
                f"-DCMAKE_INSTALL_PREFIX=install",
                "-B",
                "build",
            ]
        ).returncode:
            raise RuntimeError("Error configuring amulet_game")
        if subprocess.run(
            ["cmake", "--build", "build", "--config", "Release"]
        ).returncode:
            raise RuntimeError("Error installing amulet_game")
        if subprocess.run(
            ["cmake", "--install", "build", "--config", "Release"]
        ).returncode:
            raise RuntimeError("Error installing amulet_game")


cmdclass["build_ext"] = CMakeBuild


def _get_version() -> str:
    version_str: str = versioneer.get_version()

    if os.environ.get("AMULET_FREEZE_COMPILER", None):
        # Add the compiler version to the library version so that pip sees it as a distinct version.
        compiler_version_str = ".".join(
            amulet_compiler_version.__version__.split(".")[3:]
        )
        if compiler_version_str:
            version = Version(version_str)
            if version.epoch != 0 or version.is_devrelease or version.is_postrelease:
                raise RuntimeError(f"Unsupported version format. {version_str}")
            major, minor, patch, fix, *_ = version.release + (0, 0, 0, 0)
            pre = "".join(map(str, version.pre)) if version.is_prerelease else ""
            local = f"+{version.local}" if version.local else ""
            version_str = (
                f"{major}.{minor}.{patch}.{fix}.{compiler_version_str}{pre}{local}"
            )

    return version_str


setup(
    version=_get_version(),
    cmdclass=cmdclass,
    ext_modules=[Extension("amulet.game._amulet_game", [])],
    install_requires=dependencies,
)
