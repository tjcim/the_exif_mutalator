""" Pytest for November Challenge """
import os
import logging

import pytest

from context import cli


IMAGES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_images")


def test_image_valid():
    """ Test the parse_args method. """
    res = cli.parse_args(["-i", os.path.join(IMAGES, "jpg/Canon_40D.jpg")])
    assert res.input == os.path.join(IMAGES, "jpg/Canon_40D.jpg")


def test_image_no_file():
    """ Test the parse_args method. """
    with pytest.raises(SystemExit):
        cli.parse_args(["-i"])


def test_input_is_folder():
    """ Input can be a folder. """
    res = cli.parse_args([
        "-i", os.path.join(IMAGES, "jpg")
    ])
    assert res.input == os.path.join(IMAGES, "jpg")


def test_image_missing_file():
    """ parse_args with -i but a file that doesn't exist. """
    with pytest.raises(SystemExit):
        cli.parse_args(["-i", "/this/file/doesn't/exit"])


def test_output_valid():
    """ Test the output option."""
    res = cli.parse_args(
        ["-i", os.path.join(IMAGES, "jpg/Canon_40D.jpg"),
         "-o", os.path.join(IMAGES, "jpg/new_file.jpg")]
    )
    assert res.output == os.path.join(IMAGES, "jpg/new_file.jpg")


def test_output_parent_dir_nonexistant():
    """ Test that the system accepts an output path that doesn't exit. """
    res = cli.parse_args(
        ["-i", os.path.join(IMAGES, "jpg/Canon_40D.jpg"),
         "-o", os.path.join(IMAGES, "does/not/exist/new_file.jpg")]
    )
    assert res.output == os.path.join(IMAGES, "does/not/exist/new_file.jpg")


def test_input_folder_valid():
    """ Test that providing an input folder works. """
    res = cli.parse_args(["-i", os.path.join(IMAGES, "jpg")])
    assert res.input == os.path.join(IMAGES, "jpg")


def test_input_folder_nonexistant():
    """ Test that providing an input folder that doesn't exist exits. """
    with pytest.raises(SystemExit):
        cli.parse_args(["-I", os.path.join(IMAGES, "does/not/exist/")])


def test_providing_image_and_image_folder_errors():
    """ App should error if image and image_folder are both provided. """
    with pytest.raises(SystemExit):
        cli.parse_args(["-i", os.path.join(IMAGES, "jpg/Canon_40D.jpg"),
                        "-I", os.path.join(IMAGES, "jpg")])


def test_an_input_was_provided():
    """ App should error if no input option was provided. """
    with pytest.raises(SystemExit):
        cli.parse_args(["-o", os.path.join(IMAGES, "jpg")])


def test_exif_print_to_stdout_option():
    """ App should print exif to stdout if this option is provided. """
    res = cli.parse_args(["-p", "-i", os.path.join(IMAGES, "jpg/Canon_40D.jpg")])
    assert res.print_exif is True


def test_save_exif_data_to_file():
    """ App should save exif data if the option is specified. """
    res = cli.parse_args([
        "-s", os.path.join(IMAGES, "exif_data.txt"),
        "-i", os.path.join(IMAGES, "jpg/Canon_40D.jpg"),
    ])
    assert res.save_exif == os.path.join(IMAGES, "exif_data.txt")


def test_save_exif_file_already_exists():
    """ App should warn and exit if saving exif data to a file that already exists. """
    with pytest.raises(SystemExit):
        cli.parse_args([
            "-s", os.path.join(IMAGES, "jpg/Canon_40D.jpg"),
            "-i", os.path.join(IMAGES, "jpg/Canon_40D.jpg"),
        ])


def test_delete_exif_data():
    """ App should allow deleting exif data for image. """
    res = cli.parse_args([
        "-i", os.path.join(IMAGES, "jpg/Canon_40D.jpg"),
        "-d"
    ])
    assert res.delete_exif is True


def test_save_exif_individual_files():
    """ App should save exif data to individual files if this option is presented. """
    res = cli.parse_args([
        "-i", os.path.join(IMAGES, "jpg"),
        "-S",
    ])
    assert res.save_exif_by_file is True


def test_save_exif_and_save_exif_by_file_are_exclusive():
    """ You can only use -s or -S """
    with pytest.raises(SystemExit):
        cli.parse_args([
            "-s", os.path.join(IMAGES, "jpg/Canon_40D.jpg"),
            "-i", os.path.join(IMAGES, "jpg/Canon_40D.jpg"),
            "-S",
        ])


def test_prefix_option_valid():
    """ Test prefix option. """
    res = cli.parse_args([
        "-i", os.path.join(IMAGES, "jpg"),
        "--prefix", "no_exif",
    ])
    assert res.prefix == "no_exif"


def test_suffix_option_valid():
    """ Test prefix option. """
    res = cli.parse_args([
        "-i", os.path.join(IMAGES, "jpg"),
        "--suffix", "no_exif",
    ])
    assert res.suffix == "no_exif"


def test_prefix_and_suffix_options_valid():
    """ Test prefix and suffix option. """
    res = cli.parse_args([
        "-i", os.path.join(IMAGES, "jpg"),
        "--prefix", "no_exif",
        "--suffix", "no_exif",
    ])
    assert res.suffix == "no_exif"
    assert res.prefix == "no_exif"


@pytest.mark.parametrize("text,expected", [
    ("no/forward_slashes", "noforward_slashes"),
    ("no!@#$%^&*()+=|\\}{][_special_characters", "no_special_characters"),
    ("test\"\'_quotes", "test_quotes"),
    ("test?><,/~`_these_characters", "test_these_characters"),
    ("test\n'{-+\)(ç?_unicode", "testç_unicode"),  # pylint: disable=anomalous-backslash-in-string
])
def test_prefix_option_removes_invalid_data(text, expected):
    """ Only file name safe characters should be allowed. """
    res = cli.parse_args([
        "-i", os.path.join(IMAGES, "jpg"),
        "--prefix", text,
        "--suffix", text,
    ])
    assert res.prefix == expected
    assert res.suffix == expected


@pytest.mark.parametrize("text,expected", [
    ("blah" + "e" * 30, "blah" + "e" * 26)
])
def test_prefix_and_suffix_trimmed_to_30_chars(text, expected):
    """ Test prefix and suffix trim """
    res = cli.parse_args([
        "-i", os.path.join(IMAGES, "jpg"),
        "--prefix", text,
        "--suffix", text,
    ])
    assert res.prefix == expected
    assert res.suffix == expected


def test_verbose_option():
    """ Test verbose option."""
    log = logging.getLogger(__name__)
    assert log.isEnabledFor(logging.DEBUG) is False
    cli.parse_args([
        "-i", os.path.join(IMAGES, "jpg"),
        "-v",
    ])
    assert log.isEnabledFor(logging.DEBUG) is True

def test_quiet_option():
    """ Test quiet option. """
    log = logging.getLogger(__name__)
    assert log.isEnabledFor(logging.WARN) is True
    cli.parse_args([
        "-i", os.path.join(IMAGES, "jpg"),
        "-q",
    ])
    assert log.isEnabledFor(logging.WARN) is False
    assert log.isEnabledFor(logging.ERROR) is True
