# Poetess

Poetress is a poetry retrieval and storage system.
It fetches poems from the poetry foundation website and
creates a local copy. Inclues the poem of the day.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install poetress.

```bash
pip install poetress
```
or if you're not into pip you can clone this repo and run this command:
```
git clone https://github.com/bwinnett12/poetress.git
python3 setup.py develop
```

## Usage
Run poetress through command line to store to a designated drive. By default, that will be
stored in "./poetry_storage which isn't anywhere if you installed through pip. If you want a self-
contained solution simply run poetess only there. You can opt to select that storage location
if you run:
```
poetess -c
```
 Otherwise, you are set up. Run poetess with the -d to grab today's poem or -f to select a
 desired specific poem. Example:
 ```
 poetess -d // Fetches the poem of the day
 poetess -f [Specific poem] // Fetches a specific poem
 poetess -c // Config wizard
 ```

If you want to reset the storage location or the max amount of characters per line
with the config wizard using -c

### Contributing
If you want to contribute, by all means make a pull request.

### License
[MIT](https://choosealicense.com/licenses/mit/)

