import sys
from collections import OrderedDict
from operator import itemgetter

from main_tools.housekeeping import debugPrint, set_seed
from main_tools.my_random import MY_RANDOM as random

verbose = 0
times = []


# TODO: Make sure this is actually not used anywhere then delete
def get_sample_and_discovery(in_file):
    temp_file = read_model_file(in_file)
    out_dict = dict()
    for line in temp_file:
        if line.startswith("-I"):
            line = line.split(',')
            out_dict["-I"] = [int(s.strip()) for s in line[2:] if s]
        elif line.startswith("-discovery") or line.startswith("-sample"):
            line = line.split(',')
            out_dict[line[0]] = [int(s.strip()) for s in line[1:] if s]
    return out_dict


def read_model_file(in_file):
    """
    reads the file into a list 
    :param in_file: a file name as a string
    :return: a list with each line as a single string object 
    """
    fl = open(in_file, "r")
    info = []
    tmp_seed = 0
    for line in fl:
        if line.startswith("-"):
            temp = str(line).strip()
            info.append(temp)
        if line.split(",")[0] == "-s":
            temp = str(line).strip()
            tmp_seed = temp.split(",")[1]
    set_seed(tmp_seed)
    return info


def read_params_file(in_file):
    """
    reads the file into a list
    :param in_file: a file name as a string
    :return: a list with each line as a single string object
    """
    fl = open(in_file, "r")
    model_params_dict = {}
    for line in fl:
        if "=" in line:
            model_params_dict[line.split("=")[0].strip()] = line.split("=")[1].strip()
    return model_params_dict


def get_param_value_bounded(temp_num, temp_low):
    """

    :param temp_num:
    :param temp_low:
    :return:
    """

    temp_num = temp_num.strip()
    if ":" not in temp_num:
        temp_num = str(sci_to_float(temp_num))
        return_value = str(temp_num)
    else:
        # This means you want range
        temp_low = max(float(sci_to_float(temp_num.split(":")[0][1:])), float(temp_low))
        temp_high = sci_to_float(temp_num.split(":")[1][:-1])
        return_value = str(random.uniform(float(temp_low), float(temp_high)))

    return return_value


# TODO: Confirm that this code doesn't break when you use a range without attaching it to a variable
def get_param_value_un_bounded(model_params_dict, param_key):
    """
    getParamValueUnBounded:
    This is a function that searches the model dictionary for the value
    and replace the param name with the matching param value in the param file
    If there is a value that is a given range it will pick a float in that range
    """

    assert param_key in model_params_dict, "get_param_value_un_bounded called without proper param"

    param_raw_value = model_params_dict[param_key]
    if ":" in param_raw_value:
        # This means you want range
        unscaled_param_value = prior_to_param_value(param_raw_value)
    else:
        unscaled_param_value = str(sci_to_float(param_raw_value))

    return unscaled_param_value


def prior_to_param_value(input_param_str):
    """
    priorToParamValue:
    This is a helper function that takes a string in the form (###:###)
    Numbers are allowed to be either scientific notation or base 10
    And returns a random value in that range, in the form of a string

    :param input_param_str:
    :return:
    """

    assert isinstance(input_param_str, str), "priorToParamValue called without a string"

    temp_low = float(sci_to_float(input_param_str.split(":")[0][1:]))
    temp_high = float(sci_to_float(input_param_str.split(":")[1][:-1]))
    return_value = str(random.uniform(temp_low, temp_high))

    return return_value


def sci_to_float(s):
    """
    Converts a string of the form 'aEb' into an int given by a*10^b
    """
    s = s.replace("e", "E")
    if 'E' in s:
        s = s.split('E')
        return float(s[0]) * 10**float(s[1])
    return s


def find_scale_value(flags):
    # used for scaling
    debugPrint(2, "Finding scaling value")
    ne = 10000
    if "-Ne" not in flags.keys():
        if "-n" in flags.keys():
            ne = float(flags["-n"][0][1])
    else:
        ne = float(flags['-Ne'][0][0])
    debugPrint(2, "Scaling factor found: {0}".format(ne))
    return ne


def process_time_data(flag, last_time, model_params_dict_raw, time_data_raw):
    """
    This is a helper function that takes the raw time data from the model
    file and replaces it with the correct value in the params file.

    :param flag:
    :param last_time:
    :param model_params_dict_raw:
    :param time_data_raw:
    :return:
    """

    low_time_used = False
    if "_" in flag and int(flag.split("_")[1]) == 1:
        # There is no time constraint
        low_time_used = True

    if "inst" in time_data_raw:
        temp_time = str(float(last_time) + 1)
        while temp_time in times:
            temp_time += 10
        time_data = temp_time
    else:
        if low_time_used:
            time_data = get_param_value_bounded(time_data_raw, last_time)
        else:
            if time_data_raw in model_params_dict_raw.keys():
                time_data = get_param_value_un_bounded(model_params_dict_raw, time_data_raw)
            else:
                time_data = time_data_raw

    return time_data


def populate_flags(model_data_raw):
    """
    This will fill a dictionary with keys that equal the flags, and values that
    is a list of every time (in order) the flag is used.

    :param model_data_raw:
    :return:
    """
    debugPrint(2, "Starting: populateFlags ")
    flags = OrderedDict()
    # loops through all items in modelDataRaw
    for i, argument in enumerate(model_data_raw):
        arg_split = argument.split(',')

        flag = arg_split[0]
        if flag in flags.keys():
            flags[flag].append([x.strip() for x in arg_split[1:] if x])
        else:
            flags[flag] = [[x.strip() for x in arg_split[1:] if x]]

    return flags


def define_non_time_priors(model_params_dict_raw):
    """

    :param model_params_dict_raw:
    :return:
    :TODO: This is the section of code where variables can relate to each other, issue #8
    """

    model_params_dict = {}
    for param_raw_value in model_params_dict_raw:
        # if it has _t in it, ignore for now
        if param_raw_value[-2:].lower() == "_t":
            model_params_dict[param_raw_value[:-2]+"_t"] = model_params_dict_raw[param_raw_value]
            continue
        # TODO: check to make sure value is stripped before here
        prior = model_params_dict_raw[param_raw_value]
        if ":" in prior:
            # This means you want range
            unscaled_param_value = prior_to_param_value(prior)
        else:
            unscaled_param_value = str(sci_to_float(prior))

        model_params_dict[param_raw_value] = unscaled_param_value

    return model_params_dict


def filter_out_timed_params(model_params_dict_raw):
    model_params_dict = {}
    for param in model_params_dict_raw:
        if not param.endswith("_t"):
            model_params_dict[param] = model_params_dict_raw[param]
    return model_params_dict


def define_time_priors(model_params_dict_raw, model_data_raw):
    """

    :param model_params_dict_raw:
    :param model_data_raw:
    :return:
    """
    timed_flags = []
    model_params_dict = filter_out_timed_params(model_params_dict_raw)
    for argument in filter(lambda x: x.startswith("-e"), model_data_raw):
        arg_split = argument.split(',')
        flag = arg_split[0]

        time_data_raw = arg_split[1]
        time_data = get_time_data(flag, model_params_dict_raw, time_data_raw, timed_flags)

        # find time variable
        tmp_var = ""
        for tmp_var in arg_split:
            if tmp_var.lower().endswith("_t"):
                break
        if tmp_var in model_params_dict_raw and tmp_var.endswith("_t"):
            model_params_dict[tmp_var] = time_data

        argument_list = [argument.split(",")[0], time_data]
        argument_list.extend(argument.split(",")[2:])
        argument = ",".join(argument_list)
        timed_flags.append(argument)

    return model_params_dict


def get_time_data(flag, model_params_dict_raw, time_data_raw, timed_flags):
    if timed_flags:
        last_time_value = timed_flags[-1].split(',')[1]
        time_data = process_time_data(flag, last_time_value, model_params_dict_raw, time_data_raw)
    else:
        if time_data_raw in model_params_dict_raw.keys():
            time_data = get_param_value_un_bounded(model_params_dict_raw, time_data_raw)
        else:
            time_data = time_data_raw
    return time_data


def define_priors(model_params_dict_raw, model_data_raw):
    """
    :param model_params_dict_raw:
    :param model_data_raw:
    :return:
    """

    model_params_dict = define_non_time_priors(model_params_dict_raw)

    model_params_dict = define_time_priors(model_params_dict, model_data_raw)

    return model_params_dict


def substitute_variables(model_params_variables, model_data_raw):
    """

    :param model_params_variables:
    :param model_data_raw:
    :return:
    """

    model_data_list = []
    for argument_raw in model_data_raw:
        argument_split_raw = argument_raw.split(",")
        argument_split = []
        for parameter_raw in filter(lambda x: x != "", argument_split_raw):
            parameter = parameter_raw.strip()
            if parameter in model_params_variables:
                argument_split.append(model_params_variables[parameter])
            else:
                if "inst" in parameter:
                    last_time_str = model_data_list[-1][1]
                    last_time = float(last_time_str)
                    new_time = last_time + 1
                    new_time_str = str(new_time)
                    argument_split.append(new_time_str)
                elif parameter.startswith("-e") and "_" in parameter:
                    flag = parameter.split("_")[0]
                    argument_split.append(flag)
                else:
                    argument_split.append(parameter)
        model_data_list.append(argument_split)

    # generate clean model data
    model_data = []
    for argument in model_data_list:
        model_data.append(",".join(argument))

    return model_data


def gather_pop_names(model_data_raw):
    names = []
    size = -1
    for argument in model_data_raw:
        flag = argument.split(",")[0]
        if "-n" in flag:
            names.append(argument.split(",")[2])
        if "-I" in flag:
            size_str = argument.split(',')[1]
            size = int(size_str)+1
    if not names:
        names = list(range(1, size))

    return names


def populate_sizes(flags):
    sizes = map(int, flags["-I"][0][1:])
    if sys.version_info > (3, 0):
        sizes = list(sizes)
    if '-discovery' in flags:
        for discovery_pop_str in flags["-discovery"][0]:
            discovery_pop = int(discovery_pop_str) - 1
            if "True" in flags['-random_discovery'][0]:
                sizes[discovery_pop] += random.randint(2, sizes[discovery_pop])
            else:
                sizes[discovery_pop] += sizes[discovery_pop]
    return sizes


def generate_macs_args(flags):
    """
    This is a helper function that takes the sim options and outputs the start the macs_args

    :param flags:
    :return macs_args:
    """
    macs_args = None
    if '-macs_file' in flags:
        macs_args = [flags['-macs_file'][0][0], flags['-length'][0][0], "-I", flags['-I'][0][0]]
    elif '-macsswig' in flags:
        macs_args = [flags['-macsswig'][0][0], flags['-length'][0][0], "-I", flags['-I'][0][0]]
    elif '-macs' in flags:
        macs_args = [flags['-macs'][0][0], flags['-length'][0][0], "-I", flags['-I'][0][0]]
    else:
        # This option should never be reached since it errors out in housekeeping
        print("There is no sim option given. Check your model file.")
        exit(1)
    return macs_args


def remove_ignored_flags(flags_bloated):
    """

    :param flags_bloated:
    :return:
    """
    assert isinstance(flags_bloated, OrderedDict), "Given flag value was not a OrderedDict"

    flags = OrderedDict()
    ignored_flags = ["-germline",
                     "-array",
                     "-nonrandom_discovery",
                     "-random_discovery",
                     "-pedmap"]

    for flag in flags_bloated:
        if flag not in ignored_flags:
            flags[flag] = flags_bloated[flag]
    return flags


def process_type1_flags(flags):
    # TODO Don't loop through this, instead pull out type1, ignoring the rest

    processed_data = {}

    discovery = flags.get("-discovery", None)
    if discovery:
        for argument_raw in flags['-discovery']:
            processed_data['discovery'] = [int(s.strip()) for s in argument_raw if s]

    sample = flags.get("-sample", None)
    if sample:
        for argument_raw in flags['-sample']:
            processed_data['sample'] = [int(s.strip()) for s in argument_raw if s]

    i = flags.get("-I", None)
    if i:
        for argument_raw in flags['-I']:
            processed_data['I'] = [int(s.strip()) for s in argument_raw if s]

    daf = flags.get("-daf", None)
    if daf:
        processed_data['daf'] = float(daf[0][0])

    length = flags.get("-length", None)
    if length:
        processed_data['length'] = float(length[0][0])

    macs = flags.get("-macs", None)
    if macs:
        processed_data['macs'] = macs[0][0]

    macsswig = flags.get("-macsswig", None)
    if macsswig:
        processed_data['macsswig'] = macsswig[0][0]

    return processed_data


def filter_out_type1(flags_raw):
    flags = {}
    type1_flags = [
        "-discovery",
        "-sample",
        "-daf",
        "-length",
        "-macs",
        "-I",
        "-macsswig"]
    for flag in flags_raw:
        if flag not in type1_flags:
            flags[flag] = flags_raw[flag]
    return flags


def scale_argument(flag, argument_raw, ne):
    """
    A helper function that scaled one index in the argument.
    It returns the scaled number and the index the scaled numbers goes to.
    To add more flags to this, add it to the matching index group and matching scale group
    """
    index = -1
    # Get the index for the value you are changing
    index0 = ["-t", "-r", "-G"]
    if flag in index0:
        index = 0
    index1 = ["-eM", "-g", "-eN", "-n"]
    if flag in index1:
        index = 1

    index2 = ["-en", "-eg", "-es", "-m", "-em"]
    if flag in index2:
        index = 2

    index3 = ["-em"]
    if flag in index3:
        index = 3

    assert index != -1, "scale_argument was called with a flag that is not defined in the index lists."

    param = argument_raw[index]

    # scale the number when we have it
    scale_factor1 = [
        "-em", "-eM", "-g", "-eg", "-m", "-t", "-r", "-G",
    ]
    scale_factor2 = ["-eN", "-n", "-en"]

    if flag in scale_factor1:
        scaled_param = str(float(4 * (float(param) * ne)))
    elif flag in scale_factor2:
        scaled_param = str(float((float(param) / ne)))
    else:
        scaled_param = param

    return scaled_param, index


# TODO: Make this code simpler
def scale_flags(flags_raw):

    # find scale value
    ne = find_scale_value(flags_raw)

    flags = {}

    for flag in flags_raw.keys():
        # Looping through every key
        debugPrint(3, "FLAG:  {}: {}".format(flag, flags_raw[flag]))
        arguments = []
        for argument_raw in flags_raw[flag]:

            argument = generate_argument(argument_raw, flag, ne)

            arguments.append(argument)
        flags[flag] = arguments

    return flags


def generate_argument(argument_raw, flag, ne):
    type2_flags = [
        "-em", "-eM", "-g", "-eN", "-n", "-en",
        "-eg", "-es", "-m", "-t", "-r", "-G"
    ]
    argument = []
    if flag.startswith('-e'):
        # all <t>'s are scaled
        scaled_time = str(round(float(argument_raw[0])) / (4 * ne))
        argument.append(scaled_time)

    if flag in type2_flags:
        scaled_param, index = scale_argument(flag, argument_raw, ne)
        append_argument(argument, argument_raw, flag, index, scaled_param)

    # These scales are difference since they scale all possible values in list
    # TODO: I really don't think ema and ma flags work, get a test to test them
    if flag == "-ema":
        argument = argument_raw[:1]
        for param in argument_raw[2:]:
            argument.append(str(float(4 * (float(param) * ne))))

    elif flag == "-ma":
        argument = argument_raw[0]
        for param in argument_raw:
            argument.append(str(float(4 * (float(param) * ne))))

    if not argument:
        for param in argument_raw:
            argument.append(param)

    if len(argument) == 1 and flag.startswith("-e"):
        for param in argument_raw[1:]:
            argument.append(param)
    return argument


def append_argument(argument, argument_raw, flag, index, scaled_param):
    for i, param in enumerate(argument_raw):
        if i != index:
            if flag.startswith('-e') and i == 0:
                # TODO: figure out how to "not" this correctly
                pass
            else:
                argument.append(param)
        else:
            argument.append(scaled_param)


def add_events_to_seasons(flags):
    seasons = []
    for flag in flags.keys():
        # Looping through every key
        for argument_raw in flags[flag]:
            if flag.startswith('-e'):
                seasons.append([flag] + argument_raw)
    return seasons


def filter_out_events(flags_raw):
    flags = {}
    for flag in flags_raw:
        if not flag.startswith('-e'):
            flags[flag] = flags_raw[flag]
    return flags


def populate_macs_args(macs_args, scaled_flags):
    for flag in scaled_flags.keys():
        # Looping through every key
        debugPrint(3, "FLAG:  {}: {}".format(flag, scaled_flags[flag]))
        for argument_raw in scaled_flags[flag]:
            # Looping through every argumentRaw
            try:
                debugPrint(3, flag + ": " + str(argument_raw))

                macs_args.append(flag.strip())
                for sub_line in argument_raw:
                    macs_args.append(sub_line.strip())
            except IndexError:
                print("There was an index error!\nThis most likely means your input file has a malformed flag.")
                print("Try running with -vv argument for last flag ran")
                sys.exit()


def process_input_files(param_file, model_file, args):
    """

    :param param_file:
    :param model_file:
    :param args:
    :return:
    """
    """
    This is the function that takes links to two files and outputs a dictionary (processedData)
    With all the (useful) data in the two files
    """
    debugPrint(2, "Starting processInputFiles")

    model_data_raw = read_model_file(model_file)
    debugPrint(2, "Finished reading " + str(model_file))
    debugPrint(3, "Raw input data into make_args", model_data_raw)

    model_params_dict_raw = read_params_file(param_file)
    debugPrint(2, "Finished reading " + str(param_file))
    debugPrint(3, "Raw Output for modelParamsDict", model_params_dict_raw)

    # defining and replacing the variables from the param file
    model_params_variables = define_priors(model_params_dict_raw, model_data_raw)
    model_data = substitute_variables(model_params_variables, model_data_raw)

    flags = populate_flags(model_data)

    macs_args = generate_macs_args(flags)

    # find and add sizes to macs_args
    sizes = populate_sizes(flags)

    total = float(sum(sizes))
    macs_args.insert(1, str(total))
    sizes_str = map(str, sizes)
    if sys.version_info > (3, 0):
        sizes_str = list(sizes_str)
    macs_args.extend(sizes_str)

    debugPrint(3, "Processing flags in for macs_args")

    # take out ignored flags
    flags = remove_ignored_flags(flags)

    # take out process data )type 1
    processed_data = process_type1_flags(flags)
    flags = filter_out_type1(flags)

    # scale values if needed
    scaled_flags = scale_flags(flags)

    # pull out seed
    seed = scaled_flags.get("-s", None)
    if seed:
        processed_data['seed'] = seed

    # seasons is all the time based events
    seasons = add_events_to_seasons(scaled_flags)
    macs_args_flags = filter_out_events(scaled_flags)

    # add to macs_args
    # TODO: This needs to be done explictily
    populate_macs_args(macs_args, macs_args_flags)

    pop_names = gather_pop_names(model_data_raw)
    processed_data['name'] = pop_names

    if not processed_data.get('discovery') or not processed_data.get('sample') or not processed_data.get('daf'):
        if not processed_data.get('discovery') and not processed_data.get('sample') and not processed_data.get('daf'):
            debugPrint(2, "discovery, sample, and daf are all missing")
        else:
            print("discovery, sample, or daf is missing")
            quit()

    debugPrint(2, "Adding events data back to flag pool")
    for i in range(len(seasons)):
        seasons[i][1] = float(seasons[i][1])
    seasons = sorted(seasons, key=itemgetter(1))
    for i in range(len(seasons)):
        seasons[i][1] = str(seasons[i][1])
    for season in seasons:
        macs_args.extend(season)

    processed_data["macs_args"] = macs_args

    debugPrint(3, "printing model_params_variables:", model_params_variables)

    processed_data['param_dict'] = model_params_variables

    if args['genetic map']:
        processed_data['macs_args'].extend(['-R', args['genetic map']])

    return processed_data
