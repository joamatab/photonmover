import yaml
import importlib


def parse_instr_yaml_file(filename):
    """
    Parses the instrument yaml file, creates the instrument objects
    and returns a list with all of them
    """

    with open(filename) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        instr_list = yaml.load(file, Loader=yaml.FullLoader)
        instr_name_list = instr_list["Instruments"]

    instr_obj_list = []

    # Create each instrument and add it to the list
    for instr_dict in instr_name_list:

        cl_name = instr_dict["class_name"]

        instr_module = importlib.import_module(instr_dict["class_package"])
        cl = getattr(instr_module, cl_name)

        if (
            "class_params" in instr_dict
            and instr_dict["class_params"] is not None
        ):
            cl_params = instr_dict["class_params"]
            instr = cl(**cl_params)
        else:
            instr = cl()
        instr_obj_list.append(instr)

    vars_list = instr_list["Setup"] if "Setup" in instr_list else None
    return instr_obj_list, vars_list
