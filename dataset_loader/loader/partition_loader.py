import glob
import os


def _list_files(base_path: str, extension: str):
    """
    List all files in base_path subdirectories with extension
    :param base_path: root path to search files
    :param extension: extension of files searched
    :return: list of files in base_path
    """
    if base_path.endswith(os.sep):
        base_path = base_path[:1]

    search_path = os.path.join(base_path, "**", f"*.{extension}")
    return glob.glob(search_path, recursive=True)


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

    if ignore_partitions:
        return data
    else:
        partitions = _take_partitions(file_path, base_path)
        return {**partitions, **data}


def load_dataset(base_path: str, extension: str, loader_function, ignore_partitions=False):
    paths = _list_files(base_path, extension)

    for path in paths:
        yield _load_file(path, base_path, loader_function, ignore_partitions)
