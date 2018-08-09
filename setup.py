import os
from shutil import copyfile
from subprocess import PIPE, Popen

import kankei_paths


def installing_requirements():
    print('installing requirements')

    command = ['pip3', 'install', '-r', 'requirement.txt']
    process = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (output, err) = process.communicate()

    print(output)


def generating_config():
    if not os.path.exists(kankei_paths.CONF_PATH):
        copyfile(kankei_paths.EX_CONF_PATH, kankei_paths.CONF_PATH)
        print('file copied')
    else:
        print('cant setup config file:: already exist')


if __name__ == '__main__':
    installing_requirements()
    generating_config()
