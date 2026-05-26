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

# —————————————————————— CONAN ——————————————————————

CONAN_PROFILE="${PRESET:-default}"
PROFILE_PATH="./conan/profiles/$CONAN_PROFILE"

if [ -f "$PROFILE_PATH" ]; then
    CONAN_PROFILE_ARG="$PROFILE_PATH"
else
    CONAN_PROFILE_ARG="$CONAN_PROFILE"
fi

echo $PRESET
echo $PROFILE_PATH
echo $CONAN_PROFILE_ARG

conan install . \
    --profile="$CONAN_PROFILE_ARG" \
    --output-folder=build \
    --build=missing

if [ $? -ne 0 ]; then
    echo "conan install failed"
    exit 1
fi
# ———————————————————————————————————————————————————

cd build

if [ -z "$PRESET" ]; then
    cmake ..
    cmake --build .
else
    cmake --preset "$PRESET" ..
    cmake --build .
fi

cd ..