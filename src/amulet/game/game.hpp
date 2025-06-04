#pragma once

#include <memory>
#include <string>

#include "abc/version.hpp"
#include "java/version.hpp"
#include <amulet/core/version/version.hpp>

namespace Amulet {
namespace game {

    std::shared_ptr<GameVersion> get_game_version(const std::string&, const VersionNumber& version);
    std::shared_ptr<JavaGameVersion> get_java_game_version(const VersionNumber& version);

} // namespace game
} // namespace Amulet
