## Data Loader
A python library to load partitioned data (like in spark data frames).

# Changelog
Last version is [1.6](https://pypi.org/project/dataset-loader/) released on *2019/11/18*.

* Now loader_function may return a `dict` or a `list of dict`.
* Correct a bug when base_path ends with a directory separator


## Installation
To install using pypi:

`pip install dataset-loader`

## Why this is useful?
As a Big Data software developer, I usually face huge data sets, it's complicated for maintaining and using, once, I have to deal with all data before filter it.

Hadoop ecosystem solved this problem using partitions, a folder structure to keep data with the same value for the partition columns, making it easier to access data and load it back.

For example, a partitioned data separated by values of variables *gx* and *gy* is shown there:

```
output  
├── gx=3  
│   ├── gy=1  
│   └── gy=2  
└── gx=4  
    ├── gy=2  
    └── gy=3  
```

Softwares like spark write data in this format, but it's difficult to consume for example in tools like pandas, which doesn't have support for partitioned data.

## How to use
You just need to import the `from dataset_loader.loader import load_dataset` function, which returns a generator of dictionaries or the class `data.Dataset`, where data is load, the property `rows` give you a generator (like in `load_dataset`), or the function `.to_pandas()` which gives you a pandas dataframe, both have the same signature.

```python
from dataset_loader import Dataset

data_source = Dataset(base_path = "/path/to/data/directory", extension="csv", loader_function=_loader_function , ignore_partitions=False)

# Print data
for row in data_source.rows:
    print(row)
    
# Convert to pandas
data_frame = data_source.to_pandas()    
```

or

```python
from dataset_loader.loader import load_dataset

generator = load_dataset(base_path = "/path/to/data/directory", extension="csv", loader_function=_loader_function, ignore_partitions=False)

for row in generator:
    print(row)
```


here:

* `base_path` is the path for the directory containing a partitioned data structure
* `extension` is the extension of files to load
* `loader_function` is a function which knows how to load a single file and return in a dictionary format
* `ignore_partitions`, if `True`, the partitions discovered will not be inserted in data as columns. (defaults to False)
* `filter_function`, a function which read resulting dictionary and includes only True resultants on generator. Defaults to `lambda _: True`.
* `randomize`: if `True`, will randomize itens before returning. Default is `False`.  

An example of `loader_function` for numpy *npy* files which contains a single dictionary is:

```python
import numpy as np

def loader_function(filename):
    data = np.load(filename, allow_pickle=True)
    return data[0]
```

An example of `filter_function` which ignores all data with value `gx='3'`:
```python
def filter_function(loaded_item):
    return loaded_item['gx'] != '3'
```

## Help is needed

Help in developing or increasing the library. Give us a star, open issues and help coding. Every help is welcome.
