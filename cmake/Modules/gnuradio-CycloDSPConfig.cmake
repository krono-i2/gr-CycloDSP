find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_CYCLODSP gnuradio-CycloDSP)

FIND_PATH(
    GR_CYCLODSP_INCLUDE_DIRS
    NAMES gnuradio/CycloDSP/api.h
    HINTS $ENV{CYCLODSP_DIR}/include
        ${PC_CYCLODSP_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_CYCLODSP_LIBRARIES
    NAMES gnuradio-CycloDSP
    HINTS $ENV{CYCLODSP_DIR}/lib
        ${PC_CYCLODSP_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-CycloDSPTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_CYCLODSP DEFAULT_MSG GR_CYCLODSP_LIBRARIES GR_CYCLODSP_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_CYCLODSP_LIBRARIES GR_CYCLODSP_INCLUDE_DIRS)
