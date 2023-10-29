import pytest
from src.intro import get_intro
import platform

def test_get_intro():
    docker_repo = "example_repo"
    current_version = "1.0.0"
    github_readme = "https://github.com/example_repo"
    uptime_kuma_url = "http://uptime.kuma"
    uptime_kuma_check = "5"

    expected_intro_msg = (
        "Completed importing environment variables. No errors.\n\n"
        f"Github repository: {docker_repo}:{current_version}\n"
        f"Python version: {platform.python_version()}\n"
        f"System platform: {platform.system()}\n"
        f"Documentation: {github_readme}\n\n\n"
        f"System checks health via UpTime-kuma every {uptime_kuma_check}\n"
        f"UpTime-kuma url: {uptime_kuma_url} seconds\n\n"
        "Starting main loop that check lectio messageing is working\n"
        '**************************************************************************************\n\n'
    )

    output = get_intro(
        docker_repo=docker_repo,
        current_version=current_version,
        github_readme=github_readme,
        uptime_kuma_url=uptime_kuma_url,
        uptime_kuma_check=uptime_kuma_check
    )

    assert output == expected_intro_msg

