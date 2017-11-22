"""
Entry point for the_exif_mutalator
"""
import sys
import os.path
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from the_exif_mutalator.cli import parse_args  # pylint: disable=wrong-import-position


logger = logging.getLogger('the_exif_mutalator')  # pylint: disable=invalid-name


def print_exif(image_file):
    """ Prints exif data to stdout """
    pass


def save_exif(image_file):
    """ Saves exif data to same name as image_file with a .txt ending. """
    pass


def delete_exif(input_file, output_file, prefix=None, suffix=None):
    """ Removes exif data when saving file. """
    pass


def main(args):
    """ Main function. """
    logger.info("test")
    logger.warning("test warning")
    logger.error("test error")
    print(args)

    is_dir = os.path.isdir(args.input)
    if is_dir:
        logger.info("Working on all image files within the directory: {}".format(args.input))
    else:
        logger.info("Working on the image: {}".format(args.input))


if __name__ == '__main__':
    import logging_config  # pylint: disable=unused-import
    main(parse_args(sys.argv[1:]))
