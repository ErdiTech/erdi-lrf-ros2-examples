"""Real LRF22VB (millimetre stream) -> filter -> RViz.
   ros2 launch erdi_lrf_ros2_examples lrf22vb_rviz.launch.py port:=/dev/ttyUSB0
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    share = get_package_share_directory("erdi_lrf_ros2_examples")
    return LaunchDescription([
        DeclareLaunchArgument("port", default_value="/dev/ttyUSB0"),
        DeclareLaunchArgument("model", default_value="LRF22VB"),
        Node(
            package="erdi_lrf_ros2", executable="range_node", name="erdi_lrf_range", output="screen",
            parameters=[{"port": LaunchConfiguration("port"), "model": LaunchConfiguration("model"),
                         "rate": 50.0, "frame_id": "erdi_lrf"}],
        ),
        Node(package="erdi_lrf_ros2_examples", executable="range_filter_node", name="range_filter", output="screen"),
        Node(package="tf2_ros", executable="static_transform_publisher", arguments=["0", "0", "0", "0", "0", "0", "map", "erdi_lrf"]),
        Node(package="rviz2", executable="rviz2", arguments=["-d", os.path.join(share, "rviz", "range.rviz")]),
    ])
