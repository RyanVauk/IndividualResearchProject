from mutagen.mp4 import MP4
from urllib.request import urlopen
from bs4 import BeautifulSoup
from googlesearch import search
import os, stat
import shutil

def google_search(search_term):
    for j in search(search_term, tld="co.in", num = 1):
        return j

def convert_to_american(date):
    year = date[2:4]
    month = date[5:7]
    day = date[8:10]
    return month + "/" + day + "/" + year

def change_album(dir, new_album):
    file=MP4(dir)
    file[r'©alb'] = new_album
    file.save()

def change_name(dir, new_name):
    file=MP4(dir)
    file[r'©nam'] = new_name
    file.save()

def get_album(dir):
    file=MP4(dir)
    return file[r'©alb'][0]

def get_artist(dir):
    file=MP4(dir)
    return file[r"©ART"][0]

def get_readable_text_from_webpage(url):
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
    return text

def transform_webpage_to_setlist(text):
    return_array = []
    encore = 0
    text = text[text.index("Set 1"):text.index("I was there")].replace("\n(>)", " >").replace("\n(>", " > \n")
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
        except:
            if("reprise)" in i):
                return_array.append(i[1:].replace('"', "").replace("reprise)", "(Reprise)" + ":" + "λ" + key))
        try:
            if(i[-2] == ">" or i[-1] == ">"):
                return_array[-1] = return_array[-1][:return_array[-1].index(":")] + " >" + return_array[-1][return_array[-1].index(":"):]
            # elif(">" in i):
            #     return_array[-1] = return_array[-1][:return_array[-1].index(":")] + " >" + return_array[-1][return_array[-1].index(":"):]
        except:
            pass
        if(inital_return_size < len(return_array) and encore > 0):
            encore += 1
    if("1st Encore" in return_array[-1]):
        return_array[-1] = return_array[-1].replace("1st Encore", "Encore")
    return return_array

def progress_bar(current, total, bar_length=20):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    ending = '\n' if current == total else '\r'

    return f'Progress: [{arrow}{padding}] {int(fraction*100)}%'

def album_to_searchterm(artist, album):
    date = convert_to_american(album[:album.index(" ")])
    location = album[album.index(" ") + 1:]
    return "Setlistfm " + artist + " " + date + " " + location

# ----------------------------------------------------------------------------------------------------------
try:
    starting_directory = "C:\\Users\\ryanv\\Desktop\\_organizesongs"
    os.mkdir(starting_directory)
    os.chdir(starting_directory)
    print("Successfully created folder at " + starting_directory + "!\nPlease put the concert folders in it and press ENTER to continue")
    input()
except FileExistsError:
    print(r'"_organize songs" already exists at ' + starting_directory + "!")
except:
    print("Unsuccessfully created folder")

total_folders = len(os.listdir())
folder_iterations = 1
for concert_folder in os.listdir(): #folders
    #print("\nChanging " + concert_folder + " (" + str(folder_iterations) + "/" + str(total_folders) + ")")
    #print(progress_bar(0, 100) + "                                                       ", end='\r', flush=True)
    os.chdir(starting_directory + "\\" + concert_folder)
    album = get_album(starting_directory + "\\" + concert_folder + "\\" +os.listdir()[0])
    date = convert_to_american(album[:album.index(" ")])
    artist = get_artist(starting_directory + "\\" + concert_folder + "\\" +os.listdir()[0])

    print(progress_bar(5, 100) + "                                                       ", end='\r', flush=True)
    searchterm = album_to_searchterm(artist, album)

    print(progress_bar(6, 100) + "                                                       ", end='\r', flush=True)
    url_setlist = google_search(searchterm)
    os.remove(starting_directory + "\\" + concert_folder + "\\.google-cookie") # Mysterious file
    text = get_readable_text_from_webpage(url_setlist)
    venue = text[text.index("at")+3:text.index(", ")] + album[-4:]
    setlist = transform_webpage_to_setlist(text)
    count = 0
    song_list = os.listdir()
    missing_songs = ""
    duplicate_songs = ""
    print(progress_bar(25, 100) + "                                                       ", end='\r', flush=True)
    for song in setlist: #songs in setlist
        print(progress_bar(((((count+1)/len(song_list))*70) + 25), 100) + "                                                       ", end='\r', flush=True)
        if(").m4a" in song_list[count] or " - Copy.m4a" in song_list[count]):
            duplicate_songs += song_list[count] + ", "
            count += 1

        while True:
            #print(song_list[count][song_list[count].index("_") + 4:song_list[count].index(".m")].upper().replace("THE_", "").replace("_LAMA_", "LAMMA").replace("_", "") + ":" + song.replace("'", "").replace(".", "").replace("Pt 1", "Pt I").replace("Pt 2", "Pt II").replace("ñ", "").replace(" (", " ").replace(")", "").upper().replace("THE ", "").replace(" ", ""))
            if(song_list[count][song_list[count].index("_") + 4:song_list[count].index(".m")].upper().replace("THE_", "").replace("_LAMA_", "LAMMA").replace("_", "")  in song.replace("'", "").replace(".", "").replace("-", "").replace("Pt 1", "Pt I").replace("Pt 2", "Pt II").replace("ñ", "").replace(" (", " ").replace(")", "").upper().replace("THE ", "").replace(" ", "")):
                if(">" in song):
                    change_name(starting_directory + "\\" + concert_folder + "\\" + os.listdir()[count], song[:song.index(" >")+2])
                else:
                    change_name(starting_directory + "\\" + concert_folder + "\\" + os.listdir()[count], song[:song.index(":")])
                new_album = date + " | " + song[song.index("λ") + 1:] + " | " + venue
                change_album(starting_directory + "\\" + concert_folder + "\\" + os.listdir()[count], new_album)
                count += 1
                break

            else:
                try:
                    if(song_list[count+1][song_list[count+1].index("_") + 4:song_list[count+1].index(".m")].replace("_", " ").upper().replace("THE ", "").replace(" ", "") in song.replace("'", "").replace(".", "").replace("Pt 1", "Pt I").replace("Pt 2", "Pt II").replace("ñ", "").replace(" (", " ").replace(")", "").upper().replace("THE ", "").replace(" ", "")):
                        change_album(starting_directory + "\\" + concert_folder + "\\" + os.listdir()[count], new_album)
                        count += 1
                    else:
                        missing_songs += song + ", "
                except:
                    pass


    if(len(missing_songs) + len(duplicate_songs) > 0):
        print(progress_bar(((((count+1)/len(song_list))*70) + 25), 100) + "                                                       ", end='\r', flush=True)
        with open('log.txt', 'w', encoding="utf-8") as f:
            f.write("missing songs: " + missing_songs + "\n" + "duplicate songs: " + duplicate_songs)
    os.chdir(starting_directory)
    print(progress_bar(98, 100) + "                                                       ", end='\r', flush=True)
    shutil.move(starting_directory + "\\" + concert_folder, starting_directory[:starting_directory.rindex("\\")])
    folder_iterations += 1
    print(progress_bar(100, 100) + "                                                       ")
    if(len(missing_songs) + len(duplicate_songs) > 0):
        pass
        print("missing songs: " + missing_songs + "\n" + "duplicate songs: " + duplicate_songs + "\n")
os.chdir(starting_directory[:starting_directory.index("\\")+1])
os.chmod(starting_directory, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
shutil.rmtree(starting_directory, ignore_errors=False)
print("Successfully deleted " + starting_directory + "!")
print("------------------------------\nProgram Complete!")
print("Press any key to exit...")
input()

#https://stackoverflow.com/questions/8948/accessing-mp3-metadata-with-python
#https://www.geeksforgeeks.org/performing-google-search-using-python-code/
#https://stackoverflow.com/questions/57521843/python-can-not-delete-folder-on-windows
