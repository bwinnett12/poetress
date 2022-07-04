#!/usr/bin/python
import argparse
import configparser
import os
from os.path import abspath
from datetime import date
import bs4
from bs4 import BeautifulSoup
import pkg_resources
import requests

__author__ = "Bill Winnett"
__email__ = "bwinnett12@gmail.com"
__license__ = "MIT"
__version = "0.5.0"


def get_config():
    stream = pkg_resources.resource_filename(__name__, "data/poetress_config.config")
    config = configparser.ConfigParser()
    config.read(stream)
    return config


def alter_config():
    stream = pkg_resources.resource_filename(__name__, "data/poetress_config.config")
    config = configparser.ConfigParser()
    config.read(stream)

    print("Poetress configuration update. Anything blank will be left the same. \n")
    new_storage_location = input("Location for storage (currently{0}):  ".format(config['Options']['storage_location']))
    new_line_max = input("Max characters per line (currently {0}):  ".format(config['Options']["max_line_length"]))

    if new_storage_location:
        config.set("Options", "storage_location", new_storage_location)

    if new_line_max:
        config.set("Options", "max_line_length", new_line_max)

    with open(stream, 'w') as configfile:
        config.write(configfile)


# function to return the closest space that doesn't go over the max line length
def find_closest_space(s):
    for c in range(len(s) - 1, 0, -1):
        if s[c] == ' ':
            return c
    else:
        return len(s) - 1


# Returns the link for the poem of the day
def get_potd_link():
    url = "https://www.poetryfoundation.org/poems/poem-of-the-day"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Split by articles
    links = soup.find_all('a')
    potd_link = ""
    for link in links:
        if "Read More" in link.text:
            potd_link = link['href']
            break

    return potd_link


# Gets the soup for a desired poem
def get_poem_soup(url):
    headers = {
        'Host': "www.poetryfoundation.org",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        'Accept': '*/*',
        'Accept-Language': 'en-US,pt;q=0.7,en;q=0.3',
    }
    page = requests.get(url, headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


# Generates the text for the poem itself. Does not get title or author
def provide_body(soup, max_line_length):
    full_text = ""
    features = soup.find_all("div", class_="c-feature")

    raw_poem = features[0]
    raw_poem = raw_poem.find("div", class_='o-poem')

    for ton in raw_poem.contents:

        if type(ton) != bs4.element.Tag:
            continue

        for elem in ton.contents:
            if type(elem) == bs4.element.Tag:
                full_text += elem.text
                continue

            line = elem
            line = line.strip("\r")
            # Replaces fun elements that get dragged along with the html
            line = line.replace(" ", "").replace("&nbsp;", "")
            line = line.replace(" ", "").replace("&lsep;", "")

            # Variable for keeping track of index within a line
            l = 0

            # Splits lines up depending on the maximum length desired
            while l < len(line):
                if len(line[l:]) > max_line_length:
                    # Finds the length until the closest whitespace and adds that
                    offset = find_closest_space(line[l:l + max_line_length])

                    full_text += line[l:l + offset] + "\n"
                    l += offset
                else:
                    full_text += line[l:]
                    l += max_line_length
            full_text += "\n"
    return full_text


# Writes the poem to a file. Wow remarkable
def write_poem_to_file(location, poem_text, header):
    filee = open(location, "w")
    title = header[0].replace("/", "|")
    try:
        author = header[1].replace("/", "|")
    except IndexError:
        author = "misc"

    filee.write("{0} by {1}".format(title, author))
    filee.write("\n\n")

    filee.write(poem_text)
    filee.close()


# Finds a local location for the poetry
def get_file_location(folder, header):
    try:
        author = "-".join(header[1].split(" ")[::-1]).replace("/", "|")
    except IndexError:
        author = "misc"
        pass

    title = "-".join(header[0].split(" ")).replace("/", "|")

    out_loc_folder = folder + author + "/"
    out_loc = out_loc_folder + author + "_" + title + ".txt"

    os.makedirs(out_loc_folder, exist_ok=True)
    if not os.path.isfile(out_loc):
        current_file = open(out_loc, "x")

    return out_loc


# Ensures that folder is a folder and not a link to a possible file
def format_storage_folder(folder):
    return folder.rstrip("/") + "/"


# Prints fetched poem
def print_poem(file_location):
    filee = open(file_location, "r")
    for line in filee.readlines():
        print(line.replace("\n", ""))


# retrieves poem desired
def fetch_poetry(url, folder, max_line_length, print):
    folder = format_storage_folder(folder)
    poem_soup = get_poem_soup(url)
    poem_text = provide_body(poem_soup, max_line_length)
    headr = poem_soup.find("meta", {"name": "dcterms.Title"}).attrs['content'].split(" by ")
    file_location = get_file_location(folder, headr)
    write_poem_to_file(file_location, poem_text, headr)

    if print:
        print_poem(file_location)


# Fetches daily poem. Feeds into @fetch_poetry
def fetch_daily(folder, max_line_length, print):
    url = get_potd_link()
    fetch_poetry(url, folder, max_line_length, print)


def main():
    parser = argparse.ArgumentParser(description='Retrieve and store poems from Poetry Foundation')
    today = date.today()

    # All config paresed items
    parser.add_argument('-d', '--daily',
                        dest='daily',
                        default=False,
                        action='store_true',
                        help="Retrieves the poem of the day for {0}".format(today.strftime("%B %d, %Y")))

    # Argument for fetching
    parser.add_argument('-f', '--fetch',
                        dest='fetch',
                        default="",
                        help='Retrieves a specific poem from the poetry foundation: \n '
                             'Usage: -f [url of poem]')

    parser.add_argument('-c', '--config',
                        dest='config',
                        default=False,
                        action='store_true',
                        help="Wizard to reset the configuration for poetry storage")

    # All config paresed items
    parser.add_argument('-p', '--print',
                        dest='print',
                        default=False,
                        action='store_true',
                        help="Prints the poem of the day. Add to -d or -f option")

    args = parser.parse_args()
    daily = args.daily
    fetch = args.fetch
    config = args.config
    print = args.print

    # Using configparser
    configuration = get_config()
    poetry_storage = configuration['Options']['storage_location']
    poetry_storage = abspath(os.path.expanduser(poetry_storage))
    max_line_length = int(configuration['Options']['max_line_length'])

    if daily:
        fetch_daily(poetry_storage, max_line_length, print)

    if len(fetch) > 0:
        fetch_poetry(fetch, poetry_storage, max_line_length, print)

    if config:
        alter_config()


if __name__ == '__main__':
    main()
