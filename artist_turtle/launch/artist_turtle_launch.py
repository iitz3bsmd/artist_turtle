from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtle'
        ),
        Node(
            package='artist_turtle',
            executable='turtleCommander',
            name='turtleCommander',
        )
    ])