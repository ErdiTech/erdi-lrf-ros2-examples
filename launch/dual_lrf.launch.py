"""Two rangefinders in separate namespaces (front: LRF100H on ttyUSB0, down: LRF22VB on ttyUSB1)."""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    def lrf(ns, port, model, frame):
        return Node(
            package="erdi_lrf_ros2", executable="range_node", namespace=ns, name="range", output="screen",
            parameters=[{"port": port, "model": model, "rate": 20.0, "frame_id": frame}],
        )

    return LaunchDescription([
        lrf("front", "/dev/ttyUSB0", "LRF100H", "front_lrf"),
        lrf("down", "/dev/ttyUSB1", "LRF22VB", "down_lrf"),
    ])
