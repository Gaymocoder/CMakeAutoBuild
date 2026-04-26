
function(gcs_export_prepare target_name)
    message("gcs_utils: Exporting ${target_name}")

    foreach(obj IN LISTS ARGN)
        message("Adding source-object '${obj}' to target '${target_name}'")
        target_sources(${target_name} PRIVATE $<TARGET_OBJECTS:${obj}>)
    endforeach()

    string(FIND "${target_name}" "_" POS)
    if(POS EQUAL -1)
        set(MODULE "${target_name}")
        set(PREFIX "${target_name}")
    else()
        string(SUBSTRING "${target_name}" 0 ${POS} PREFIX)
        math(EXPR RIGHT_START "${POS} + 1")
        string(SUBSTRING "${target_name}" ${RIGHT_START} -1 MODULE)
    endif()

    add_library("${PREFIX}::${MODULE}" ALIAS "${target_name}")
    target_include_directories("${target_name}" PUBLIC
        $<BUILD_INTERFACE:${GCS_INCLUDE_DIRS}>
        $<INSTALL_INTERFACE:include>
    )
    set_target_properties("${target_name}" PROPERTIES EXPORT_NAME "${MODULE}")
    target_compile_options("${target_name}" PRIVATE -Wall -Wextra -pedantic -O0 -g)
    if (MINGW)
        target_link_libraries("${target_name}" INTERFACE
            $<$<COMPILE_FEATURES:cxx_std_23> : stdc++exp>
        )
    endif()

    message("gcs_utils: Exported (with prefix = '${PREFIX}', module = '${MODULE}')")
endfunction()


function(gcs_object_prepare target_name)
    target_include_directories("${target_name}" PUBLIC "${GCS_INCLUDE_DIRS}")
    target_compile_options("${target_name}" PRIVATE -Wall -Wextra -pedantic -O0 -g)
    if (MINGW)
        target_link_libraries("${target_name}" INTERFACE
            $<$<COMPILE_FEATURES:cxx_std_23> : stdc++exp>
        )
    endif()
endfunction()