"""Launch the field coordinate adapter and path planner."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description() -> LaunchDescription:
    """Include the adapter and planner launch files."""
    adapter_launch = GroupAction(
        scoped=True,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory(
                            'field_coordinate_adapter'
                        ),
                        'launch',
                        'field_coordinate_adapter.launch.py',
                    )
                )
            )
        ],
    )

    planner_launch = GroupAction(
        scoped=True,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory(
                            'humanoid_path_planner'
                        ),
                        'launch',
                        'path_planning.launch.py',
                    )
                )
            )
        ],
    )

    return LaunchDescription([
        adapter_launch,
        planner_launch,
    ])
