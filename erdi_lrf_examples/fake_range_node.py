"""Publish a synthetic sensor_msgs/Range sine wave so the RViz demo runs without hardware."""
import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range


class FakeRange(Node):
    def __init__(self):
        super().__init__("fake_range")
        self.declare_parameter("frame_id", "erdi_lrf")
        self.declare_parameter("min_range", 0.05)
        self.declare_parameter("max_range", 20.0)
        self.declare_parameter("rate", 20.0)
        self.pub = self.create_publisher(Range, "range", 10)
        self.t0 = self.get_clock().now()
        self.create_timer(1.0 / float(self.get_parameter("rate").value), self.tick)

    def tick(self):
        t = (self.get_clock().now() - self.t0).nanoseconds * 1e-9
        lo = float(self.get_parameter("min_range").value)
        hi = float(self.get_parameter("max_range").value)
        msg = Range()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.get_parameter("frame_id").value
        msg.radiation_type = Range.INFRARED
        msg.field_of_view = 0.05
        msg.min_range = lo
        msg.max_range = hi
        msg.range = lo + (hi - lo) * (0.5 + 0.4 * math.sin(0.5 * t))
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = FakeRange()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
