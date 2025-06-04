from unittest import TestCase


class GameVersionTestCase(TestCase):
    def test_game_version(self) -> None:
        from amulet.game.abc import (
            JSONInterface,
            JSONCompatible,
            JSONDict,
            JSONList,
            GameVersion,
        )
