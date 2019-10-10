from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("LICENSE", "r") as fh:
    license = fh.read()


setup(
    name='dataset-loader',
    version='0.1',
    packages=['data_loader'],
    license=license,
    long_description=long_description,
    author="André Claudino",
    long_description_content_type="text/markdown",
    url="https://github.com/andreclaudino/dataset_loader",
    description="A simple package to load folder partitioned data",
    install_requires=['pandas']
)
