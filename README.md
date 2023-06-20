# IndividualResearchProject
Song Organizer is a python script utilizing mutagen, google, requests, shutil, urllib3, bs4, and stat libraries in order to organize song files into a more desirable format. It utilizes the setlist.fm website in order to accomplish this task.

Created by Ryan Vauk
## Setup
Getting started:
- Download all .py files
- Run [Startup Song Organizer.bat]([https://github.com/RyanVauk/IndividualResearchProject/blob/main/startup_song_organizer.py](https://github.com/RyanVauk/Live-Song-Organizer/blob/main/Startup%20Song%20Organizer.bat)) to automatically download all necessary libraries and outside files (NOTE: you must have all of the files downloaded on this repository!)
- Change CODE-DIRECTORY in the .bat file to where you put the python files
## Usage
To actually run the program, you must run the Song Organizer.bat file. This file will run you through the song_organier.py file. The following is what will show when you run the .bat file assuming you changed the CODE-DIRECTORY in it.
```
Successfully created folder at C:\Users\ryanv\Desktop\_organizesongs!
If you need to download concerts, input URLs. If you don't or are done inputting, press enter.
If you don't need to download any concerts, just put the folders into the '_organizesongs' folder
```
After this, please input any links of concerts you would like to have downloaded and/or put any concert folders into the _organizesongs folder.
## Example
For example, take a Goose concert on 3/24/23. An abbreviated version of the metadata is listed below:
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
This is because the two songs are from the first set of the 3/24/23 concert which took place at the Metropolitan Opera House. The set information, venue, and if a song has a ">" is all taken from the setlist.fm site which, in this case, it would be [this webpage](https://www.setlist.fm/setlist/goose/2023/metropolitan-opera-house-philadelphia-pa-4bbbcbae.html).
## Notes
If a log.txt file appears in the concert folder, that means there is a missing song, a questionable song, or both from that concert. This means that there is either a missing song or a song that could have been changed wrong and requires further editing by you to fix. This information is also displayed in the console when the concert is done processing.

This program is ever-evolving and will always have bugs due to differences in how people type setlists on the website. For the most part, though, this code will work with most concerts that are downloaded in the format shown in the examples. However, if it doesn't this needs to be reported so that more edge cases can be created and the program is more functional.
