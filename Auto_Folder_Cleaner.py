from threading import Thread
from pyfiglet import Figlet
import tkinter.filedialog
import datetime as dt
import tkinter as tk
import fnmatch
import socket
import shutil
import time
import json
import sys
import os

if socket.gethostname() == 'Aperture-Two':
    config = 'personal_config.json'
else:
    config = 'config.json'
with open(config) as json_file:
    data = json.load(json_file)

'''These variables, lists and disctionaries are pulled from
the config file to allow for easier customization without touching the main code.'''
# Settings
watched_folder = data['settings']['watched_folder']  # Default watcher folder.
autostart = data['settings']['autostart']  # Autostart using default folder toggle.

# Dictionaries
file_type_groups = data['dictionaries']['file_type_groups']  # Sets file types into groups.
file_group_dest = data['dictionaries']['file_group_dest']  # Sets destination based on file group.
keywords_dest = data['dictionaries']['keywords_dest']  # Checks for keywords in file names.
special_case_dest = data['dictionaries']['special_case_dest']  # Lists special cases for file type destinations.
delete_def = data['dictionaries']['delete_def']  # Lists file types that you might want to delete.


def Get_File_Type(f):
    '''Gets file type from the given file name.'''
    file_type = ''
    split_string = f.split(".")
    if len(split_string) == 2:
        file_type = f'.{split_string[1]}'
    else:
        print()
    return file_type


def Set_Destination(watched_folder, f):
    '''This function checks for matches for file extensions and keywords.
    It sets the destination for the file or sets it to skip if the file was deleted.'''
    destination = 'skip'
    file_type = Get_File_Type(f)
    for file_group, file_type_list in file_type_groups.items():
        if file_type in file_type_list:
            destination = file_group_dest[file_group]
            if file_type in delete_def:
                del_resp = input(f'{f} found.\nDo you want to delete it?\n')
                if del_resp == 'yes' or del_resp == 'y':
                    os.remove(os.path.join(watched_folder, f))
                    print('Deleted File.')
                    return 'skip'
            for keyword, keyword_data in keywords_dest.items():
                if file_group in keyword_data:
                    destination = keyword_data[1]
                    print(destination)
    return destination


def File_Move(watched_folder, target, destination):
    '''Moves Target file to Destination after making the destination directory if it does not exist.
    It will also leave the file where it is if it already exists at the destination.'''
    if os.path.isdir(destination) is False:
        os.mkdir(destination)
    if os.path.exists(os.path.join(destination, target)):
        print(f'{target} already exists at destination.\nLeaving file as is.')
    else:
        shutil.move(os.path.join(watched_folder, target), destination)


threads = []  # Initializes the thead list for use in Move_By_Name() and Main()


# TODO Add progress bar
def Move_By_Name(watched_folder):
    '''This script checks each file in the watched folder and figures out the destination if any exist.
    Once a destinations are found, it moves the files via threads. It also returns a count of the total files moved.'''
    file_moved_count = 0
    for f in os.listdir(watched_folder):
        destination = Set_Destination(watched_folder, f)
        if destination != 'skip':
            file_moved_count += 1
            file_move_thread = Thread(target=File_Move, args=(watched_folder, f, destination))
            file_move_thread.start()
            threads.append(file_move_thread)
    return file_moved_count


def Set_Watched_Folder(watched_folder):
    '''Sets the Watched folder via tkinter Directory Dialog if you type cd. otherwise it uses what you entered for the watched folder.'''
    tk.Tk().withdraw()
    response = input("Press Enter to continue with default\nType cd to enter new directory\n")
    if response == 'cd':
        watched_folder = tk.filedialog.askdirectory(initialdir="C:/", title="Select Directory")
    if response == '':
        watched_folder = watched_folder
    return watched_folder


def Main(watched_folder):
    '''This is the main function that introduces the script and sets up backbone for everything.'''
    title = 'Auto Folder Cleaner'
    try:
        text = Figlet(font='slant')
        print(text.renderText(title))
    except:
        print(title)
    if autostart != 1:
        watched_folder = Set_Watched_Folder(watched_folder)
    else:
        print(f'Autostarting in {watched_folder}.')
    overall_start = time.perf_counter()
    file_moved_count = Move_By_Name(watched_folder)
    for thread in threads:
        thread.join()
    print(f'\nFinished file check of {watched_folder}.\n{file_moved_count} files moved.')
    overall_finish = time.perf_counter()
    elapsed_time = round(overall_finish-overall_start, 2)
    if elapsed_time != 0:
        converted_elapsed_time = str(dt.timedelta(seconds=elapsed_time))
    else:
        converted_elapsed_time = 'Instant'
    print(f'Overall Time Elapsed: {converted_elapsed_time}\n')
    input("Press Enter to Exit\n")
    sys.exit()


if __name__ == '__main__':
    Main(watched_folder)
