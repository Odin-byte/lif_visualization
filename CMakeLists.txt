cmake_minimum_required(VERSION 3.0.2)
project(lif_visualizer)

find_package(catkin REQUIRED)

catkin_python_setup()

catkin_package()

catkin_install_python(PROGRAMS
    scripts/${PROJECT_NAME}.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)