# local imports
import import_env, intro, lectio, read_version, uptime_kuma

# 3rd party imports
from datetime import datetime
import time



# import environment variables
DOCKER_REPO = import_env.get_env_variable("DOCKER_REPO")
GITHUB_README = import_env.get_env_variable("GITHUB_README")
UPTIME_KUMA_URL = import_env.get_env_variable("UPTIME_KUMA_URL")
UPTIME_KUMA_URL_CHECK = import_env.get_env_variable("UPTIME_KUMA_URL_CHECK")
LECTIO_USER = import_env.get_env_variable("LECTIO_USER")
LECTIO_PASSWORD = import_env.get_env_variable("LECTIO_PASSWORD")
LECTIO_SCHOOL_ID = import_env.get_env_variable("LECTIO_SCHOOL_ID")
MAIN_LOOP_TIME = import_env.get_env_variable("LECTIO_SCHOOL_ID")

# get current version
CURRENT_VERSION = read_version.get_version()





def main():
    print(intro.get_intro(DOCKER_REPO, GITHUB_README, CURRENT_VERSION, UPTIME_KUMA_URL, UPTIME_KUMA_URL_CHECK))
    while True:
        lectio.lectio_send_msg(LECTIO_SCHOOL_ID,
                               LECTIO_USER,
                               LECTIO_PASSWORD,
                               'RPA holdet Øh',
                               'Hourly msg test',
                               f'This is an hourly test msg from the docker container. Time: {datetime.now()}',
                               False,
                               True)
        print(f'Hourly test msg to Lectio. Time: {datetime.now()}')
        print(uptime_kuma.push_health_check(UPTIME_KUMA_URL))

        time.sleep(int(MAIN_LOOP_TIME))



if __name__ == '__main__':
    main()