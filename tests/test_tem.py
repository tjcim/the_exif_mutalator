"""
Test the tem module.
"""
import os

from context import tem


IMAGES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_images")


def test_get_exif(canon_40d_exif):
    """ test get_exif functionality """
    exif_data = tem.get_exif(os.path.join(IMAGES, "jpg/Canon_40D.jpg"))
    assert exif_data == canon_40d_exif


def test_print_exif(capfd, canon_40d_exif):
    """ test print exif data to screen. """
    tem.print_exif(os.path.join(IMAGES, "jpg/Canon_40D.jpg"))
    out, _ = capfd.readouterr()
    assert str(canon_40d_exif['ApertureValue']) in out
    assert str(canon_40d_exif['DateTime']) in out
