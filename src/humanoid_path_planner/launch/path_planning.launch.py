"""Launch the ROBIT humanoid path planner."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    """Return a launch description with an overridable config file."""
    package_share = get_package_share_directory('humanoid_path_planner')
    default_config = os.path.join(
        package_share,
        'config',
        'path_planning.yaml',
    )
    config_argument = DeclareLaunchArgument(
        'config',
        default_value=default_config,
        description='Path planner parameter YAML file',
    )
    planner = Node(
        package='humanoid_path_planner',
        executable='path_planning',
        name='path_planning',
        output='screen',
        parameters=[LaunchConfiguration('config')],
    )
    return LaunchDescription([config_argument, planner])
