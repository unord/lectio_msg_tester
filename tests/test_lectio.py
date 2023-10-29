
from src.import_env import get_env_variable
from src.lectio import lectio_send_msg


def test_lectio_send_msg():


    school_id = get_env_variable('LECTIO_SCHOOL_ID')
    lectio_user =  get_env_variable('LECTIO_USER')
    lectio_password = get_env_variable('LECTIO_PASSWORD')
    send_to = 'RPA holdet Øh'
    subject = 'Dette er en test besked'
    msg = 'Dette er en test besked'
    this_msg_can_be_replied = False

    result = lectio_send_msg(school_id,
                             lectio_user,
                             lectio_password,
                             send_to, subject,
                             msg,
                             this_msg_can_be_replied,
                             True)

    assert result == {'msg': f'message sent successful to: {send_to}', 'success': True}