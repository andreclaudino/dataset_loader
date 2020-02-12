import glob
import os
import random


def _list_files(base_path: str, extension: str):
    """
    List all files in base_path subdirectories with extension
    :param base_path: root path to search files
    :param extension: extension of files searched
    :return: list of files in base_path
    """
    if base_path.endswith(os.sep):
        base_path = base_path[1:]

    search_path = os.path.join(base_path, "**", f"*.{extension}")

    return glob.iglob(search_path, recursive=True)


def _take_partitions(file_path, base_path):
    """
    Get a dictionary with partitons in filename
    :param file_path: path fot the file which will take the partitions
    :param base_path: begining of path to ignore partition generating
    :return: dictionary with partitions for the filename
    """
    sub_path = file_path.replace(base_path, "", 1)
    partitions = [part for part in sub_path.split(os.sep) if "=" in part]
    partitions_kv = [part.split("=", 1) for part in partitions]
    return {k: v for k, v in partitions_kv}


def _load_file(file_path, base_path, loader_function, ignore_partitions):
    """
     Merge the result of loading file with loader_function and the partitions
    :param file_path: path to the file which will be loaded
    :param base_path: begining of path to ignore on partition generating
    :param loader_function: function which receive file path and returns dictionary with file dataset_loader
    :return:
    """
    data = loader_function(file_path)
    if type(data) == dict:
        data = [data]
    if type(data) != list:
        raise ValueError(f"Parameter loader_function ({str(loader_function)}) "
                         f"should be a function returning `dict` or list of dict, but returned {str(type(data))}")

    if ignore_partitions:
        return data
    else:
        partitions = _take_partitions(file_path, base_path)
        return [{**partitions, **row} for row in data]


def load_dataset(base_path: str, extension: str,
                 loader_function,
                 ignore_partitions=False,
                 filter_function=lambda _: True,
                 randomize=False):
    """
    Return a generator for itens on `base_path` loaded by loader_function and filtered by ignore function
    :param base_path: Folder where files would be loaded
    :param extension: extension of files to be read
    :param loader_function: function which receive a path and return a dictionary of loaded item. (path) => dict
    :param ignore_partitions: if True, ignore partitions on resulting dictionary
    :param filter_function: A function which operates on each returning dictionary, if True, data is returned on generator
            else, data is ignored.
    :param randomize: if True, shuffle resulting list
    :return: generator of dictionaries
    """

    paths = _list_files(base_path, extension)

    if randomize:
        paths = random.shuffle(paths)

    for path in paths:
        for result in _load_file(path, base_path, loader_function, ignore_partitions):
            if filter_function(result):
                yield result
            else:
                continue
