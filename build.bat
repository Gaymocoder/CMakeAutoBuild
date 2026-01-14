@echo off

IF "%~2"=="clear" (
    rd /s /q build
)

mkdir build
cd build

IF "%~1"=="" (
    cmake ..
    cmake --build .
) ELSE (
    cmake --preset %~1 ..
    cmake --build .
)