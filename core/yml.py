# -*- coding: utf-8 -*-
import yaml


def open_yml(path=None, mode='r'):
    """ Open a yaml file and return data from it.

    :param: path: Path to yaml file
    :param: mode: Opening file mode
    :type: path: str
    :type: mode: str
    :return: Data from yaml file
    :rtype: dict
    """
    with open(path, mode) as yml_fd:
        data = YamlHandler(yml_fd).load_yaml()
    yml_fd.close()
    return data


def write_yml(path=None, mode='w', data=None):
    """ Write an Object to a yaml file.

    :param: path: Path to yaml file
    :param: mode: Opening file mode
    :param: data: Object that we need to write
    :type: path: str
    :type: mode: str
    :type: data: Object (Profile, Plateform, Type)
    :return: Object wrote
    :rtype: Object
    """
    datadict = dict(data)

    with open(path, mode) as yml_fd:
        YamlHandler(yml_fd).write_yaml(datadict)
    yml_fd.close()
    return data


def rename_yml(oldpath=None, newpath=None):
    """ rename a yaml file.

    :param: oldpath: old path to yaml file
    :param: newpath: new path to yaml file
    :type: oldpath: str
    :type: oldpath :str
    :return: new path to yaml file
    :rtype: str
    """
    from os import rename
    rename(oldpath, newpath)
    return newpath


def remove_yml(path=None):
    """ remove a yaml file.

    :param: path: path to yaml file
    :type: path: str
    :return: path to removed yaml file
    :rtype: str
    """
    from os import remove
    remove(path)
    return path


class YamlHandler:
    """ Base class who manage loading and writing data to yaml file.

        :param: fd: yaml file descriptor
        :type: fd: File Descriptor Object
     """

    def __init__(self, fd):
        self.fd = fd

    def load_yaml(self):
        """ Read file from a file descriptor and load data to dict.

        :return: data loaded from yaml file
        :rtype: dict
        """
        try:
            data = yaml.safe_load(self.fd)
            return data
        except yaml.YAMLError as ye:
            print "Error in configuration file:", ye
            exit(1)
        except IOError as ioe:
            print "Error during data loading: ", ioe
            exit(1)

    def write_yaml(self, data):
        """ Write data to yaml file.

        :return: data write to yaml file
        :rtype: dict
        """

        try:
            if isinstance(data, dict):
                yaml.safe_dump(data, self.fd, default_flow_style=False, indent=4)
                return data
            else:
                raise TypeError
        except IOError as ioe:
            print "Error during data writing: ", ioe
            exit(1)
        except yaml.YAMLError as ye:
            print "Error in configuration file:", ye
            exit(1)
        except TypeError as te:
            print "Only dictionnary can be write on yaml file :", te
            exit(2)

    def close_yaml(self):
        """ Close properly the file descriptor opened."""
        self.fd.close()
