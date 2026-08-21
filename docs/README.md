# Humanoid Navigation Stack

ROS 2 Jazzy packages for field-coordinate conversion and collision-aware path planning.

## Packages

| Package | Purpose |
|---|---|
| field_coordinate_adapter | Converts pixel positions and yaw angles into the map frame |
| humanoid_path_planner | Generates a collision-aware nav_msgs/Path |
| humanoid_path_follower | Reserved for future path-following integration |

## Build and Run

From the repository root:

~~~bash
make build-path-planning
make start-path-planning
~~~

Direct launch:

~~~bash
source ~/colcon_ws/install/setup.bash
ros2 launch humanoid_path_planner path_planning_with_adapter.launch.py
~~~

## Test

~~~bash
make test-path-planning
~~~

## Configuration

- [Adapter configuration](../src/field_coordinate_adapter/config/field_coordinate_adapter.yaml)
- [Planner configuration](../src/humanoid_path_planner/config/path_planning.yaml)

## Documentation

- [Architecture](architecture.md)
- [Coordinate system](coordinate_system.md)
