from os.path import join, abspath, dirname


PROJECT_ROOT = join(abspath(dirname(__file__)), '..')


def root_join(*path):
    return join(abspath(PROJECT_ROOT), *path)
