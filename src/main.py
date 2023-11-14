# 3rd party imports
from datetime import datetime
import time

import import_env
import intro
import lectio
import read_version
import uptime_kuma

# import environment variables
DOCKER_REPO = import_env.get_env_variable("DOCKER_REPO")
GITHUB_README = import_env.get_env_variable("GITHUB_README")
UPTIME_KUMA_URL = import_env.get_env_variable("UPTIME_KUMA_URL")
UPTIME_KUMA_URL_CHECK = import_env.get_env_variable("UPTIME_KUMA_URL_CHECK")
LECTIO_USER = import_env.get_env_variable("LECTIO_USER")
LECTIO_PASSWORD = import_env.get_env_variable("LECTIO_PASSWORD")
LECTIO_SCHOOL_ID = import_env.get_env_variable("LECTIO_SCHOOL_ID")
MAIN_LOOP_TIME = import_env.get_env_variable("MAIN_LOOP_TIME")

# get current version
CURRENT_VERSION = read_version.get_version()


def test_lectio_send_msg():
    lectio_session = lectio.LectioBot(LECTIO_SCHOOL_ID, LECTIO_USER, LECTIO_PASSWORD, False)
    lectio_session.start_playwright()
    lectio_session.login_to_lectio()
    lectio_session.navigate_to_messages()
    lectio_session.send_message('RPA holdet Øh',
                                'Hourly msg test',
                                f'This is an hourly test msg from the docker container. Time: {datetime.now()}',
                                False,
                                )
    lectio_session.stop_playwright()


def main():
    print(intro.get_intro(DOCKER_REPO, CURRENT_VERSION, GITHUB_README, UPTIME_KUMA_URL, UPTIME_KUMA_URL_CHECK))
    while True:
        try:
            test_lectio_send_msg()
            uptime_kuma.push_health_check(UPTIME_KUMA_URL)
            print('Message sent successfully')
            print('Sleeping for 1 hour')
            time.sleep(int(MAIN_LOOP_TIME))
        except Exception as e:
            print(f'Error in main loop: {e}')
            print('Sleeping for 5 minutes')
            time.sleep(60*5)


if __name__ == '__main__':
    main()
