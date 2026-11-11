"""No hardware: synthetic Range -> filter -> RViz.   ros2 launch erdi_lrf_examples demo_fake_rviz.launch.py"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    share = get_package_share_directory("erdi_lrf_examples")
    return LaunchDescription([
        Node(package="erdi_lrf_examples", executable="fake_range_node", name="fake_range", output="screen"),
        Node(package="erdi_lrf_examples", executable="range_filter_node", name="range_filter", output="screen"),
        Node(package="tf2_ros", executable="static_transform_publisher", arguments=["0", "0", "0", "0", "0", "0", "map", "erdi_lrf"]),
        Node(package="rviz2", executable="rviz2", arguments=["-d", os.path.join(share, "rviz", "range.rviz")]),
    ])
