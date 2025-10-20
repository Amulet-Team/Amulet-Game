from unittest import TestCase


class UniversalGameVersionTestCase(TestCase):
    def test_game_version(self) -> None:
        from amulet.game.abc import GameVersion
        from amulet.game.universal import UniversalVersion

        self.assertTrue(issubclass(UniversalVersion, GameVersion))

    def test_get_versions(self) -> None:
        from amulet.game import get_game_platforms, get_game_versions
        from amulet.game.universal import UniversalVersion

        self.assertIn("universal", get_game_platforms())
        self.assertEqual(1, len(get_game_versions("universal")))
        for v in get_game_versions("universal"):
            self.assertIsInstance(v, UniversalVersion)
