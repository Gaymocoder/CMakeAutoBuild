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

REM —————————————————————— CONAN ——————————————————————

if "!PRESET!"=="" (
    set CONAN_PROFILE=default
) else (
    set CONAN_PROFILE=!PRESET!
)

set PROFILE_PATH=.\conan\profiles\!CONAN_PROFILE!

if exist "!PROFILE_PATH!" (
    set CONAN_PROFILE_ARG=!PROFILE_PATH!
) else (
    set CONAN_PROFILE_ARG=!CONAN_PROFILE!
)

conan install . --profile=!CONAN_PROFILE_ARG! --output-folder=build --build=missing
if errorlevel 1 (
    echo conan install failed
    exit /b 1
)

REM ———————————————————————————————————————————————————

if "!PRESET!"=="" (
    cmake -B build -S .
) else (
    cmake --preset !PRESET! .
)
if errorlevel 1 exit /b 1

cmake --build build --config Release