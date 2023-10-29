import pytest
from src.uptime_kuma import push_health_check
from src.import_env import get_env_variable
from unittest.mock import patch, MagicMock  # Importing MagicMock here

def test_push_health_check_success(mocker):
    # Mock requests.get to return a successful response
    mocker.patch('requests.get', return_value=MagicMock(status_code=200))

    # Call the function
    push_health_check(get_env_variable('UPTIME_KUMA_URL'))

    # If it reaches here without exceptions, it's assumed to be a success


def test_push_health_check_fail(mocker):
    # Mock requests.get to raise an exception
    mocker.patch('requests.get', side_effect=Exception('An error occurred'))

    # Mock icecream to capture the output
    ic_mock = mocker.patch('src.uptime_kuma.ic')

    # Call the function
    push_health_check('http://wrong_url.com')

    # Check if the ic function was called with the expected arguments
    ic_mock.assert_any_call('Error in push_health_check: An error occurred')
    ic_mock.assert_any_call('web_address: http://wrong_url.com')

