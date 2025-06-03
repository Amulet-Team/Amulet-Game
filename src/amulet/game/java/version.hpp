#pragma once

#include <amulet/game/abc/version.hpp>

#include "block.hpp"

namespace Amulet {
namespace game {

    class JavaGameVersion : public GameVersion {
    public:
        using GameVersion::GameVersion;
        using GameVersion::operator=;

        std::shared_ptr<JavaBlockData> get_block_data();
    };

} // namespace game
} // namespace Amulet
