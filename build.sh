#!/usr/bin/env sh

if [ "$1" = "clear" ]; then
    rm -rf ./build
    rm -rf ./bin
    echo "Build directories cleared."
    exit 0
fi

if [ "$2" = "clear" ]; then
    rm -rf ./build
    rm -rf ./bin
fi

mkdir build
cd build

if [ -z "$1" ]; then
    cmake ..
    cmake --build .
    exit 0
fi

cmake --preset "$1" ..
cmake --build .

cd ..