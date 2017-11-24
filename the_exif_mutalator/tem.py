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
    logger.debug("Getting exif data for: {}".format(image_file))
    img = PIL.Image.open(image_file)
    if img._getexif():  # pylint: disable=protected-access
        exif = {
            PIL.ExifTags.TAGS[key]: value for key, value in \
            img._getexif().items() if key in PIL.ExifTags.TAGS  # pylint: disable=protected-access
        }
    else:
        exif = None
        logger.debug("No exif data for file.")
    return exif


def print_exif(image_file):
    """ Prints exif data to stdout """
    exif_data = get_exif(image_file)
    logger.debug("Printing exif data for: {}".format(image_file))
    print(exif_data)


def save_exif(image_file, exif_file_name=None):
    """ Saves exif data to same name as image_file with a .exif.txt ending. """
    logger.debug("Saving exif data for: {}".format(image_file))
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


def save_image(input_file, output):
    """ Save the image file removing exif_data. """
    if os.path.isdir(output):
        _, tail = os.path.split(input_file)
        output_file = os.path.join(output, tail)
    else:
        output_file = output
    img = PIL.Image.open(input_file)
    logger.debug("Saving image: {} to {}".format(input_file, output))
    img.save(output_file, 'JPEG')
    return output_file


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
    image_files = create_file_list(args)
    logger.debug("Created list of files: {}".format(image_files))
    for image_file in image_files:
        # Exif options
        if args.print_exif:
            print_exif(image_file)
        if args.save_exif_by_file:
            save_exif(image_file)
        elif args.save_exif:
            save_exif(image_file, args.save_exif)
        # Output options
        if args.output:
            new_filename = args.output
        else:
            new_filename = image_file
        if args.prefix:
            head, tail = os.path.split(new_filename)
            new_filename = os.path.join(head, args.prefix + tail)
        if args.suffix:
            head, tail = os.path.splitext(new_filename)
            new_filename = head + args.suffix + tail
        if args.output:
            save_image(image_file, new_filename)
        elif args.delete_exif or args.prefix or args.suffix:
            save_image(image_file, new_filename)
    logger.info("All done.")


if __name__ == '__main__':
    import logging_config  # pylint: disable=unused-import,unused-variable
    main(parse_args(sys.argv[1:]))
