@echo off

IF "%~1"=="clear" (
    rd /s /q .\build
    rd /s /q .\bin
    echo Build directories cleared.
    exit /b 0
)

IF "%~2"=="clear" (
    rd /s /q .\build
    rd /s /q .\bin
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

cd ..