"""End-to-end tests for the ROS-independent Planner API."""

from humanoid_path_planner.obstacle import RoundObstacle
from humanoid_path_planner.parameters import (
    BallParameters,
    GoalObstacleParameters,
    ObstacleParameters,
    PlanningParameters,
    TopicParameters,
)
from humanoid_path_planner.planner import Planner


def planner_parameters() -> PlanningParameters:
    """Return a planner configuration without static field goals."""
    return PlanningParameters(
        frame_id='map',
        replan_hz=10.0,
        zero_pose_is_invalid=True,
        critical_cost_multiplier=10.0,
        path_resolution=0.1,
        show_visibility_graph=False,
        topics=TopicParameters(
            robot='robot',
            target='target',
            obstacles='obstacles',
            ball='ball',
            ball_obstacle_active='avoid_ball',
            path='path',
            markers='markers',
        ),
        obstacle=ObstacleParameters(
            robot_radius=0.20,
            opponent_radius_fallback=0.075,
            margin=0.10,
            near_distance=0.0,
            near_extra_margin=0.0,
            merge_gap=0.02,
            polygon_vertices=12,
        ),
        ball=BallParameters(radius=0.05, avoid=False),
        goal_obstacle=GoalObstacleParameters(
            enabled=False,
            field_length=9.0,
            goal_width=2.6,
            goal_depth=0.6,
            wall_width=0.1,
            back_extension=0.5,
        ),
    )


def test_planner_densifies_direct_path():
    """The public planner must preserve endpoints and bound point spacing."""
    result = Planner(planner_parameters()).plan(
        (0.0, 0.0),
        (1.0, 0.0),
        (),
    )

    assert result.successful
    assert result.path[0] == (0.0, 0.0)
    assert result.path[-1] == (1.0, 0.0)
    assert len(result.path) == 11


def test_planner_avoids_round_opponent():
    """A perceived opponent on the direct path must cause a detour."""
    result = Planner(planner_parameters()).plan(
        (0.0, 0.0),
        (2.0, 0.0),
        (RoundObstacle((1.0, 0.0), 0.10),),
    )

    assert result.successful
    assert any(abs(y) > 0.30 for _, y in result.path)


def test_ball_obstacle_toggle_does_not_remove_other_state():
    """The same ball should affect the path only when avoidance is active."""
    planner = Planner(planner_parameters())
    ball = RoundObstacle((1.0, 0.0), 0.05)
    direct = planner.plan(
        (0.0, 0.0),
        (2.0, 0.0),
        (),
        ball=ball,
        avoid_ball=False,
    )
    detour = planner.plan(
        (0.0, 0.0),
        (2.0, 0.0),
        (),
        ball=ball,
        avoid_ball=True,
    )

    assert all(abs(y) < 1.0e-9 for _, y in direct.path)
    assert any(abs(y) > 0.0 for _, y in detour.path)
