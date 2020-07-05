#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Take the brute-force shell-script snippets from kernel2 and
convert it into a python executable to deliver the
1 timestamps of all tags for all kernel versions
2 plot it with x-axis is time in some suitable unit and y-axis
is release in order.
3 Make sure that the labels on the x and y axis explain what
the data is about and use a meaningful title.

"""

__author__ = "Group No.18 in DSP of Lanzhou University: Yuming Chen, Huiyi Liu"
__copyright__ = "Copyright 2020, Study Project in Lanzhou University , China"
__license__ = "GPL V3"
__version__ = "0.1"
__maintainer__ = ["Yuming Chen", "Huiyi Liu"]
__email__ = ["chenym18@lzu.edu.cn", "liuhuiyi18@lzu.edu.cn"]
__status__ = "Experimental"

import os
import unicodedata
import re
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from subprocess import Popen, PIPE, DEVNULL
from subprocess import CalledProcessError, TimeoutExpired

# The compiler of regular expression
# Get the version of each tag
# e.g. v4.4
VERSION = re.compile('v\d+.\d+', re.IGNORECASE)
# Get the version of tag which start with v2
# e.g. v2.6.11
SPECIAL_VERSION = re.compile('v\d+.\d+.\d+', re.IGNORECASE)
LOG_PATH = 'error.log'


class InvalidPathError(EnvironmentError):
    pass


class Rep:
    """
    1. Describe:
    1.1 "Rep" class is to represent the git repository
    1.2 "execute" can run the command in the git repository

    Doctest:
    >>> rep = Rep('a')
    Traceback (most recent call last):
        ...
    repo.InvalidPathError
    >>> rep = Rep('linux-stable')
    >>> rep.execute('a',True)
    Traceback (most recent call last):
        ...
    subprocess.CalledProcessError: Command 'a' returned non-zero exit status 1.
    >>> rep.execute( ["git", "log", '--pretty=format:"%an&%h"', "--no-merges","-3"],False)
    '"Linus Torvalds&b3a9e3b9622a"\n"Thomas Cedeno&39030e1351aa"\n"David Sterba&55e20bd12a56"'
    """

    def __init__(self, path: str):
        """
        1. Describe:
        Init the git repository and check if the repository is valid

        2. Args:
        path: repository path
        """
        self.path = path
        # Verify the repository
        try:
            assert os.path.exists(os.path.join(self.path, '.git')), True
        except AssertionError:
            print('Invalid Git Repository')
            raise InvalidPathError from None

    def execute(self, cmd: str or list, shell: bool):
        """
        1. Describe:
        1.1 Run the git command and return the output.
        1.2 Deal with the timeout error and Catch the invalid reversion number.
        """
        p = Popen(cmd, stdout=PIPE, stderr=DEVNULL, shell=shell, cwd=self.path)
        try:
            outs, errs = p.communicate()
            if p.returncode:
                raise CalledProcessError(p.returncode, cmd) from None
        except TimeoutExpired:
            p.kill()
            raise RuntimeError("Timeout during get git commits") from None
        outs = unicodedata.normalize(u'NFKD', outs.decode(encoding="utf-8", errors="ignore"))
        return outs


def error_log(message: str):
    """
    1. Describe:
    Record error message when data extracting
    """
    print(message)
    with open(LOG_PATH, 'a+') as f:
        f.write(message)


def get_key(elem):
    """
    1. Describe:
    Define the key param of "sort" function which is suitable for linux tags

    2. Major targets are:
    2.1 Deal with the tags like "v4.4-rc1" and "v4.4"
    These tags are sorted and at the front of sort list.
    Therefore, return -1 to keep it as it is.

    2.2 Deal with the tags like "v4.4.1"
    Return the last number "1" of "v4.4.1"

    2.3 Deal with the tags in "v2" like "v2.6.1.100"
    Return the last number "100" of "v2.6.1.100"
    """
    try:
        re_complie = SPECIAL_VERSION if elem[1] == 2 else VERSION
        index = re_complie.match(elem).span()[1]
        return int(elem[index + 1:])
    except Exception:
        return -1


class Counter:
    """
    1. Describe:
    This is class to:
    1.1 Get all tags in suitable order for all kernel versions
    1.2 Get the timestamps of all tags
    1.3 Generate the DataFrame which contains two columns ['tag','timestamp']
    1.4 Draw the plot of days and tags
    """
    def __init__(self, path, version=None):
        self.__repo = Rep(path)
        self.__version = version
        self.__tags = {}
        self.__timestamps = {}
        self.__df = pd.DataFrame(columns=['tag', 'timestamp'])

    def get_tags(self):
        """
        1. Describe:
        Get all tags in suitable order for all kernel versions

        2. Return
        dict: {version:[tags in suitable order]}
        """
        if self.__tags:
            return self.__tags
        cmd = ["git", "tag"]
        data = self.__repo.execute(cmd, shell=False)
        for tag in data.split('\n'):
            if tag:
                version = VERSION.match(tag).group()
                if version == 'v2.6':
                    version = SPECIAL_VERSION.match(tag).group()
                self.__tags[version] = self.__tags.get(version, []) + [tag]
        for version in self.__tags:
            self.__tags[version].sort(key=get_key)
        return self.__tags

    tags = property(get_tags, None, None, 'Tags for all kernel versions')

    def get_timestamp(self):
        """
        1. Describe:
        Get the timestamp of each tag

        2. Return
        dict: {tag:timestamp}
        """
        if self.__timestamps:
            return self.__timestamps
        versions = [self.__version] if self.__version else self.tags.keys()
        for version in versions:
            for tag in self.tags[version]:
                cmd = ['git', 'log', '-1', '--pretty=format:\"%ct\"', tag]
                timestamp = self.__repo.execute(cmd, shell=False)
                if timestamp:
                    timestamp = float(timestamp[1:-1])
                else:
                    timestamp = np.nan
                self.__timestamps[tag] = timestamp
        return self.__timestamps

    timestamps = property(get_timestamp, None, None, 'Timestamps for all tags')

    def get_table(self):
        """
        1. Describe:
        Generate the DataFrame which contains two columns ['tag','timestamp']
        """
        if not self.__df.empty:
            return self.__df
        self.__df['tag'] = list(self.timestamps.keys())
        self.__df['timestamp'] = list(self.timestamps.values())
        return self.__df

    table = property(get_table, None, None, "")

    def draw(self, save_path=None):
        """
        1. Describe:
        Draw the plot of days and tags

        2. Args:
        save_path: The save path of result image
        """
        secPerDay = 3600 * 24
        x = (self.table['timestamp'] - self.table['timestamp'][0]) // secPerDay
        #plt.scatter(self.table['timestamp'].apply(lambda x:datetime.fromtimestamp(x).weekday()), self.table['tag'])
        plt.scatter(x, self.table['tag'])
        plt.title("the number of tags per version")
        plt.xlabel("days")
        plt.ylabel("tags")
        ymajor_locator = MultipleLocator(20)
        ay = plt.gca()
        ay.yaxis.set_major_locator(ymajor_locator)
        if save_path:
            try:
                plt.savefig(save_path)
            except ValueError as err:
                error_log('Invalid path: {error}-----{path}'.format(path=save_path, error=str(err)))
                raise ValueError
            except FileNotFoundError:
                error_log('Invalid path: No such file-----{path}'.format(path=save_path))
                raise InvalidPathError
        plt.show()
        plt.clf()


if __name__ == "__main__":
    path = "linux-stable"
    counter = Counter(path, version='v4.4')
    print(counter.table)
    counter.table.to_csv('v4.4.csv',index=False)
    counter.draw(save_path='V4.4.png')
