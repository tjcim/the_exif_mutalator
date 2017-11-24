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


def test_save_exif(canon_40d_file, canon_40d_exif):
    """ Test saving exif data to txt file. """
    filename = tem.save_exif(canon_40d_file)
    image_filename = os.path.split(canon_40d_file)[1]
    expected = ""
    expected += "\n{0}\n{1}\n{0}\n".format("*" * 25, image_filename)
    for key, value in canon_40d_exif.items():
        expected += "{}: {}\n".format(key, value)
    with open(filename, 'r') as filehandler:
        res = filehandler.read()
    assert res == expected


def test_save_exif_multiple_files(canon_40d_file, canon_40d_exif, long_description_file, tmpdir):
    """ Test saving multiple exif data to txt file. """
    exif_file = os.path.join(tmpdir, "exif_data.txt")
    ld_exif = tem.get_exif(long_description_file)
    tem.save_exif(canon_40d_file, exif_file)
    tem.save_exif(long_description_file, exif_file)
    expected = ""

    image_filename = os.path.split(canon_40d_file)[1]
    expected += "\n{0}\n{1}\n{0}\n".format("*" * 25, image_filename)
    for key, value in canon_40d_exif.items():
        expected += "{}: {}\n".format(key, value)

    image_filename = os.path.split(long_description_file)[1]
    expected += "\n{0}\n{1}\n{0}\n".format("*" * 25, image_filename)
    for key, value in ld_exif.items():
        expected += "{}: {}\n".format(key, value)

    with open(exif_file, 'r') as filehandler:
        res = filehandler.read()
    assert res == expected


def test_save_image(canon_40d_file, tmpdir):
    """ Test saving a file no exif data """
    output_file = os.path.join(tmpdir, "new_file.jpg")
    image_file = tem.save_image(canon_40d_file, output_file)
    res = tem.get_exif(image_file)
    assert res is None


def test_main_print_only(capfd, canon_40d_file, canon_40d_exif):
    """ Does a print of the exif data only. """
    args = cli.parse_args([
        "-i", canon_40d_file,
        "-p"
    ])
    tem.main(args)
    out, _ = capfd.readouterr()
    assert str(canon_40d_exif['ApertureValue']) in out
    assert str(canon_40d_exif['DateTime']) in out


def test_main_print_and_save_individually(capfd, canon_40d_file, canon_40d_exif):
    """ Does a print and saves exif data. """
    args = cli.parse_args([
        "-i", canon_40d_file,
        "-p",
        "-S",
    ])
    tem.main(args)
    out, _ = capfd.readouterr()
    assert str(canon_40d_exif['ApertureValue']) in out
    assert str(canon_40d_exif['DateTime']) in out
    exif_filename = canon_40d_file + ".exif.txt"
    assert os.path.isfile(exif_filename)


def test_main_save_exif_one_file(canon_40d_file, tmpdir):
    """ Saves all exif data to one file. """
    exif_filename = os.path.join(tmpdir, "exif_data.txt")
    args = cli.parse_args([
        "-i", canon_40d_file,
        "-s", exif_filename,
    ])
    tem.main(args)

    assert os.path.isfile(exif_filename)

    expected = os.path.split(canon_40d_file)[1]
    with open(exif_filename, 'r') as filehandler:
        contents = filehandler.read().splitlines()
    assert contents[2] == expected


def test_main_delete_exif_in_place(canon_40d_file):
    """ Save the image in-place without exif data. """
    args = cli.parse_args([
        "-i", canon_40d_file,
        "-d",
    ])
    tem.main(args)

    assert os.path.isfile(canon_40d_file)
    exif_data = tem.get_exif(canon_40d_file)
    assert exif_data is None


def test_main_delete_exif_new_file(canon_40d_file):
    """ Save the image to output without exif data. """
    output_file = canon_40d_file
    args = cli.parse_args([
        "-i", canon_40d_file,
        "-d",
        "-o", output_file,
    ])
    tem.main(args)

    assert os.path.isfile(output_file)
    exif_data = tem.get_exif(output_file)
    assert exif_data is None


def test_main_delete_exif_prefix(canon_40d_file):
    """ Delete exif, new file created with prefix."""
    prefix = "no_exif"
    args = cli.parse_args([
        "-i", canon_40d_file,
        "--prefix", prefix
    ])
    tem.main(args)

    head, tail = os.path.split(canon_40d_file)

    new_filename = os.path.join(head, prefix + tail)
    assert os.path.isfile(new_filename)
    exif_data = tem.get_exif(new_filename)
    assert exif_data is None


def test_main_delete_exif_suffix(canon_40d_file):
    """ Delete exif, new file created with suffix."""
    suffix = "_no_exif"
    args = cli.parse_args([
        "-i", canon_40d_file,
        "--suffix", suffix
    ])
    tem.main(args)

    head, tail = os.path.splitext(canon_40d_file)

    new_filename = head + suffix + tail
    assert os.path.isfile(new_filename)
    exif_data = tem.get_exif(new_filename)
    assert exif_data is None


def test_main_prefix_output(canon_40d_file, tmpdir):
    """ Save image to output with prefix. """
    prefix = "no_exif_"
    _, tail = os.path.split(canon_40d_file)
    output_file = os.path.join(tmpdir, tail)
    args = cli.parse_args([
        "-i", canon_40d_file,
        "--prefix", prefix,
        "-o", output_file,
    ])
    tem.main(args)
    head, tail = os.path.split(output_file)
    with_suffix = os.path.join(head, "no_exif_" + tail)
    assert os.path.isfile(with_suffix)
    assert tem.get_exif(with_suffix) is None


def test_main_suffix_output(canon_40d_file, tmpdir):
    """ Save image to output with suffix. """
    suffix = "_no_exif"
    _, tail = os.path.split(canon_40d_file)
    output_file = os.path.join(tmpdir, tail)
    args = cli.parse_args([
        "-i", canon_40d_file,
        "--suffix", suffix,
        "-o", output_file,
    ])
    tem.main(args)
    head, tail = os.path.splitext(output_file)
    with_suffix = head + "_no_exif" + tail
    assert os.path.isfile(with_suffix)
    assert tem.get_exif(with_suffix) is None


def test_print_exif_directory(capfd, image_folder, canon_40d_exif):
    """ print exif for a directory of images. """
    args = cli.parse_args([
        "-i", image_folder,
        "-p"
    ])
    tem.main(args)
    out, _ = capfd.readouterr()
    assert str(canon_40d_exif['ApertureValue']) in out
    assert str(canon_40d_exif['DateTime']) in out


def test_print_and_save_individually_directory(tmpdir, capfd, image_folder, canon_40d_exif):
    """ Does a print and saves exif data. """
    args = cli.parse_args([
        "-i", image_folder,
        "-p",
        "-S",
    ])
    tem.main(args)
    out, _ = capfd.readouterr()
    assert str(canon_40d_exif['ApertureValue']) in out
    assert str(canon_40d_exif['DateTime']) in out
    assert os.path.isfile(os.path.join(tmpdir, "jpg/Canon_40D.jpg.exif.txt"))


def test_main_save_exif_one_file_directory(image_folder, tmpdir):
    """ Saves all exif data to one file. """
    exif_filename = os.path.join(tmpdir, "exif_data.txt")
    args = cli.parse_args([
        "-i", image_folder,
        "-s", exif_filename,
    ])
    tem.main(args)

    assert os.path.isfile(exif_filename)

    expected = "Canon_40D.jpg"
    with open(exif_filename, 'r') as filehandler:
        contents = filehandler.read()
    assert expected in contents


def test_prefix_directory(image_folder):
    """ Save images with prefix. """
    prefix = "no_exif_"
    args = cli.parse_args([
        "-i", image_folder,
        "--prefix", prefix
    ])
    tem.main(args)
    output_filename = os.path.join(image_folder, "no_exif_Canon_40D.jpg")
    assert os.path.isfile(output_filename)
    assert tem.get_exif(output_filename) is None

def test_suffix_directory(image_folder):
    """ Save images with suffix. """
    suffix = "_no_exif"
    args = cli.parse_args([
        "-i", image_folder,
        "--suffix", suffix
    ])
    tem.main(args)
    output_filename = os.path.join(image_folder, "Canon_40D_no_exif.jpg")
    assert os.path.isfile(output_filename)
    assert tem.get_exif(output_filename) is None


def test_suffix_and_prefix_file(canon_40d_file):
    """ Test both suffix and prefix. """
    suffix = "_no_exif"
    prefix = "no_exif_"
    args = cli.parse_args([
        "-i", canon_40d_file,
        "--suffix", suffix,
        "--prefix", prefix,
    ])
    tem.main(args)
    head, tail = os.path.split(canon_40d_file)
    new_file = os.path.join(head, prefix + tail)
    head, tail = os.path.splitext(new_file)
    output_filename = head + suffix + tail
    assert os.path.isfile(output_filename)
    assert tem.get_exif(output_filename) is None


def test_prefix_and_suffix_directory(image_folder, tmpdir):
    """ Test both suffix and prefix on a directory """
    suffix = "_no_exif"
    prefix = "no_exif_"
    output_dir = os.path.abspath(tmpdir)
    args = cli.parse_args([
        "-i", image_folder,
        "-o", output_dir,
        "--suffix", suffix,
        "--prefix", prefix,
    ])
    tem.main(args)
    output_filename = os.path.join(tmpdir, "no_exif_Canon_40D_no_exif.jpg")
    assert os.path.isfile(output_filename)
    assert tem.get_exif(output_filename) is None
