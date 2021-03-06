"""
Fixtures for pytest files
"""
import os
import shutil

import pytest


IMAGES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_images")


@pytest.fixture
def canon_40d_exif():
    """ exif data from image cannon_40d"""
    exif_data = {
        'GPSInfo': {0: b'\x02\x02\x00\x00'},
        'ResolutionUnit': 2,
        'ExifOffset': 214,
        'Make': 'Canon',
        'Model': 'Canon EOS 40D',
        'Software': 'GIMP 2.4.5',
        'Orientation': 1,
        'DateTime': '2008:07:31 10:38:11',
        'YCbCrPositioning': 2,
        'XResolution': (72, 1),
        'YResolution': (72, 1),
        'ExifVersion': b'0221',
        'ComponentsConfiguration': b'\x01\x02\x03\x00',
        'ShutterSpeedValue': (483328, 65536),
        'DateTimeOriginal': '2008:05:30 15:56:01',
        'DateTimeDigitized': '2008:05:30 15:56:01',
        'ApertureValue': (368640, 65536),
        'ExposureBiasValue': (0, 1),
        'MeteringMode': 5,
        'UserComment': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',  # pylint: disable=line-too-long
        'Flash': 9,
        'FocalLength': (135, 1),
        'ColorSpace': 1,
        'ExifImageWidth': 100,
        'ExifInteroperabilityOffset': 948,
        'FocalPlaneXResolution': (3888000, 876),
        'FocalPlaneYResolution': (2592000, 583),
        'SubsecTime': '00',
        'SubsecTimeOriginal': '00',
        'SubsecTimeDigitized': '00',
        'ExifImageHeight': 68,
        'FocalPlaneResolutionUnit': 2,
        'ExposureTime': (1, 160),
        'FNumber': (71, 10),
        'ExposureProgram': 1,
        'CustomRendered': 0,
        'ISOSpeedRatings': 100,
        'ExposureMode': 1,
        'FlashPixVersion': b'0100',
        'WhiteBalance': 0, 'SceneCaptureType': 0
    }
    return exif_data


@pytest.fixture
def canon_40d_file(tmpdir):
    """ Create a copy of the file for testing. """
    shutil.copyfile(os.path.join(IMAGES, "jpg/Canon_40D.jpg"),
                    os.path.join(tmpdir, "Canon_40D.jpg"))
    return os.path.join(tmpdir, "Canon_40D.jpg")


@pytest.fixture
def long_description_file(tmpdir):
    """ Create a copy of the file for testing. """
    shutil.copyfile(os.path.join(IMAGES, "jpg/long_description.jpg"),
                    os.path.join(tmpdir, "long_description.jpg"))
    return os.path.join(tmpdir, "long_description.jpg")


@pytest.fixture
def image_folder(tmpdir):
    """ Create a directory of images for testing. """
    shutil.copytree(os.path.join(IMAGES, "jpg"),
                    os.path.join(tmpdir, "jpg"))
    return os.path.join(tmpdir, "jpg")
