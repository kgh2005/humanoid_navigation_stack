"""Launch the ROBIT field coordinate adapter."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    """Return the field coordinate adapter launch description."""
    package_share = get_package_share_directory('field_coordinate_adapter')
    default_config = os.path.join(
        package_share,
        'config',
        'field_coordinate_adapter.yaml',
    )
    config_argument = DeclareLaunchArgument(
        'config',
        default_value=default_config,
        description='Field coordinate adapter parameter YAML file',
    )
    adapter = Node(
        package='field_coordinate_adapter',
        executable='field_coordinate_adapter',
        name='field_coordinate_adapter',
        output='screen',
        parameters=[LaunchConfiguration('config')],
    )
    return LaunchDescription([config_argument, adapter])
