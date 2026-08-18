#include <pybind11/pybind11.h>

namespace py = pybind11;

py::module init_java(py::module);

void init_amulet_game(py::module m)
{
    m.attr("__doc__") = "A module to store data about the game including state enumerations and translations between different game versions.";

    auto game_module = py::module::import("amulet.game.game");
    m.attr("get_game_platforms") = game_module.attr("get_game_platforms");
    m.attr("get_game_versions") = game_module.attr("get_game_versions");
    m.attr("get_game_version") = game_module.attr("get_game_version");

    auto java_module = init_java(m);
    m.attr("JavaGameVersion") = java_module.attr("JavaGameVersion");

    auto bedrock_module = py::module::import("amulet.game.bedrock");
    m.attr("BedrockGameVersion") = bedrock_module.attr("BedrockGameVersion");
}
