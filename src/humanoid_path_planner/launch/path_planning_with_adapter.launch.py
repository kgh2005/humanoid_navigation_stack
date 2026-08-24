"""Launch the field coordinate adapter and path planner."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    GroupAction,
    IncludeLaunchDescription,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description() -> LaunchDescription:
    """Include the adapter and planner launch files."""
    adapter_share = get_package_share_directory(
        'field_coordinate_adapter'
    )
    planner_share = get_package_share_directory(
        'humanoid_path_planner'
    )
    adapter_config_argument = DeclareLaunchArgument(
        'adapter_config',
        default_value=os.path.join(
            adapter_share,
            'config',
            'field_coordinate_adapter.yaml',
        ),
        description='Field coordinate adapter parameter YAML file',
    )
    planner_config_argument = DeclareLaunchArgument(
        'config',
        default_value=os.path.join(
            planner_share,
            'config',
            'path_planning.yaml',
        ),
        description='Path planner parameter YAML file',
    )
    adapter_launch = GroupAction(
        scoped=True,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        adapter_share,
                        'launch',
                        'field_coordinate_adapter.launch.py',
                    )
                ),
                launch_arguments={
                    'config': LaunchConfiguration('adapter_config'),
                }.items(),
            )
        ],
    )

    planner_launch = GroupAction(
        scoped=True,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        planner_share,
                        'launch',
                        'path_planning.launch.py',
                    )
                ),
                launch_arguments={
                    'config': LaunchConfiguration('config'),
                }.items(),
            )
        ],
    )

    return LaunchDescription([
        adapter_config_argument,
        planner_config_argument,
        adapter_launch,
        planner_launch,
    ])
