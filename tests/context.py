""" Add directory to path, tests should import from this file. """
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from the_exif_mutalator import cli, logging_config, tem  # pylint: disable=wrong-import-position,unused-import
