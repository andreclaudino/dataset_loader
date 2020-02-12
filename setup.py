from setuptools import setup, find_packages


setup(
    name='dataset-loader',
    version='1.5',
    packages=find_packages(),
    license=license,
    long_description_content_type="text/markdown",
    # long_description=long_description,
    author="André Claudino",
    url="https://github.com/andreclaudino/dataset_loader",
    description="Load partitioned data from multilevel folder structure",
    setup_requires=['wheel', 'twine'],
    install_requires=['pandas']
)
