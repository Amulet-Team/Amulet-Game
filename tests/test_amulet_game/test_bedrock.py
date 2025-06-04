from unittest import TestCase


class BedrockGameVersionTestCase(TestCase):
    def test_game_version(self) -> None:
        from amulet.game.abc import GameVersion
        from amulet.game.bedrock import BedrockGameVersion

        self.assertTrue(issubclass(BedrockGameVersion, GameVersion))

    def test_get_versions(self) -> None:
        from amulet.game import game_platforms, game_versions
        from amulet.game.bedrock import BedrockGameVersion

        self.assertIn("bedrock", game_platforms())
        self.assertLess(10, len(game_versions("bedrock")))
        for v in game_versions("bedrock"):
            self.assertIsInstance(v, BedrockGameVersion)
