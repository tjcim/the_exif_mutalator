"""
Test the tem module.
"""
import os

from context import tem, cli


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


def test_create_file_list_single_file(canon_40d_file):
    """ test the function to create a list of files to process. """
    args = cli.parse_args([
        "-i", canon_40d_file,
    ])
    res = tem.create_file_list(args)
    assert res == [canon_40d_file]


def test_create_file_list_directory(image_folder):
    """ test the function to create a list of files on a directory. """
    args = cli.parse_args([
        "-i", image_folder,
    ])
    res = tem.create_file_list(args)
    expected = [
        'Nikon_D70.jpg', 'PaintTool_sample.jpg', 'Ricoh_Caplio_RR330.jpg', 'Canon_40D.jpg',
        'WWL_(Polaroid)_ION230.jpg', 'Fujifilm_FinePix_E500.jpg',
        'Canon_40D_photoshop_import.jpg', 'Canon_DIGITAL_IXUS_400.jpg',
        'Fujifilm_FinePix6900ZOOM.jpg', 'Sony_HDR-HC3.jpg', 'Panasonic_DMC-FZ30.jpg',
        'Olympus_C8080WZ.jpg', 'Canon_PowerShot_S40.jpg', 'Nikon_COOLPIX_P1.jpg',
        'long_description.jpg', 'Samsung_Digimax_i50_MP3.jpg', 'Kodak_CX7530.jpg',
        'Konica_Minolta_DiMAGE_Z3.jpg', 'Pentax_K10D.jpg'
    ]
    assert set(res) == set(expected)
