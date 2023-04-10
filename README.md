# IndividualResearchProject
Song Organizer is a python script utilizing mutagen, googlesearch, shutil, urllib, bs4, and stat libraries in order to organize song files into a more desirable format. It utilizes the setlist.fm website in order to accomplish this task.

Created by Ryan Vauk
## Setup
Things to download:
- Most recent version of [python](https://www.python.org/downloads/)
- Mutagen library
- Urllib library
- Beautifulsoup4 (bs4) library
- Googlesearch library
- OS and Stat libraries
- Shutil library

To download any of these just use [pip](https://pip.pypa.io/en/stable/installation/)
```
pip install [libraryname]
```
To use the program, you must download the song_organizer.py file from this repository and then, using any IDE, change the starting_directory on line 231 to their desktop or any other folder of their choice.
```
231    starting_directory = "YOUR_DIRECTORY_HERE"
```
## Usage
To actually run the program, you must run the following commands in a OS console (where [DIRECTORY] is whatever directory the song_organizer.py is inside):
```
cd /D [DIRECTORY]
python song_organizer.py
```
The console should then output the following lines if the initial start was successful. If you get an error message, please try to ensure there is no other file named _organizesongs in the selected directory.
```
Successfully created folder at C:\Users\ryanv\Desktop\_organizesongs!
Please put the concert folders in it and press ENTER to continue
```
After this, please move each concert folder into _organizesongs and hit ENTER in the console. Then the program should run and end with a success message. If it errors, please create an error report so that any edge cases may be further fixed.
## Example
For example, take a Goose concert on 3/24/23. An abrievated version of the metadata is listed below:
```
       File Name                Song         Artist                 Album
------------------------------------------------------------------------------------
goo230324d1_01_Rockdale       Rockdale       Goose       2023/03/24 Philadelphia, PA
goo230324d1_02_Atlas_Dogs    Atlas Dogs      Goose       2023/03/24 Philadelphia, PA
        ...                     ...           ...                    ...
------------------------------------------------------------------------------------
```
The resulting files should be:
```
       File Name                Song         Artist                          Album
----------------------------------------------------------------------------------------------------------
goo230324d1_01_Rockdale       Rockdale       Goose       03/24/23 | 1st Set | Metropolitan Opera House, PA
goo230324d1_02_Atlas_Dogs   Atlas Dogs >     Goose       03/24/23 | 1st Set | Metropolitan Opera House, PA
        ...                     ...           ...                             ... 
----------------------------------------------------------------------------------------------------------
```
This is because the two songs are from the first set of the 3/24/23 concert which took place at the Metropolitan Opera House. The set information, venue and if a song has a ">" is all taken from the setlist.fm site which, in this case, it would be [this webpage](https://www.setlist.fm/setlist/goose/2023/metropolitan-opera-house-philadelphia-pa-4bbbcbae.html).
## Notes
If a log.txt files appears in the concert folder, that means there is a missing song, a duplicate song or both from that concert. This means that the folder is missing a song or has a accidental duplicated file (which the program will not process and just skip). This information is also displayed in the console when the concert is done processing.

This program is ever-evolving and will always have bugs due to differences in how people type setlists on the website. For the most part though, this code will work with most concerts that are downloaded in the format shown in examples. However, if it doesn't this needs to be reported so that more edge cases can be created and the program be more functional.
