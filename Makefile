SHELL := /bin/bash
.SHELLFLAGS := -e -o pipefail -c
.ONESHELL:
.DEFAULT_GOAL := help

REPOSITORY_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
WORKSPACE_DIR := $(abspath $(REPOSITORY_DIR)/../..)
ROS_SETUP := /opt/ros/jazzy/setup.bash

PATH_PLANNING_PACKAGES := field_coordinate_adapter humanoid_path_planner
COLCON_BUILD_ARGS ?= --symlink-install
ARGS ?=

.PHONY: help build-path-planning test-path-planning start-path-planning

help:
	@printf '%s\n' \
		'make build-path-planning  - adapter와 path planner 빌드' \
		'make test-path-planning   - adapter와 path planner 테스트' \
		'make start-path-planning  - adapter와 path planner 실행' \
		'make start-path-planning ARGS="..." - launch 인자 전달'

build-path-planning:
	test -f "$(ROS_SETUP)"
	source "$(ROS_SETUP)"
	cd "$(WORKSPACE_DIR)"
	colcon build $(COLCON_BUILD_ARGS) \
		--packages-select $(PATH_PLANNING_PACKAGES)

test-path-planning:
	test -f "$(ROS_SETUP)"
	source "$(ROS_SETUP)"
	cd "$(WORKSPACE_DIR)"
	colcon test --packages-select $(PATH_PLANNING_PACKAGES)
	colcon test-result --verbose

start-path-planning:
	bash "$(REPOSITORY_DIR)/scripts/start_path_planning.sh" $(ARGS)
