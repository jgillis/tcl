cmake_minimum_required(VERSION 3.7 FATAL_ERROR)
project (TCL C CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(CMAKE_CXX_COMPILER_ID MATCHES "MSVC")
  add_definitions(-DCOMPLEX_FLOAT=_Fcomplex)
  add_definitions(-DCOMPLEX_DOUBLE=_Dcomplex)
else()
  add_definitions("-DCOMPLEX_FLOAT=float _Complex")
  add_definitions("-DCOMPLEX_DOUBLE=double _Complex")
endif()

set(TCL_SRC
  src/contract.cpp
  src/memoryBroker.cpp
  src/tensor.cpp
  src/utils.cpp
)

if(CMAKE_CXX_COMPILER_ID MATCHES "MSVC")
  set(INTEL_ROOT "C:/Program Files (x86)/IntelSWTools/compilers_and_libraries_2019.4.245/windows")
  set(IOMPROOT "${INTEL_ROOT}/compiler/lib/intel64_win")
  find_library(IOMP NAMES libiomp5md HINTS ${IOMPROOT})
else()
  set(INTEL_ROOT "$ENV{HOME}/intel/compilers_and_libraries_2019.4.243/linux")
  find_library(IOMP iomp5)
endif()
set(MKLROOT "${INTEL_ROOT}/mkl/lib/intel64")

find_library(MKL_INTEL0 NAMES mkl_intel_lp64
HINTS ${MKLROOT})
find_library(MKL_INTEL1 NAMES mkl_intel_thread
HINTS ${MKLROOT})
find_library(MKL_INTEL2 NAMES mkl_core
HINTS ${MKLROOT})


set(MKL_LIBS ${MKL_INTEL0} ${MKL_INTEL1} ${MKL_INTEL2} ${IOMP})

set(TCL_HEADER
  include/contract.h
  include/memoryBroker.h
  include/tcl.h
  include/tcl_types.h
  include/tensor.h
  include/utils.h
)

add_library(tcl STATIC ${TCL_SRC} ${TCL_HEADER})
target_compile_features(tcl PUBLIC cxx_std_11)
target_include_directories(tcl PUBLIC ${PROJECT_SOURCE_DIR}/include)
target_link_libraries(tcl hptt ${MKL_LIBS})
set_property(TARGET tcl PROPERTY POSITION_INDEPENDENT_CODE ON)
set_target_properties(tcl PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS TRUE)


if(CMAKE_CXX_COMPILER_ID MATCHES "MSVC")
  set(TCL_CXX_FLAGS ${TCL_CXX_FLAGS} /openmp)
endif()
target_compile_options(hptt PUBLIC ${TCL_CXX_FLAGS})

if(CMAKE_CXX_COMPILER_ID MATCHES "MSVC")
  target_compile_definitions(tcl PUBLIC "-Dnot=!")
endif()




install(TARGETS tcl
        RUNTIME DESTINATION ${CMAKE_INSTALL_PREFIX}/bin
        LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/lib
        ARCHIVE DESTINATION ${CMAKE_INSTALL_PREFIX}/lib)
install(FILES ${TCL_HEADER}
        DESTINATION ${CMAKE_INSTALL_PREFIX}/include)

if(CMAKE_CXX_COMPILER_ID MATCHES "MSVC")
  install(FILES "${INTEL_ROOT}/redist/intel64_win/compiler/libiomp5md.dll"
        DESTINATION ${CMAKE_INSTALL_PREFIX}/bin)
else()
  file(GLOB_RECURSE MKL_LIBS "${INTEL_ROOT}/mkl/lib/intel64_lin/*.so")
  install(FILES ${MKL_LIBS} "${INTEL_ROOT}/compiler/lib/intel64_lin/libiomp5.so"
        DESTINATION ${CMAKE_INSTALL_PREFIX}/lib)
endif()
