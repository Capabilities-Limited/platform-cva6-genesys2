# Copyright 2019-present PlatformIO <contact@platformio.org>
#
# Modifications for CVA6 Copyright 2024 Capabilities Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
CVA6 SDK

Open Source Software for Developing on the CVA6 Platform
"""

from os import listdir
from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()

print("Finding framework")
FRAMEWORK_DIR = env.PioPlatform().get_package_dir("framework-cva6-genesys2")
print(f"found {FRAMEWORK_DIR}")
assert FRAMEWORK_DIR and isdir(FRAMEWORK_DIR)


def is_valid_target(target):
    print(FRAMEWORK_DIR)
    target_dir = join(FRAMEWORK_DIR, "config", target)
    return isdir(target_dir)


env.SConscript("_bare.py", exports="env")

target = env.subst("$BOARD")

env.Append(
    ASPPFLAGS=[
        ("-D__ASSEMBLY__=1"),
        "-fno-common"
    ],

    CFLAGS=[
        "-static",
        "-std=gnu99"
    ],

    CCFLAGS=[
        "-fno-builtin-printf"
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "cva6-baremetal-bsp", "bsp", "include")
    ],

    LIBPATH=[
        join(FRAMEWORK_DIR, "cva6-baremetal-bsp", "bsp", "config")
    ],

    LINKFLAGS=[
        "-static"
    ],
)

if not is_valid_target(target):
    print ("Could not find BSP package for %s" % target)
    env.Exit(1)

if not env.BoardConfig().get("build.ldscript", ""):
    env.Replace(LDSCRIPT_PATH=env.BoardConfig().get("build.cva6-sdk.ldscript", ""))

#
# Target: Build core BSP libraries
#

libs = []

for driver in listdir(join(FRAMEWORK_DIR, "cva6-baremetal-bsp", "bsp", "drivers")):
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "cva6-baremetal-bsp", "bsp", "drivers", driver),
            join(FRAMEWORK_DIR, "cva6-baremetal-bsp", "bsp", "drivers", driver))
    )

libs.append(
    env.BuildLibrary(
        join("$BUILD_DIR", "cva6-baremetal-bsp", "bsp", "hal"),
        join(FRAMEWORK_DIR, "cva6-baremetal-bsp", "bsp", "hal")
    )
)

env.Prepend(LIBS=libs)
