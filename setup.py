from setuptools import setup, find_packages

VERSION = '0.3.3'
DESCRIPTION = 'Poetry Storage and Retrieval'
LONG_DESCRIPTION = 'Retrieves poems from the poetry foundation website'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="poetress",
    version=VERSION,
    author="Bill Winnett",
    author_email="<bwinnett12@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'poetess'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
    ]
)