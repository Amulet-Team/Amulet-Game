#include <pybind11/pybind11.h>

#include <amulet/game/game.hpp>
#include <amulet/game/java/block.hpp>
#include <amulet/core/version/version.hpp>

#include <amulet/test_utils/test_utils.hpp>

namespace py = pybind11;

void init_test_java(py::module m_parent){
    auto m = m_parent.def_submodule("test_java_");
    m.def("test_get_game_version", [](){
        auto java_game = Amulet::game::get_java_game_version(Amulet::VersionNumber({ 1, 21, 5 }));
        auto block_data = java_game->get_block_data();
        ASSERT_EQUAL(Amulet::game::Waterloggable, Amulet::game::Waterloggable::No, block_data->is_waterloggable("minecraft", "stone"))
        ASSERT_EQUAL(Amulet::game::Waterloggable, Amulet::game::Waterloggable::Yes, block_data->is_waterloggable("minecraft", "acacia_fence"))
        ASSERT_EQUAL(Amulet::game::Waterloggable, Amulet::game::Waterloggable::Always, block_data->is_waterloggable("minecraft", "seagrass"))
    });
}
