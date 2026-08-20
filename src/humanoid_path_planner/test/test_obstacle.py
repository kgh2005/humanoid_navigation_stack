"""Tests for circular inflation, merging, and goal geometry."""

import math

from humanoid_path_planner.obstacle import (
    make_goal_obstacles,
    ObstacleMap,
    RoundObstacle,
)
from humanoid_path_planner.parameters import (
    GoalObstacleParameters,
    ObstacleParameters,
)
from humanoid_path_planner.visibility_graph import point_in_polygon


def obstacle_parameters() -> ObstacleParameters:
    """Return compact deterministic obstacle test parameters."""
    return ObstacleParameters(
        robot_radius=0.20,
        opponent_radius_fallback=0.075,
        margin=0.10,
        near_distance=0.0,
        near_extra_margin=0.0,
        merge_gap=0.0,
        polygon_vertices=12,
    )


def test_round_obstacle_uses_safe_circumscribed_polygon():
    """The polygon boundary must stay outside the requested radius."""
    obstacle_map = ObstacleMap(obstacle_parameters())
    geometry = obstacle_map.build(
        (2.0, 2.0),
        [RoundObstacle((0.0, 0.0), 0.10)],
    )
    polygon = geometry.margin[0]

    assert point_in_polygon((0.399, 0.0), polygon, include_boundary=True)
    assert not point_in_polygon((0.401, 0.0), polygon, include_boundary=True)
    assert all(math.hypot(x, y) >= 0.40 for x, y in polygon)


def test_overlapping_round_obstacles_are_merged():
    """Inflated robot circles must not expose a false narrow passage."""
    obstacle_map = ObstacleMap(obstacle_parameters())
    geometry = obstacle_map.build(
        (3.0, 3.0),
        [
            RoundObstacle((0.0, 0.0), 0.10),
            RoundObstacle((0.5, 0.0), 0.10),
        ],
    )

    assert len(geometry.critical) == 1
    assert len(geometry.margin) == 1
    assert len(geometry.margin[0]) > 12


def test_goal_factory_creates_two_layered_u_shapes():
    """Both field goals must become critical and margin polygons."""
    goals = make_goal_obstacles(
        GoalObstacleParameters(
            enabled=True,
            field_length=9.0,
            goal_width=2.6,
            goal_depth=0.6,
            wall_width=0.1,
            back_extension=0.5,
        ),
        obstacle_parameters(),
    )

    assert len(goals) == 2
    assert all(len(goal.critical) == 8 for goal in goals)
    assert max(x for x, _ in goals[1].margin) > 4.5
    assert min(x for x, _ in goals[0].margin) < -4.5
