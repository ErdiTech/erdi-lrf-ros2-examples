"""Subscribe to `range`, drop outliers (slew limit), median-filter, republish on `range_filtered`."""
import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range

from .filters import MedianFilter, SlewLimiter


class RangeFilter(Node):
    def __init__(self):
        super().__init__("range_filter")
        self.declare_parameter("window", 5)
        self.declare_parameter("max_rate", 50.0)
        self.median = MedianFilter(int(self.get_parameter("window").value))
        self.slew = SlewLimiter(float(self.get_parameter("max_rate").value))
        self.pub = self.create_publisher(Range, "range_filtered", 10)
        self.create_subscription(Range, "range", self.on_range, 10)

    def on_range(self, msg: Range):
        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        r = float(msg.range)
        valid = not (math.isnan(r) or math.isinf(r)) and msg.min_range <= r <= msg.max_range
        accepted = self.slew.update(r, t) if valid else None
        out = self.median.update(accepted)
        if out is None:
            return
        f = Range()
        f.header = msg.header
        f.radiation_type = msg.radiation_type
        f.field_of_view = msg.field_of_view
        f.min_range = msg.min_range
        f.max_range = msg.max_range
        f.range = out
        self.pub.publish(f)


def main(args=None):
    rclpy.init(args=args)
    node = RangeFilter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
