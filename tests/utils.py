"""Utilities for testing."""
import os


def cleanup_files(files):
    """
    Takes a file or a list of files and removes them.
    """

    def _do_remove(fil):
        if os.path.exists(fil):
            os.remove(fil)

    flist = []
    if isinstance(files, list):
        flist = files[:]
    else:
        flist = [files]

    for fil in flist:
        _do_remove(fil)
