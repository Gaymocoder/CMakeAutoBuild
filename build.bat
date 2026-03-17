@echo off
setlocal enabledelayedexpansion

set CLEAR_BUILD=0
set PRESET=

if "%~1"=="clear" (
    set CLEAR_BUILD=1
) else if "%~2"=="clear" (
    set CLEAR_BUILD=1
    set PRESET=%~1
) else if not "%~1"=="" (
    set PRESET=%~1
)

if !CLEAR_BUILD!==1 (
    if exist ".\build" rd /s /q ".\build"
    if exist ".\bin" rd /s /q ".\bin"
    echo Build directories cleared.
)

mkdir build
cd build

REM Run cmake and build
if "!PRESET!"=="" (
    cmake ..
    cmake --build .
) else (
    cmake --preset !PRESET! ..
    cmake --build .
)

cd ..