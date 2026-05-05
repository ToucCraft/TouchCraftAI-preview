import pytest
from unittest.mock import patch
from services.deployer import stop_container, start_container


@patch('services.deployer.subprocess.run')
def test_stop_container_success(mock_subprocess_run):
    """
    Test: Verify that stop_container executes the correct Docker CLI command.
    """
    project_id = "test-uuid-1234"

    stop_container(project_id)

    # Assert that subprocess.run was called with correct arguments
    mock_subprocess_run.assert_called_once_with(
        ["docker", "stop", f"container-{project_id}"],
        check=True
    )


@patch('services.deployer.subprocess.run')
def test_start_container_success(mock_subprocess_run):
    """
    Test: Verify that start_container executes the correct Docker CLI command.
    """
    project_id = "test-uuid-5678"

    start_container(project_id)

    mock_subprocess_run.assert_called_once_with(
        ["docker", "start", f"container-{project_id}"],
        check=True
    )
