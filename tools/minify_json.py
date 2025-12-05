import os
import sys
import glob
import json
import gzip
import pickle


def main() -> None:
    # This is rather janky but it is a stop-gap until the whole library can be ported to C++
    root_path = os.path.dirname(os.path.dirname(__file__))
    src_dir = os.path.join(root_path, "src")
    sys.path.append(src_dir)

    from amulet.game.abc import GameVersion
    from amulet.game.java import JavaGameVersion
    from amulet.game.bedrock import BedrockGameVersion
    from amulet.game.universal import UniversalVersion

    json_path = os.path.join(root_path, "submodules", "PyMCTranslate", "PyMCTranslate", "json")

    universal_version = UniversalVersion.from_json(
        os.path.join(json_path, "versions", "universal")
    )
    _versions: dict[str, list[GameVersion]] = {
        "universal": [universal_version],
    }
    for init_path in glob.glob(
        os.path.join(glob.escape(json_path), "versions", "*", "__init__.json")
    ):
        version_path = os.path.dirname(init_path)

        with open(os.path.join(version_path, "__init__.json")) as f:
            init = json.load(f)

        platform = init["platform"]
        if platform == "bedrock":
            _versions.setdefault("bedrock", []).append(
                BedrockGameVersion.from_json(version_path, universal_version)
            )
        elif platform == "java":
            _versions.setdefault("java", []).append(
                JavaGameVersion.from_json(version_path, universal_version)
            )
        elif platform == "universal":
            pass
        else:
            raise RuntimeError
    with open(
        os.path.join(src_dir, "amulet", "game", "versions.pkl.gz"), "wb"
    ) as pkl:
        pkl.write(gzip.compress(pickle.dumps(_versions)))


if __name__ == '__main__':
    main()
