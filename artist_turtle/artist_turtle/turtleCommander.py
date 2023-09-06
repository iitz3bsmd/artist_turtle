import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from std_srvs.srv import Empty
import math

class turtleCommanderClass(Node):
    def __init__(self):
        super().__init__('turtleCommander')

        self.pose = Pose()

        self.pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

        cb_grp = ReentrantCallbackGroup()
        self.sub_pose = self.create_subscription(Pose, '/turtle1/pose', self.sub_callback, 10, callback_group=cb_grp)
        self.sub_cmd = self.create_subscription(Int32, 'command', self.cmd_callback, 10, callback_group=cb_grp)

        self.cli = self.create_client(Empty, '/reset')
        
        self.stop = 0

        self.msg = Twist()

    def sub_callback(self, data):
        self.pose = data

    def go2goal(self, goal):
        distance = math.sqrt(pow((goal.linear.x - self.pose.x), 2) + pow((goal.linear.y - self.pose.y), 2))
        while distance > 0.1 and self.stop == 0:
            
            dt = 4
            dx = dt*(goal.linear.x - self.pose.x)
            dy = dt*(goal.linear.y - self.pose.y)

            self.msg.linear.x = dx
            self.msg.linear.y = dy
            self.msg.angular.z = 0.0
            self.pub.publish(self.msg)
            distance = math.sqrt(pow((goal.linear.x - self.pose.x), 2) + pow((goal.linear.y - self.pose.y), 2))

    def draw_shape1(self):
        goal = Twist()
        init_x = self.pose.x
        init_y = self.pose.y
        t=-math.pi/2
        while t <= (1/2)*math.pi and self.stop == 0:

            x = init_x + 2*math.cos(9 * t) * math.cos(t)
            y = init_y + 2*math.cos(9 * t) * math.sin(t)
            
            goal.linear.x = x
            goal.linear.y = y
            self.go2goal(goal)
            t +=0.01
    
    def draw_shape2(self):
        goal = Twist()
        init_x = self.pose.x
        init_y = self.pose.y
        t=-math.pi/2
        while t <= (3/2)*math.pi and self.stop == 0:
            x = init_x + 3*math.cos(t)
            y = init_y + 3*math.sin(t)*math.cos(t)
            
            goal.linear.x = x
            goal.linear.y = y
            self.go2goal(goal)
            t +=0.01
            

    def draw_shape3(self):
        goal = Twist()
        init_x = self.pose.x
        init_y = self.pose.y
        t=0
        while self.stop == 0:
            x = init_x + math.sin(t)*(pow(math.e, math.cos(t)) - 2*math.cos(4*t) - pow(math.sin(t/12),5))
            y = init_y + math.cos(t)*(pow(math.e, math.cos(t)) - 2*math.cos(4*t) - pow(math.sin(t/12),5))

            goal.linear.x = x
            goal.linear.y = y
            self.go2goal(goal)
            t +=0.01


    def draw_shapes(self, n):
        if n == 1:
            self.draw_shape1()
        elif n == 2:
            self.draw_shape2()
        elif n == 3:
            self.draw_shape3()
            

    def cmd_callback(self, request):
        request = int(request.data) 
        if request < 4:
            self.draw_shapes(request)
            self.stop = 0
        elif request == 4:
            self.stop =1
            self.msg.linear.x = 0.0
            self.msg.linear.y = 0.0
        elif request == 5:
            self.stop =1
            self.msg.linear.x = 0.0
            self.msg.linear.y = 0.0
            req = Empty.Request()
            self.cli.call_async(req)


def main(args=None):
    rclpy.init(args=args)
    turtleCommander = turtleCommanderClass()
    executer = MultiThreadedExecutor()
    executer.add_node(turtleCommander)
    executer.spin()
    turtleCommander.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
