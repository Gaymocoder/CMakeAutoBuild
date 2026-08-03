cmake_minimum_required(VERSION 3.28)
project(Hello)

set(MAIN_EXE src/main.cpp)
add_executable(GCS_HelloWorld ${MAIN_EXE})
target_link_libraries(GCS_HelloWorld PRIVATE Boost::headers)
gcs_binary_prepare(GCS_HelloWorld)