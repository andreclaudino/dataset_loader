from .loader import load_dataset
import pandas as pd

class Dataset:

    def __init__(self, base_path: str, extension: str, loader_function, ignore_partitions=False):

        self._base_path = base_path
        self._extension = extension
        self._loader_function = loader_function
        self._ignore_partitions = ignore_partitions

        self._rows = self._load()

    def _load(self):
        return load_dataset(self._base_path, self._extension, self._loader_function, self._ignore_partitions)

    @property
    def rows(self):
        return self._rows

    def to_pandas(self):
        return pd.DataFrame([row for row in self._load()])
