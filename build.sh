#!/usr/bin/env sh

CLEAR_BUILD=0
PRESET=""

if [ "$1" = "clear" ]; then
    CLEAR_BUILD=1
elif [ "$2" = "clear" ]; then
    CLEAR_BUILD=1
    PRESET="$1"
elif [ -n "$1" ]; then
    PRESET="$1"
fi

if [ "$CLEAR_BUILD" = "1" ]; then
    rm -rf ./build
    rm -rf ./bin
    echo "Build directories cleared."
fi

mkdir -p build
cd build

if [ -z "$PRESET" ]; then
    cmake ..
    cmake --build .
else
    cmake --preset "$PRESET" ..
    cmake --build .
fi

cd ..