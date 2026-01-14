cmake_minimum_required(VERSION 3.28)
project(Hello)

set(MAIN_EXE src/main.cpp)

add_executable(GCS_HelloWorld ${MAIN_EXE})
set_target_properties(GCS_HelloWorld PROPERTIES OUTPUT_NAME "GCS.HelloWorld")

if (MINGW)
    target_link_libraries(GCS_HelloWorld stdc++exp)
endif()