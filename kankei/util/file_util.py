import os
import shutil


def reset_dir(*paths):
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)


def delete_if_exist(*paths):
    for path in paths:
        if path.exists():
            shutil.rmtree(path)
