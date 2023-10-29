
from src.import_env import get_env_variable



def test_get_env_variable_from_dotenv(mocker):
    mocker.patch('decouple.config', return_value='value_from_dotenv')
    result = get_env_variable('LECTIO_USER')
    assert result == 'kney'


def test_get_env_variable_from_os(mocker):
    mocker.patch('decouple.config', side_effect=KeyError('Not found'))
    mocker.patch('os.getenv', return_value='value_from_os')
    result = get_env_variable('LECTIO_USER')
    assert result == 'kney'



