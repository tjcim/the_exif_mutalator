""" Defining command line options for the app. """
import os
import logging
import argparse


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def clean_filename(name):
    """ Remove illegal characters from filenames. """
    valid_special_characters = (' ', '.', '_')
    new_name = "".join(l for l in name if l.isalnum() or l in valid_special_characters).rstrip()
    if not name == new_name:
        logger.debug("Modified name due to the existence of special characters.")
        logger.debug("Original name: {}".format(name))
        logger.debug("New name: {}".format(new_name))
    if len(new_name) > 30:
        logger.debug("Trimming name due to length. Length was: {}".format(len(new_name)))
        new_name = new_name[:30]
    return new_name


def add_exif_options(parser):
    """ Add argument options for handling exif data. """
    parser.add_argument('-p', '--print-exif', action='store_true',
                        help='Print EXIF data to stdout.')
    save_exif_group = parser.add_mutually_exclusive_group()
    save_exif_group.add_argument('-s', '--save-exif', help='Save EXIF data to specified file.')
    save_exif_group.add_argument('-S', '--save-exif-by-file', action='store_true',
                                 help='Save EXIF data of each file.')
    parser.add_argument('-d', '--delete-exif', action='store_true',
                        help='Delete EXIF data on image.')
    return parser


def add_output_options(parser):
    """ Add argument options for saving images. """
    parser.add_argument('-o', '--output', help='The path to save the image(s).')
    parser.add_argument('--prefix', help='Save image with the provided prefix.')
    parser.add_argument('--suffix', help='Save image with the provided suffix.')
    return parser


def add_verbosity_options(parser):
    """ Add ability to increase and decrease verbosity. """
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument('-v', '--verbose', action='store_true', help='Increase verbosity')
    verbosity_group.add_argument('-q', '--quiet', action='store_true', help='Decrease verbosity')
    return parser


def parse_args(args):
    """ Parse and validate command line arguments. """
    parser = argparse.ArgumentParser(
        prog='the_exif_mutalator',
        description='Absolutely destroys EXIF data.'
    )
    # Image input options
    parser.add_argument('-i', '--input', required=True,
                        help='The image file or directory of images with dirty EXIF data.')
    parser = add_output_options(parser)
    parser = add_exif_options(parser)
    parser = add_verbosity_options(parser)

    args = parser.parse_args(args)

    log = logging.getLogger()
    if args.verbose:
        log.setLevel(logging.DEBUG)
        logger.debug("Setting logging to debug.")
    elif args.quiet:
        log.setLevel(logging.ERROR)
    else:
        log.setLevel(logging.INFO)

    # if image option, check it exists.
    if args.input:
        if not os.path.isfile(args.input) and not os.path.isdir(args.input):
            logging.error("The file or directory doesn't exist: {}".format(args.input))
            raise SystemExit

    # if save exif data to file that exists it should exit.
    if args.save_exif:
        if os.path.isfile(args.save_exif):
            logging.error("The exif file already exists: {}".format(args.save_exif))
            raise SystemExit

    # Make sure prefix and suffix are safe
    if args.prefix:
        args.prefix = clean_filename(args.prefix)
    if args.suffix:
        args.suffix = clean_filename(args.suffix)

    return args
