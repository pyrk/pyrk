# -*- coding: utf-8 -*-
# Author: Douglas Creager <dcreager@dcreager.net>
# This file is placed into the public domain.

# Calculates the current version number.  If possible, this is the
# output of “git describe”, modified to conform to the versioning
# scheme that setuptools uses.  If “git describe” returns an error
# (most likely because we're in an unpacked copy of a release tarball,
# rather than in a git working copy), then we fall back on reading the
# contents of the RELEASE-VERSION file.
#
# To use this script, simply import it your setup.py file, and use the
# results of get_git_version() as your package version:
#
# from version import *
#
# setup(
#     version=get_git_version(),
#     .
#     .
#     .
# )
#
# This will automatically update the RELEASE-VERSION file, if
# necessary.  Note that the RELEASE-VERSION file should *not* be
# checked into git; please add it to your top-level .gitignore file.
#
# You'll probably want to distribute the RELEASE-VERSION file in your
# sdist tarballs; to do this, just create a MANIFEST.in file that
# contains the following line:
#
#   include RELEASE-VERSION

from __future__ import print_function
__all__ = ["get_git_version"]

from subprocess import Popen, PIPE


def call_git_describe():
    try:
        p = Popen(['git', 'describe', ],
                  stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0]
        return line.strip()

    except BaseException:
        return None


def read_release_version():
    try:
        f = open("RELEASE-VERSION", "rt")

        try:
            v = f.readlines()[0]
            return v.strip()

        finally:
            f.close()

    except BaseException:
        return None


def write_release_version(v):
    f = open("RELEASE-VERSION", "w")
    f.write("%s\n" % v)
    f.close()


def get_git_version():
    # Read in the version that's currently in RELEASE-VERSION.
    release_version = read_release_version()

    # First try to get the current version using “git describe”.
    v = call_git_describe()

    # adapt to PEP 440 compatible versioning scheme
    v = pep440adapt(v)

    # If that doesn't work, fall back on the value that's in
    # RELEASE-VERSION.
    if v is None:
        v = release_version

    # If we still don't have anything, that's an error.
    if v is None:
        raise ValueError("Cannot find the version number!")

    # If the current version is different from what's in the
    # RELEASE-VERSION file, update the file to be current.
    if v != release_version:
        write_release_version(v)

    # Finally, return the current version.
    return v.decode('utf-8')


def pep440adapt(v):
    dash = b'-'
    if v is not None and dash in v:
        # adapt git-describe version to be in line with PEP 440
        # by setting a dev release identifier
        parts = v.split(dash)
        parts[-2] = b'dev' + parts[-1].lstrip(b'g')
        v = b'.'.join(parts[:-1])
    return v


if __name__ == "__main__":
    print(get_git_version())
