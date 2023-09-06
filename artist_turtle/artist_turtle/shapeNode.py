import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class shapeNodeClass(Node):
    def __init__(self):
        super().__init__('shapeNode')
        self.pub = self.create_publisher(Int32, 'command', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        request = Int32()
        request.data = int(input('What shape do you wanna draw? (input a number) [1: Rose, 2: Infinity, 3: Butterfly, 4: Stop, 5: Reset]: '))

        self.pub.publish(request)


def main(args=None):
    rclpy.init(args=args)
    shapeNode = shapeNodeClass()
    rclpy.spin(shapeNode)
    shapeNode.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()