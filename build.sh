#!/usr/bin/env sh

if ["$2" = "clear"]; then
    rm -rf build
fi

mkdir build
cd build

if [-z  "$1"]; then
    cmake ..
    cmake --build .
    exit 0
fi

cmake --preset "$1" ..
cmake --build .