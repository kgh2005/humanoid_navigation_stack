# Coordinate System

## Pixel to Map

Source localization coordinates use a 1100 × 800 px image with the origin at the top-left corner.

The adapter converts them into a centered, meter-based map frame:

~~~text
x_m = (x_px - width_px / 2) × width_m / width_px
y_m = (height_px / 2 - y_px) × height_m / height_px
~~~

| Pixel | Map | Location |
|---|---|---|
| (0, 0) | (-5.5, 4.0) | Top-left |
| (550, 400) | (0.0, 0.0) | Center |
| (1100, 800) | (5.5, -4.0) | Bottom-right |

Axis directions in the map frame:

- Positive X: right
- Positive Y: up

## Yaw

~~~text
ROS yaw = source yaw + 90°
~~~

| Source yaw | Direction | ROS yaw |
|---:|---|---:|
| 0° | Up | 90° |
| 90° | Left | 180° |
| -90° | Right | 0° |
| ±180° | Down | -90° (or 270°) |

Robot yaw comes from ImuMsg.yaw. Target yaw comes from Master2localization.angle_to_target.

## Important Settings

- Keep zero_pose_is_invalid set to false because the field center is (0, 0).
- Adapter field dimensions define the converted coordinate range.
- Planner field_length defines the goal positions.

See the [adapter configuration](../src/field_coordinate_adapter/config/field_coordinate_adapter.yaml) and [planner configuration](../src/humanoid_path_planner/config/path_planning.yaml).
