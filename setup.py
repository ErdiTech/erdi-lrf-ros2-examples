import os
from glob import glob

from setuptools import find_packages, setup

package_name = "erdi_lrf_ros2_examples"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
        (os.path.join("share", package_name, "rviz"), glob("rviz/*.rviz")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="ERDI TECH LTD",
    maintainer_email="tommy@erdimail.com",
    description="Examples for the ERDI laser rangefinder ROS 2 driver",
    license="MIT",
    entry_points={
        "console_scripts": [
            "fake_range_node = erdi_lrf_ros2_examples.fake_range_node:main",
            "range_filter_node = erdi_lrf_ros2_examples.range_filter_node:main",
        ],
    },
)
