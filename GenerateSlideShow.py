#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

"""

GenerateSlideShow.py generates a single html file that displays a slideshow with all images from a subfolder, "img" by default.
If called with no additional configuration, it uses the current directory to write "slideshow.html". 
For more help, run  GenerateSlideShow.py -h
        
"""

programDescription = "GenerateSlideShow.py generates a single html file that displays a slideshow with all images from a subfolder, \"img\" by default. If called with no additional configuration, it uses the current directory to write \"slideshow.html\". " 

__version__ = "0.2.8"
__author__ = "Pieter van der Wolk"

__copyright__ = "Copyright 2024, Pieter van der Wolk"

__status__ = "beta"  # "pre-alpha" / "alpha" / "beta" / "RC" / "RTM" / "GA" / "Gold"   # https://en.wikipedia.org/wiki/Software_release_life_cycle
#__Python-version-used__ = "3.8.6"

"""  
Bugs

1. use os.sep - done 0.2.8 - 21-05-2024 + tested
2. ...

"""

"""
Feature requests

1. Enable selection which images to process (.gif, .svg, ...)
2. set title                                                    - done 0.2.6 - 21-05-2024 + tested
3. set title in .ini
4. store all settings in a list


"""

"""
Dependencies

!pip install ...

"""

import os, sys, subprocess, logging
import pathlib
import argparse, configparser

rootFolderPath = pathlib.Path().absolute()  # path of the current prompt in command prompt
slideshowFolderPath = os.path.realpath(os.path.dirname(__file__))    # r'C:\\Users\\me\\Documents\\holiday\\pictures\\slideshow\\'
programPath = os.path.realpath(os.path.dirname(__file__))            # Path of GenerateSlideShow.py

# fallback configuration
imageFolderName = "img"
imageHeight = "1500"
headerTextFile = "header.txt"
footerTextFile = "footer.txt"
slideshowFileName = "slideshow.html"
fVerbose = True
HeaderToReplace = "<title>slides</title>"
NewHeader = HeaderToReplace

logging.basicConfig(filename=os.path.join(programPath, 'GenerateSlideShow.log'),  level=logging.DEBUG) # python version 3.9 can do "encoding='utf-8'," additionally here

# .ini configuration, overwrites fallback configuration
config = configparser.ConfigParser()
config.optionxform = str  # otherwise, all keys are converted to lowercase - bug 2
iniPathAndName = os.path.join(programPath, 'GenerateSlideShow.ini')
if fVerbose: print(f"Path to .ini is: {iniPathAndName}.")
config.read(iniPathAndName, 'UTF-8')
config.sections()
if fVerbose: print(f"Sections: {config.sections()}")

for key in config['path']:  
    logging.info(f"Adding setting : {config['path'][key]}")  # not tested yet


if config['path']['RootFolderPath'] != "": 
    rootFolderPath = config['path']['RootFolderPath']

if config['path']['ImageSubfolder'] != "": 
    rootFolderPath = config['path']['ImageSubfolder']

for key in config['input files']:  
    logging.info(f"Adding setting : {config['input files'][key]}")  # not tested yet

if config['input files']['HeaderTextFile'] != "": 
    headerTextFile = config['input files']['HeaderTextFile']

if config['input files']['FooterTextFile'] != "": 
    footerTextFile = config['input files']['FooterTextFile']

for key in config['images']:  
    logging.info(f"Adding setting : {config['images'][key]}")  # not tested yet
if config['images']['ImageHeight'] != "": imageHeight = config['images']['ImageHeight']
if fVerbose: print(f"Config file sets image height to: {imageHeight}.")

# command line parameter configuration, overwrites all other configurations

parser = argparse.ArgumentParser(description=programDescription, epilog="...have fun!")
# you get the -h argument for free
parser.add_argument("-p", "--path", help="Path to the folder where the image folder is located. Defaults to the current folder", type=str)
parser.add_argument("-f", "--folder", help="Folder name of the folder with images, defaults to\"img\"", type=str)
parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true") # if you specify --verbose/-v,  args.verbose becomes True, the default is False. 
parser.add_argument("-ih", "--imageHeight", help="Default image height, default = 1500 px", type=int)
parser.add_argument("-hf", "--headerfile", help="File with the html headings for the slideshow in the current folder; default: header.txt.", type=str)
parser.add_argument("-ff", "--footerfile", help="File with the html closing lines for the slideshow in the current folder; default: footer.txt.", type=str)
parser.add_argument("-ssf", "--slideshowfile", help="Filename for the slideshow html file; default: slideshow.html.", type=str)
parser.add_argument("-bt", "--BrowserTabText", help="Text displayed in the browser tab; default: slides.", type=str)


args = parser.parse_args()
logging.info(f"Path for slideshow.html : {args.path}")  
logging.info(f"Name of the folder with images : {args.folder}")
logging.info(f"Name of the  html headings file : {args.headerfile}")
logging.info(f"Name of the html footer file : {args.footerfile}")
logging.info(f"Name of the slideshow output html-file : {args.slideshowfile}")
if args.imageHeight:
    imageimageheight = str(args.imageHeight)
logging.info(f"Command line sets image height of the images : {args.imageHeight}")

if args.verbose:
    fVerbose = True
    print("Commandline sets verbosity turned on")

if args.folder: 
    imageFolderName = args.folder
if fVerbose:  print(f"Command line sets name of the folder with images : {args.folder}")

if args.headerfile: 
    headerTextFile = args.headerfile
if fVerbose:  print(f"Command line sets name of the  html headings file : {args.headerfile}")  # default: header.txt

if args.footerfile: 
    footerTextFile = args.footerfile
if fVerbose:  print(f"Command line sets name of the folder with images : {args.footerfile}") # default: footer.txt

if args.slideshowfile: 
    slideshowFileName = args.slideshowfile
if fVerbose:  print(f"Command line sets name of the slideshow output html-file : {args.slideshowfile}") # default: slideshow.html

if args.BrowserTabText: 
    NewHeader = "<title>" + args.BrowserTabText + "</title>" 
if fVerbose:  
    print(f"Command line sets name of the browser tab: {args.BrowserTabText}") # default: slides
    print(f"The new header line is: {NewHeader}.")



if __name__ == "__main__":

    """ 
    
    GenerateSlideShow.py generates a single html file that displays a slideshow with all images in a subfolder, "img" by default.
    If called on its own, it sets the root of the file tree to be traversed as the current directory. 

    """

    imageFolderPath = os.path.join(slideshowFolderPath, imageFolderName)
    if fVerbose: print(f"The path to the image folder = {imageFolderPath}")

    SlideshowFile = open(os.path.join(slideshowFolderPath,slideshowFileName), "w") 

    # read the headers, copy it to the slideshow file

    with open(os.path.join(programPath,headerTextFile),'r') as headersfile:
        # read content from headersfile 
        for line in headersfile:            
                # write content to slideshow file 
                line = line.replace(HeaderToReplace, NewHeader)
                SlideshowFile.write(line)  # replace is to change the title on the browser tab
                if fVerbose: print(line)
    headersfile.close

    # write the list of image files

    for root, dirs, files in os.walk(imageFolderPath):
        files = [ file for file in files if file.endswith( ('.jpg','.JPG','.png','.PNG', '.jpeg', '.JPEG', '.jfif', '.JFIF', '.svg', '.SVG', '.gif', '.GIF') ) ]
        for filename in files:
            lineWithImage = f"<img class=\"images\" src=\"./{imageFolderName}/"+os.path.join(filename)+f"\" imageHeight={imageHeight}>\n"
            SlideshowFile.write(lineWithImage)
            if fVerbose: print(lineWithImage)

    with open(os.path.join(programPath,footerTextFile),'r') as footerfile:
        # read content from footerfile 
        for line in footerfile:            
                # write content to slideshow file 
                SlideshowFile.write(line)
    footerfile.close

    SlideshowFile.close() 
