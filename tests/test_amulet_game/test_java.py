from unittest import TestCase


class JavaGameVersionTestCase(TestCase):
    def test_game_version(self) -> None:
        from amulet.game.abc import GameVersion
        from amulet.game.java import JavaGameVersion

        self.assertTrue(issubclass(JavaGameVersion, GameVersion))

    def test_get_versions(self) -> None:
        from amulet.game import game_platforms, game_versions
        from amulet.game.java import JavaGameVersion

        self.assertIn("java", game_platforms())
        self.assertLess(10, len(game_versions("java")))
        for v in game_versions("java"):
            self.assertIsInstance(v, JavaGameVersion)

    def test_cpp(self) -> None:
        from test_amulet_game.test_java_ import test_get_game_version

        test_get_game_version()
