"""Tests for visibility edges and Euclidean A* behavior."""

from humanoid_path_planner.core.obstacle import ObstacleGeometry
from humanoid_path_planner.core.visibility_graph import shortest_path


def test_direct_path_without_obstacles():
    """An empty map must produce the direct Euclidean path."""
    result = shortest_path(
        (0.0, 0.0),
        (2.0, 0.0),
        ObstacleGeometry((), ()),
        critical_cost_multiplier=10.0,
    )

    assert result is not None
    assert result.points == ((0.0, 0.0), (2.0, 0.0))


def test_path_routes_around_polygon():
    """A wall across the direct path must introduce detour vertices."""
    wall = ((0.8, -0.5), (1.2, -0.5), (1.2, 0.5), (0.8, 0.5))
    result = shortest_path(
        (0.0, 0.0),
        (2.0, 0.0),
        ObstacleGeometry((wall,), (wall,)),
        critical_cost_multiplier=10.0,
    )

    assert result is not None
    assert len(result.points) > 2
    assert any(abs(y) >= 0.5 for _, y in result.points)


def test_goal_inside_critical_obstacle_has_no_path():
    """The planner must not deliberately finish inside another robot."""
    obstacle = ((0.8, -0.5), (1.2, -0.5), (1.2, 0.5), (0.8, 0.5))
    result = shortest_path(
        (0.0, 0.0),
        (1.0, 0.0),
        ObstacleGeometry((obstacle,), (obstacle,)),
        critical_cost_multiplier=10.0,
    )

    assert result is None


def test_start_inside_obstacle_gets_best_effort_escape():
    """A localized robot inside an obstacle must still receive an exit path."""
    obstacle = ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5))
    result = shortest_path(
        (0.0, 0.0),
        (2.0, 0.0),
        ObstacleGeometry((obstacle,), (obstacle,)),
        critical_cost_multiplier=10.0,
    )

    assert result is not None
    assert result.points[0] == (0.0, 0.0)
    assert result.points[-1] == (2.0, 0.0)
