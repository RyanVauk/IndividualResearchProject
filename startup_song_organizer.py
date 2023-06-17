import subprocess
from console_colors import ConsoleColors
import os
import json
import zipfile
import shutil

def get_current_file_directory():
    file_path = os.path.abspath(__file__)
    directory = os.path.dirname(file_path)
    return directory + "\\"

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

    return ConsoleColors.BG_BLUE + f'Progress: [{arrow}{padding}] {int(fraction*100)}%' + ConsoleColors.RESET

def install_package(package_names):
    print(ConsoleColors.MAGENTA + "Downloading required libraries..." + ConsoleColors.RESET)
    for i in range(len(package_names)):
        print(ConsoleColors.MAGENTA + f"Downloading {package_names[i]: <30} {progress_bar(((i+1)/len(package_names)) * 100, 100)}" + ConsoleColors.RESET, end='\r', flush=True)
        try:
            subprocess.check_call(['pip', 'install', package_names[i]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            print(ConsoleColors.RED + "ERROR: SOMETHING WENT WRONG AND ONE OF THE PACKAGES FAILED TO DOWNLOAD. IF THIS ERROR PERSISTS, TRY TO INSTALL IT YOURSELF." + ConsoleColors.RESET)
            return
    print(ConsoleColors.GREEN + "Successfully downloaded all the needed python libraries!                                           " + ConsoleColors.CYAN + "\n-------------------------------------------------------------------------------------------------" + ConsoleColors.RESET)

def download_github(url):
    import requests

    try:
        os.mkdir("Nugs-Downloader")
    except:
        pass
    os.chdir("Nugs-Downloader")

    try:
        response = requests.get(url)
        release_data = json.loads(response.text)
        latest_release = release_data["tag_name"]
        assets = release_data["assets"]

        print(ConsoleColors.MAGENTA + "Downloading github files..." + ConsoleColors.RESET)

        # Download the latest assets
        print(progress_bar(0, 100), end='\r', flush=True)
        count = 0
        for asset in assets:
            asset_name = asset["name"]
            asset_url = asset["browser_download_url"]
            print(ConsoleColors.MAGENTA + f"Downloading {asset_name: <30} {progress_bar(((count+1)/len(assets)) * 100, 100)}" + ConsoleColors.RESET, end='\r', flush=True)
            response = requests.get(asset_url)
            with open(asset_name, "wb") as file:
                file.write(response.content)
            count += 1

        print(ConsoleColors.GREEN + "Successfully downloaded all the needed github files!                                           " + ConsoleColors.CYAN + "\n-------------------------------------------------------------------------------------------------" + ConsoleColors.RESET)
    except:
         print(ConsoleColors.RED + "ERROR: SOMETHING WENT WRONG AND ONE OF THE FILES FAILED TO DOWNLOAD. IF THIS ERROR PERSISTS, TRY TO DOWNLOAD IT YOURSELF." + ConsoleColors.RESET)

def manage_config_file(directory):

    print(ConsoleColors.MAGENTA + "Creating  a config file..." + ConsoleColors.RESET)

    email = input(ConsoleColors.BOLD + "Please input your nugs.net email: " + ConsoleColors.RESET)
    password = input(ConsoleColors.BOLD + "Please input your nugs.net password: " + ConsoleColors.RESET)
    data = {
    "email": email,
    "password": password,
    "format": 4,
    "videoFormat": 5,
    "outPath": "Nugsdownloads",
    "token": "",
    "useFfmpegEnvVar": False
}
    os.chdir(directory)
    file_path = "config.json"  # Specify the desired file path

    # Write the data to a JSON file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

    print(ConsoleColors.GREEN + f"JSON file '{file_path}' created successfully!                                           " + ConsoleColors.CYAN + "\n-------------------------------------------------------------------------------------------------" + ConsoleColors.RESET)

def download_ffmpeg(directory):
    import requests

    print(ConsoleColors.MAGENTA + "Downloading ffmpeg files..." + ConsoleColors.RESET)

    os.chdir(directory)
    url = 'https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-win64-gpl.zip'
    save_path = 'ffmpeg-master-latest-win64-gpl.zip'
    extract_path = 'ffmpeg-master'

    response = requests.get(url)
    response.raise_for_status()

    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(ConsoleColors.GREEN + "Successfully downloaded ffmpeg.zip!" + ConsoleColors.RESET)

    with zipfile.ZipFile(save_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print(ConsoleColors.GREEN + "Successfully unzipped ffmpeg.zip!" + ConsoleColors.RESET)

    os.chdir(directory + "\\ffmpeg-master\\ffmpeg-master-latest-win64-gpl\\bin")
    for file in os.listdir():
        try:
            shutil.move(directory + "\\ffmpeg-master\\ffmpeg-master-latest-win64-gpl\\bin\\" + file, directory)
        except:
            print(ConsoleColors.RED + "ERROR: FILE ALREADY EXISTS! PLEASE MAKE SURE TO DELETE ALL FFMPEG FILES FIRST!")
            return
    print(ConsoleColors.GREEN + "Successfully moved all .exes to Nugs-Downloader directory!" + ConsoleColors.RESET)

    os.remove(directory + "\\ffmpeg-master-latest-win64-gpl.zip")
    print(ConsoleColors.GREEN + "Successfully deleted the extraneous ffmpeg.zip file!" + ConsoleColors.RESET)

starting_directory = get_current_file_directory()
os.chdir(starting_directory)
package_names = ["bs4", "google", "mutagen", "urllib3", "requests"]
install_package(package_names)
download_github("https://api.github.com/repos/Sorrow446/Nugs-Downloader/releases/latest")
manage_config_file(starting_directory + "Nugs-Downloader")
download_ffmpeg(starting_directory + "Nugs-Downloader")
print(ConsoleColors.CYAN + "\n-------------------------------------------------------------------------------------------------" + ConsoleColors.GREEN + "\nProgram finished successfully!" + ConsoleColors.RESET)
print(ConsoleColors.BOLD + "Press any key to exit..." + ConsoleColors.RESET)
input()
