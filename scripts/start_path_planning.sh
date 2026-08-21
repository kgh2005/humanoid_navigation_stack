#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd -- "${SCRIPT_DIR}/../../.." && pwd)"

source /opt/ros/jazzy/setup.bash
source "${WORKSPACE_DIR}/install/setup.bash"

exec ros2 launch \
  humanoid_path_planner \
  path_planning_with_adapter.launch.py \
  "$@"