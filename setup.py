from setuptools import setup, find_packages

VERSION = '0.5.1'
DESCRIPTION = 'Poetry Storage and Retrieval'
LONG_DESCRIPTION = 'Retrieves poems from the poetry foundation website'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="poetress",
    version=VERSION,
    author="Bill Winnett",
    author_email="<bwinnett12@gmail.com>",
    url="https://github.com/bwinnett12/poetress",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    entry_points={
        'console_scripts': ['poetress=poetress.poetress:main'],
    },
    packages=find_packages(),
    install_requires=['bs4==0.0.1',
                      # 'beautifulsoup>=4.1.1',
                      'requests~=2.26.0',
                      'setuptools~=59.8.0'],
    include_package_data=True,
    keywords=['python', 'poetess'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
    ]
)