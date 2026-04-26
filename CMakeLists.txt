cmake_minimum_required(VERSION 3.28)
project(CMakeAutoBuild VERSION 1.1.0)

block()
    include(${CMAKE_CURRENT_LIST_DIR}/cmake/gcs_utils.cmake)

    set(CMAKE_CXX_STANDARD 23)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

    set(GCS_INCLUDE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/include")
    set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/lib)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin)
    
    add_subdirectory(Hello)
endblock()