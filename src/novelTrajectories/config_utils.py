#!/usr/bin/env python
import rospy
import sys, os, getpass
import ConfigParser


def get_path():
    user = getpass.getuser()
    data_dir = os.path.join('/home/' + user + '/STRANDS/')
    check_dir(data_dir)

    path = os.path.dirname(os.path.realpath(__file__))
    config_path =  os.path.join(path + '/config.ini')
    config_parser = ConfigParser.SafeConfigParser()
    print(config_parser.read(config_path))

    if len(config_parser.read(config_path)) == 0:
        raise ValueError("Config file not found, please provide a config.ini file as described in the documentation")

    return data_dir, config_path


def get_map_config(config_path):
    config_parser = ConfigParser.SafeConfigParser()
    print(config_parser.read(config_path))
    config_section = "soma"
    try:
        map = config_parser.get(config_section, "soma_map")
        config = config_parser.get(config_section, "soma_config")
    except ConfigParser.NoOptionError:
         raise
    return (map, config)


def check_dir(directory):
    if not os.path.isdir(directory):
        os.system('mkdir -p ' + directory)
    return


def get_qsr_config(multiple_qsrs=False):
    data_dir, config_path = get_path()

    config_parser = ConfigParser.SafeConfigParser()
    config_parser.read(config_path)
    config_section = "trajectory_data_reader"

    try:
        date = config_parser.get(config_section, "date")
        qsr = config_parser.get(config_section, "qsr")
    except ConfigParser.NoOptionError:
        raise

    if qsr == "arg_distance_qtcb_comb":
        print("Arg Distance and QTCb Combined")

        try:
            touch = config_parser.getfloat(config_section, "touch")
            near = config_parser.getfloat(config_section, "near")
            medium = config_parser.getfloat(config_section, "medium")
            far = config_parser.getfloat(config_section, "far")
            ignore = config_parser.getfloat(config_section, "ignore")
            qsr_values = {"touch":touch, "near":near, "medium":medium, "far":far, "ignore":ignore}

            q = config_parser.getfloat(config_section, "q")
            v = config_parser.getboolean(config_section, "v")
            n = config_parser.getboolean(config_section, "n")

            params = (["arg_distance", qsr_values], ["qtcb", q, v, n])

        except ConfigParser.NoOptionError:
            raise


    if qsr == "qtcb":
        print("QTCb requested")
        try:
            q = config_parser.getfloat(config_section, "q")
            v = config_parser.getboolean(config_section, "v")
            n = config_parser.getboolean(config_section, "n")
            params = [qsr, q, v, n]
        except ConfigParser.NoOptionError:
            raise

    if qsr == "rcc3":
        print("RCC3 requested")
        params = [qsr]

    if qsr == "arg_distance":
        print("Distance QSRs requested")
        config_section = "qsr_relations_and_values"
        try:
            #values = config_parser._sections['qsr_relations_and_values']
            #for i, val in values.items():
            #    print(i, val)

            touch = config_parser.getfloat(config_section, "touch")
            near = config_parser.getfloat(config_section, "near")
            medium = config_parser.getfloat(config_section, "medium")
            far = config_parser.getfloat(config_section, "far")
            ignore = config_parser.getfloat(config_section, "ignore")
            qsr_values = {"touch":touch, "near":near, "medium":medium, "far":far, "ignore":ignore}
            params = [qsr, qsr_values]
        except ConfigParser.NoOptionError:
            raise

    return data_dir, config_path, params, date



def get_learning_config():
    data_dir, config_path = get_path()

    qsr = os.path.join(data_dir, 'qsr_dump/')
    trajs = os.path.join(data_dir, 'trajectory_dump/')
    graphs = os.path.join(data_dir, 'AG_graphs/')
    learning_area = os.path.join(data_dir, 'learning/')

    check_dir(qsr)
    check_dir(trajs)
    check_dir(graphs)
    check_dir(learning_area)

    directories = (data_dir, qsr, trajs, graphs, learning_area)

    config_parser = ConfigParser.SafeConfigParser()
    config_parser.read(config_path)
    config_section = "activity_graph_options"
    try:
        input_data={}
        date = config_parser.get(config_section, "date")
        input_data['MAX_ROWS'] = config_parser.get(config_section, "MAX_ROWS")
        input_data['MIN_ROWS'] = config_parser.get(config_section, "MIN_ROWS")
        input_data['MAX_EPI']  = config_parser.get(config_section, "MAX_EPI")
        input_data['num_cores'] = config_parser.get(config_section, "num_cores")

    except ConfigParser.NoOptionError:
        raise

    return (directories, config_path, input_data, date)



if __name__ == "__main__":
    params = get_qsr_config()
    print params, "\n"

    (directories, config_path, input_data, date) =  get_learning_config()
    print directories, "\n"

    (map, config) = get_map_config(config_path)
    print map, config
