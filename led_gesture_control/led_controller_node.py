import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial

class LedControllerNode(Node):
    def __init__(self):
        super().__init__('led_controller')

        self.declare_parameter('serial_port', '/dev/ttyACM0')
        self.declare_parameter('baud_rate', 9600)

        port = self.get_parameter('serial_port').value
        baud = self.get_parameter('baud_rate').value

        try:
            self.serial_conn = serial.Serial(port, baud, timeout=1)
            self.get_logger().info(f'Connected to Arduino on {port}')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to connect: {e}')
            self.serial_conn = None

        self.subscription = self.create_subscription(
            Int32,
            'finger_count',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        count = msg.data
        if self.serial_conn and self.serial_conn.is_open:
            if count == 5:
                self.serial_conn.write(b'1')
                self.get_logger().info('5 fingers detected → LED ON')
            else:
                self.serial_conn.write(b'0')
                self.get_logger().info(f'{count} fingers → LED OFF')

    def destroy_node(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.write(b'0')
            self.serial_conn.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = LedControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()