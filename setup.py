import os
from shutil import copyfile
from subprocess import PIPE, Popen

import config


def installing_requirements():
    print('installing requirements')

    command = ['pip3', 'install', '-r', 'requirement.txt']
    process = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (output, err) = process.communicate()

    print(output)


def generating_config():
    if not os.path.exists(config.configuration_file_path):
        copyfile(config.base_configuration_file_path, config.configuration_file_path)
        print('file copied')
    else:
        print('cant setup config file:: already exist')


if __name__ == '__main__':
    installing_requirements()
    generating_config()
