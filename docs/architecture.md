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

Opponent robots passed to the planner core are inflated by the robot radius and safety margin. The ball is included only while avoidance is active, initially configured by `ball.avoid` and updated at runtime through `/ball_obstacle_active`. Each enabled goal is modeled as a static U-shaped obstacle.

The planner maintains two obstacle layers:

- `critical`: the physical obstacle inflated by the robot radius
- `margin`: the critical area plus the configured safety margin

Normal visibility-graph edges that cross a margin are blocked. If the start or goal is already inside an obstacle, edges that let the path leave or enter that obstacle remain available. An allowed edge crossing a critical area uses `search.critical_cost_multiplier` as its cost multiplier. The direct start-to-goal edge is retained as a best-effort fallback candidate, allowing the planner to return a path when no collision-free detour exists.

~~~text
goal_x = ±(field.length / 2 + goal_obstacle.goal_line_offset)
~~~

## Launch

[path_planning_with_adapter.launch.py](../src/humanoid_path_planner/launch/path_planning_with_adapter.launch.py) starts the adapter and planner together. The path follower is not included yet.

[path_planning_debug.launch.py](../src/humanoid_path_planner/launch/path_planning_debug.launch.py) additionally starts RViz with the installed planner configuration.
