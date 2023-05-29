from mutagen.mp4 import MP4
from urllib.request import urlopen
from bs4 import BeautifulSoup
from googlesearch import search
import os, stat
import shutil

def google_search(search_term):
    """Takes in a search term and uses the googlesearch library to search for it. It will then return the first url of the resulting search.

    ### Parameters
    1. search_term : str
        - The term to be searched for

    ### Returns
    - url : str
        - The first url of the search
    """
    for j in search(search_term, tld="co.in", num = 1):
        return j

def convert_to_american(date):
    """Takes in a date in format year/month/day and returns it as the American date format (month/day/year)

    ### Parameters
    1. date : str
        - Date in format (year/month/day)

    ### Returns
    - date : str
        - Date in American format (month/day/year)
    """
    year = date[2:4]
    month = date[5:7]
    day = date[8:10]
    return month + "/" + day + "/" + year

def change_album(dir, new_album):
    """Changes album of the given directory song file to new_album

    ### Parameters
    1. dir : str
        - Directory of the song file to change
    2. new_album : str
        - The new album to replace the old one
    """
    file=MP4(dir)
    file[r'©alb'] = new_album
    file.save()

def change_name(dir, new_name):
    """Changes thename of the given directory song file to new_name

    ### Parameters
    1. dir : str
        - Directory of the song file to change
    2. new_name : str
        - The new name to replace the old one
    """
    file=MP4(dir)
    file[r'©nam'] = new_name
    file.save()

def get_name(dir):
    """Gets the name of the given directory song file 

    ### Parameters
    1. dir : str
        - Directory of the song file to return the name of
        
    ### Returns
    - name : str
        - Metadata name of the given directory file
    """
    file=MP4(dir)
    return file[r'©nam'][0]

def get_album(dir):
    """Gets album of the given directory song file 

    ### Parameters
    1. dir : str
        - Directory of the song file to return the album of
        
    ### Returns
    - album : str
        - Metadata album of the given directory file
    """
    file=MP4(dir)
    return file[r'©alb'][0]

def get_artist(dir):
    """Gets artist of the given directory song file 

    ### Parameters
    1. dir : str
        - Directory of the song file to return the artist of
        
    ### Returns
    - artist : str
        - Metadata artist of the given directory file
    """
    file=MP4(dir)
    return file[r"©ART"][0]

def get_venue(text, album):
    """Gets venue of the given setlist text

    ### Parameters
    1. text : str
        - Text on setlist webpage
        
    ### Returns
    - venue : str
        - The venue in format venue, COUNTRY
    """
    venue = text[text.index("at")+3:]
    venue = venue[:venue.index(", ")] + album[-4:]
    return venue


def get_readable_text_from_webpage(url):
    """Returns the text from the given url webpage

    ### Parameters
    1. url : str
        - url to scrape text from
        
    ### Returns
    - text : str
        - Text from the url webpage
    """
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = text[text.index("You are here"):]
    return text

def transform_webpage_to_setlist(text):
    """Transforms basic webpage text to a readable setlist

    ### Parameters
    1. text : str
        - Webpage text
        
    ### Returns
    - list : return_array
        - Array of songs in the setlist
    - boolean : False
        - If any code errors
    """
    # try to find the setlist within the page, if fail, return False
    try:
        return_array = []
        encore = 0
        text = text[text.index("Set 1"):text.index("I was there")].replace("->", ">").replace("\n(>)", " >").replace("\n(>", " > \n")
        if("Note:" in text):
            text = text[:text.index("Note:")]
        for i in text.splitlines():
            inital_return_size = len(return_array)
            if("Set 1" in i):
                key = "1st Set"
                continue
            if("Set 2" in i):
                key = "2nd Set"
                continue
            if("Set 3" in i):
                key = "3rd Set"
                continue
            if(encore == 4):
                key = "4th Encore"
            if(encore == 3):
                key = "3rd Encore"
            if(encore == 2):
                key = "2nd Encore"
            if("Encore" in i):
                key = "1st Encore"
                encore += 1
                continue
            if(i[-2:] != "r)" and i[0] != "" and i != "Play Video" and "reprise" not in i and "tease)" not in i and i[0] != "("):
                return_array.append(i + ": λ" + key)
            try:
                return_array.append(i[i.rindex(r'> "')+3: i.index("reprise") + 7].replace(r'"', "").replace("reprise", "(Reprise)") + ":" + "λ" + key)
                return_array[-2] = return_array[-2][:return_array[-2].index(":")] + " >" + return_array[-2][return_array[-2].index(":"):]
                questionable_songs += return_array[-2] + ", "
            except:
                if("reprise)" in i):
                    return_array.append(i[1:].replace("‘", "").replace("’", "").replace('"', "").replace("reprise)", "(Reprise)" + ":" + "λ" + key))
            try:
                if(i[-2] == ">" or i[-1] == ">"):
                    return_array[-1] = return_array[-1][:return_array[-1].index(":")] + " >" + return_array[-1][return_array[-1].index(":"):]
            except:
                pass
            if(inital_return_size < len(return_array) and encore > 0):
                encore += 1
        if("1st Encore" in return_array[-1]):
            return_array[-1] = return_array[-1].replace("1st Encore", "Encore")
        return return_array
    except:
        return False
    
def progress_bar(current, total, bar_length=20):
    """Returns a progress bar

    ### Parameters
    1. current : int
        - Current percentange of the progress bar that is filled
    2. total : int
        - Max percetange of the progress bar that can be filled
    3. bar_length : int
        - How long the bar should be on the console
        
    ### Returns
    - str : progressbar
        - A progress bar with the given parameters taken into account
    """
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    ending = '\n' if current == total else '\r'

    return f'Progress: [{arrow}{padding}] {int(fraction*100)}%'

def album_to_searchterm(artist, album):
    """Changes thename of the given directory song file to new_name

    ### Parameters
    1. artist : str
        - Artist to search for
    2. album : str
        - Name of the album downloaded

    ### Returns
    - searchterm : str
        - Searchterm to find the setlist.fm webpage of the given artist, album, date and location
    """
    date = convert_to_american(album[:album.index(" ")])
    location = album[album.index(" ") + 1:]
    return "Setlistfm " + artist + " " + date + " " + location

def unknown_setlist():
    """Allows the user to define what setlist is to be used

    ### Returns
    - setlist : array
        - Properly formatted setlist with the input from the user
    - venue : str
        - The venue that the user stated
    """
    global text, venue, setlist
    user_input = input("Please input either a link or each line of the set (type help for more information) \n")
    if "www." in user_input:
        text = get_readable_text_from_webpage(url_setlist)
        venue = get_venue(text, album)
        setlist = transform_webpage_to_setlist(text)
        if(setlist == False):
            print("ERROR, SETLIST NOT FOUND AGAIN!")
            errored_input = input("Would you like to try again? It is recommended now to type out the setlist by hand (y/n).")
            if(errored_input == "y"):
                unknown_setlist()
            else:
                return
    if user_input == "help":
        print("You must enter the setlist in the format:\n1st Set: song, song, song, ...\n2nd Set: song, song, song, ...\nEncore: song, song, ...")
        unknown_setlist()
    else:
        user_setlist_full = user_input + "\n"
        
        while True:
            user_setlist_input = input()
            if user_setlist_input:
                user_setlist_full += user_setlist_input + "\n"
            else:
                break
        setlist = unknown_setlist_format(user_setlist_full)
        venue = input("What is the venue (venue, state abbreviation)? ")
            
def unknown_setlist_format(setlist):
    """Formats the user-inputted setlist to a useable format within the program

    ### Parameters
    1. setlist : str
        - What the user inputs as the setlist

    ### Returns
    - formatted_setlist : array
        - Array of the properly formatted setlist
    """
    formatted_setlist = []
    encore_count = 0
    encore_prefix = ''

    for line in setlist.split('\n'):
        if line:
            if line.startswith("1st Set:"):
                set_prefix = 'λ1st Set'
                line = line.replace("1st Set:", "").strip()
            elif line.startswith("2nd Set:"):
                set_prefix = 'λ2nd Set'
                line = line.replace("2nd Set:", "").strip()
            elif line.startswith("Encore:"):
                break
            else:
                set_prefix = encore_prefix if encore_prefix else ''

            songs = line.split(',')
            formatted_songs = [f"{song.strip()}: {set_prefix}" for song in songs]
            formatted_setlist.extend(formatted_songs)
    if("Encore: " in line):
        line = line.replace("Encore: ", "")
        for song in line.split(", "):
            encore_count += 1
            encore_prefix = f'λ{encore_count}{"st" if encore_count == 1 else "nd" if encore_count == 2 else "rd" if encore_count == 3 else "th"} Encore'
            formatted_setlist.append(song + ": " + encore_prefix)
    return formatted_setlist

# ----------------------------------------------------------------------------------------------------------

try:
    try:
        #Create a directory for the user to put all concert folders in to be processed
        starting_directory = "C:\\Users\\ryanv\\Desktop\\_organizesongs"
        os.mkdir(starting_directory)
        os.chdir(starting_directory)
        print("Successfully created folder at " + starting_directory + "!")
    except FileExistsError:
        print(r'"_organize songs" already exists at ' + starting_directory + "!")
    except:
        print("Unsuccessfully created folder")

    urls_to_be_downloaded = ""
    string_urls = ""
    urls_downloaded = False
    print("If you need to download concerts, input urls. If you don't type input or are done inputting, press enter.")
    while True:
        urls_to_be_downloaded = input()
        print("\033[A                                                                                         \033[A")
        if urls_to_be_downloaded:
            urls_downloaded = True
            string_urls += urls_to_be_downloaded + " "
        else:
            break
    if urls_downloaded:
        os.chdir("R:\\Coding\\My Coding\\Python\\Song Organizer\\Nugs-Downloader")
        print("-----------------------------------------------------\nDownloading inputted concerts (this could take a while)...")
        os.system("nugs_dl_x64.exe " + string_urls + " >nul 2>&1")
        print("Downloaded all inputted concerts!\n-----------------------------------------------------")
        os.chdir("R:\\Coding\\My Coding\\Python\\Song Organizer\\Nugs-Downloader\\Nugsdownloads")
        downloaded_concerts = os.listdir()
        for i in downloaded_concerts: 
            shutil.move("R:\\Coding\\My Coding\\Python\\Song Organizer\\Nugs-Downloader\\Nugsdownloads" + "\\" + i, starting_directory)
    else:
        print("You must move any concert folders into _organizesongs!")

    os.chdir(starting_directory)

    #Count number of concert folders in _organizesongs
    total_folders = len(os.listdir())

    folder_iterations = 1
    to_be_moved_concert_folders = []

    #For concert folder in _organizesongs
    for concert_folder in os.listdir():
        print("\nChanging " + concert_folder + " (" + str(folder_iterations) + "/" + str(total_folders) + ")")
        print(progress_bar(0, 100) + "                                                       ", end='\r', flush=True)
        os.chdir(starting_directory + "\\" + concert_folder)
        print(os.getcwd())
        #Get the album for the current concert folder
        album = get_album(starting_directory + "\\" + concert_folder + "\\" +os.listdir()[0])

        #Get the date for the current concert folder
        date = convert_to_american(album[:album.index(" ")])

        #Get the artist for the current concert folder
        artist = get_artist(starting_directory + "\\" + concert_folder + "\\" +os.listdir()[0])
        print(progress_bar(5, 100) + "                                                       ", end='\r', flush=True)

        #Create a searchterm with the album to be googled
        searchterm = album_to_searchterm(artist, album)
        print(progress_bar(6, 100) + "                                                       ", end='\r', flush=True)

        #Find the url of the setlist on setlist.fm
        url_setlist = google_search(searchterm)

        #Remove a mysterious file
        os.remove(starting_directory + "\\" + concert_folder + "\\.google-cookie")

        #Get readable text from the downloaded setlist information
        text = get_readable_text_from_webpage(url_setlist)

        #Get venue for later use
        venue = get_venue(text, album)

        #Transfom the readable text to a functioning setlist
        setlist = transform_webpage_to_setlist(text)
        if(setlist == False):
            print("ERROR, SETLIST NOT FOUND!")
            errored_input = input("Would you like to input the setlist yourself (y/n)? ")
            if(errored_input == "y"):
                unknown_setlist()
            else:
                to_be_moved_concert_folders.append(concert_folder)
                continue
        count = 0
        song_list = os.listdir()
        missing_songs = ""
        questionable_songs = ""
        print(progress_bar(25, 100) + "                                                       ", end='\r', flush=True)

        #For song string in the downloaded setlist
        for song in setlist:
            print(progress_bar(((((count+1)/len(song_list))*70) + 25), 100) + "                                                       ", end='\r', flush=True)
            #If the song is obviously a duplicate, skip it and add it to the duplicates list to be shown at the end of processing
            # try:
            #     if("1).m4a" in song_list[count] or " - Copy.m4a" in song_list[count]):
            #         duplicate_songs += song_list[count] + ", "
            #         count += 1
            # except:
            #     break
            if(get_name(song_list[count])[0:5].upper() == "INTRO" or get_name(song_list[count])[0:6].upper == "TUNING"):
                new_album = date + " | " + setlist[setlist.index(song) + 1][setlist[setlist.index(song) + 1].index("λ") + 1:] + " | " + venue
                change_album(starting_directory + "\\" + concert_folder + "\\" + os.listdir()[count], new_album)
                count += 1
            iterations = 0
            while True:
                continious = False
                if song[0:2] == " ‘" and "’ " in song:
                    song = song.replace(" ‘", "").replace("’", "")
                elif song[0:2] == " '" and "' " in song:
                    song = song.replace(" '", "").replace("'", "")
                #Check if the directory song name is in the downloaded setlist
                if((get_name(song_list[count]).upper() in song.upper()) or (song[:song.rindex(":")].replace(" (Reprise)", "").upper() in get_name(song_list[count]).upper())):
                    if(">" in song):
                        change_name(starting_directory + "\\" + concert_folder + "\\" + os.listdir()[count], song[:song.index(" >")+2])
                    else:
                        change_name(starting_directory + "\\" + concert_folder + "\\" + os.listdir()[count], song[:song.index(":")])
                    new_album = date + " | " + song[song.index("λ") + 1:] + " | " + venue
                    change_album(starting_directory + "\\" + concert_folder + "\\" + os.listdir()[count], new_album)
                    count += 1
                    break

                else:
                    #Check each word in the directory song name, if they are all there, then there is a match between the directory song and the setlist song!
                    possible_fix = True
                    wordsCorrect = 0
                    for i in get_name(song_list[count]).replace(".", " ").split(" "):
                        #Counter for how many words are correct between the two song names
                        if(i.upper() in song.upper()):
                            wordsCorrect += 1
                        #Try it with eliminating all parenthesis
                        elif(i.upper().replace("(", "").replace(")", "") in song.upper().replace("(", "").replace(")", "")):
                            wordsCorrect += 1
                        #Try it with eliminating all spaces
                        elif(i.upper().replace(" ", "").replace(" ", "") in song.upper().replace(" ", "").replace(" ", "")):
                            wordsCorrect += 1
                    #If over half the words are incorrect, this song is not the same
                    if(not wordsCorrect / len(get_name(song_list[count]).replace(".", " ").split(" ")) >= 0.5):
                        possible_fix = False
                    #If the above for loop gives a true value, fix the album and name of the directory song
                    if(possible_fix):
                        if(">" in song):
                            change_name(starting_directory + "\\" + concert_folder + "\\" + os.listdir()[count], song[:song.index(" >")+2])
                        else:
                            change_name(starting_directory + "\\" + concert_folder + "\\" + os.listdir()[count], song[:song.index(":")])
                        new_album = date + " | " + song[song.index("λ") + 1:] + " | " + venue
                        change_album(starting_directory + "\\" + concert_folder + "\\" + os.listdir()[count], new_album)
                        count += 1
                        break
                    
                    #If none of the above works, try skipping a song in the directory (to skip past any duplicates that could mess with the matching)
                    try:
                        if((get_name(song_list[count+1]).upper() in song.upper()) or (song[:song.rindex(":")].replace(" (Reprise)", "").upper() in get_name(song_list[count+1]).upper())):
                            change_album(starting_directory + "\\" + concert_folder + "\\" + os.listdir()[count], new_album)
                            count += 1
                        elif(iterations == 1):
                            #This may or may not fix the problem so it is questionable
                            questionable_songs += song + " & " + setlist[setlist.index(song) - 1] + ", "
                            if(">" in song):
                                change_name(starting_directory + "\\" + concert_folder + "\\" + os.listdir()[count-1], get_name(os.listdir()[count-1])+ " " + song[:song.index(" >")+2])
                            else:
                                change_name(starting_directory + "\\" + concert_folder + "\\" + os.listdir()[count-1], get_name(os.listdir()[count-1]) + " " + song[:song.index(":")])
                    except:
                        pass
                #Prevent infinite loops
                iterations += 1
                if(iterations >= 5):
                    break


        #If there is any missing songs or questionable songs, make a log file containing that information
        if(len(missing_songs) + len(questionable_songs) > 0):
            print(progress_bar(((((count+1)/len(song_list))*70) + 25), 100) + "                                                       ", end='\r', flush=True)
            with open('log.txt', 'w', encoding="utf-8") as f:
                f.write("missing songs: " + missing_songs + "\n" + "questionable songs: " + questionable_songs)
        os.chdir(starting_directory)
        print(progress_bar(98, 100) + "                                                       ", end='\r', flush=True)
        
        #Move completed concert file out of _organizesongs
        to_be_moved_concert_folders.append(concert_folder)
        folder_iterations += 1
        print(progress_bar(100, 100) + "                                                       ")
        
        #If there is any missing songs or questionable songs, print them to the console
        if(len(missing_songs) + len(questionable_songs) > 0):
            print("missing songs: " + missing_songs + "\n" + "questionable songs: " + questionable_songs + "\n")

    for i in to_be_moved_concert_folders:
        shutil.move(starting_directory + "\\" + i, starting_directory[:starting_directory.rindex("\\")])

    os.chdir(starting_directory[:starting_directory.index("\\")+1])
    os.chmod(starting_directory, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

    #Remove _organizesongs folder
    shutil.rmtree(starting_directory, ignore_errors=False)
    print("Successfully deleted " + starting_directory + "!")
    print("-----------------------------------------------------\nProgram Complete!")
    print("Press any key to exit...")
    input()

    #https://stackoverflow.com/questions/8948/accessing-mp3-metadata-with-python
    #https://www.geeksforgeeks.org/performing-google-search-using-python-code/
    #https://stackoverflow.com/questions/57521843/python-can-not-delete-folder-on-windows
except Exception as e:
    print(f"An error occurred: {str(e)}")
    input("Press Enter to exit...")
