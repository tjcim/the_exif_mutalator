[![Build Status](https://travis-ci.org/tjcim/the_exif_mutalator.svg?branch=master)](https://travis-ci.org/tjcim/the_exif_mutalator) [![Coverage Status](https://coveralls.io/repos/github/tjcim/the_exif_mutalator/badge.svg?branch=master&service=github)](https://coveralls.io/github/tjcim/the_exif_mutalator?branch=master&service=github)

# The EXIF Mutalator

This is a tool to view, save, and or delete EXIF data from images. The project started from the November Python Study Group Challenge.

## My Goals

While building this project I have the following goals:

* Fairly strict adherence to Test Driven Development
* Greater than 80% testing coverage
* Use a public testing server such as Travis or CircleCI
* Create a proper package that can be installed with pip (from the repo if not from pypi)
* Developing with security in mind
* Runs in Linux and Windows -- lower on the priority list


## INPUT

* You can specify a single image or a folder of images (`-i`,`--input`)


## EXIF OUTPUT

* You can print to stdout (`-p`,`--print-exif`)
* Save all exif data to a single file (`-s`,`--save-exif`)
* Save exif data to individual files with same name as destination image in the same output folder
(`-S`,`--save-exif-by-file`)
* Delete (`-d`,`--delete-exif`) - only makes sense when no output option is used.

You can print, save and delete exif data. The two save options are mutually exclusive.


## IMAGE OUTPUT

** Anytime an output option is used, the resulting image will no longer have exif data **

* You can save the image in-place (happens automatically when the `--delete-exif` option is used)
* You can save the image while setting a prefix `--prefix "no-exif-"` means the image will be saved
with the name "no-exif-Whatever the original name was.jpg"
* You can save the image while setting a suffix `--suffix "-no-exif"` means the image will be saved
with the name "Whatever the original name was-no-exif.jpg"
* You can save the image to another location `-o /path/to/output`
