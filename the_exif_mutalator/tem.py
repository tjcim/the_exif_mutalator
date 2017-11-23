"""
Entry point for the_exif_mutalator
"""
import sys
import glob
import os.path
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import PIL.Image  # pylint: disable=wrong-import-position
import PIL.ExifTags  # pylint: disable=wrong-import-position

from the_exif_mutalator.cli import parse_args  # pylint: disable=wrong-import-position


logger = logging.getLogger('the_exif_mutalator')  # pylint: disable=invalid-name


def get_exif(image_file):
    """ Returns a dictionary of exif data. """
    img = PIL.Image.open(image_file)
    exif = {
        PIL.ExifTags.TAGS[key]: value for key, value in \
        img._getexif().items() if key in PIL.ExifTags.TAGS  # pylint: disable=protected-access
    }
    return exif


def print_exif(image_file):
    """ Prints exif data to stdout """
    exif_data = get_exif(image_file)
    print(exif_data)


def save_exif(image_file, exif_file_name=None):
    """ Saves exif data to same name as image_file with a .exif.txt ending. """
    parent_dir, image_filename = os.path.split(image_file)
    if exif_file_name:
        txt_path = exif_file_name
    else:
        txt_path = os.path.join(parent_dir, image_filename + ".exif.txt")
    exif_data = get_exif(image_file)
    with open(txt_path, 'a') as filehandler:
        filehandler.write("\n{0}\n{1}\n{0}\n".format("*" * 25, image_filename))
        for key, val in exif_data.items():
            filehandler.write("{}: {}\n".format(key, val))
    return txt_path


def save_image():
    """ Save the image file. """
    pass


def create_file_list(args):
    """ Return a list of files to process """
    is_dir = os.path.isdir(args.input)
    if is_dir:
        os.chdir(args.input)
        files = []
        for filename in glob.glob("*.jpg"):
            files.append(filename)
        return files
    return [args.input]


def main(args):
    """ Main function. """
    pass


if __name__ == '__main__':
    import logging_config  # pylint: disable=unused-import
    main(parse_args(sys.argv[1:]))
