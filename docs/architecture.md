# Architecture

## Data Flow

~~~mermaid
flowchart LR
    Localization["/localization"] --> Adapter["field_coordinate_adapter"]
    Imu["/Imu"] --> Adapter
    Target["/master2local"] --> Adapter

    Adapter -->|robot, target, obstacles, ball| Planner["path_planning"]
    BallControl["/ball_obstacle_active"] --> Planner

    Planner -->|/vg/path| Follower["path_follower (future)"]
    Planner -->|/vg/markers| RViz
~~~

## Components

### field_coordinate_adapter

Stores the latest localization, IMU, and target messages, then publishes converted Markers at 30 Hz.

### path_planning

Consumes the converted Markers and generates a visibility-graph path at up to 10 Hz.

## Main Topics

| Topic | Type | Description |
|---|---|---|
| /localization | RobocupLocalization | Robot, ball, and obstacle pixel positions |
| /Imu | ImuMsg | Robot yaw |
| /master2local | Master2localization | Target position and yaw |
| /adapter/pose_marker | Marker | Robot pose in the map frame |
| /adapter/target_marker | Marker | Target pose in the map frame |
| /adapter/obstacle_marker | MarkerArray | Opponent obstacles |
| /adapter/ball_marker | Marker | Ball position |
| /vg/path | Path | Planned path |
| /vg/markers | MarkerArray | Planner debug visualization |

## Obstacles

Opponent robots and the ball are inflated by the robot radius and safety margin. Each goal is modeled as a static U-shaped obstacle.

~~~text
goal_x = ±goal_obstacle.field_length / 2
~~~

## Launch

[path_planning_with_adapter.launch.py](../src/humanoid_path_planner/launch/path_planning_with_adapter.launch.py) starts the adapter and planner together. The path follower is not included yet.
