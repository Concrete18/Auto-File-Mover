from threading import Thread
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

if  __name__ != '__main__':
    config = 'config.json'
elif socket.gethostname() == 'Aperture-Two':  # sets to my personal config instead of the example config on my pc
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
delete_def = data['dictionaries']['delete_def']  # Lists file types that you might want to delete.\


def Run_Delete_Empty_Folders(watched_folder):
    '''Deletes empty folders in the watched_folder entered as an argument.

    Keyword arguments:

    watched_folder -- folder watched within the main function

    f -- file that is being checked for file extension and keyword matches
    '''
    # checks config setting for deleting empty folders - enable/disable
    delete_empty_folders = data['settings']['delete_empty_folders']
    if delete_empty_folders == 1:
        delete_total = 0  # init var for total empty folders deleted
        for f in os.scandir(watched_folder):
            if os.path.exists(f.path) and not os.path.isfile(f.path):  # checks if f is a folder instead of a file
                if len(os.listdir(f.path)) == 0:  # detects if folder is empty
                    try:
                        os.rmdir(f.path)
                    except OSError:  # error check in case of unseen circumstance
                        print(f'Failed to delete {f.name}\nIt is not empty.')
                    delete_total += 1
            if delete_total > 0: # prints info if empty folders were deleted
                print('Deleted empty folders.')


def Get_File_Type(f):
    '''Gets file type from the given file name. It only uses the last period separating extension.'''
    file_type = ''
    split_string = f.name.split(".")
    file_type = f'.{split_string[-1]}'
    return file_type


def Set_Destination(watched_folder, f):
    '''This function looks for matches in file extensions and keywords.
    It sets the destination for the file or sets it to skip if the file was deleted.

    Keyword arguments:

    watched_folder -- folder watched within the main function

    f -- file that is being checked for file extension and keyword matches
    '''
    destination = 'skip'
    file_type = Get_File_Type(f)
    for file_group, file_type_list in file_type_groups.items():  # for loop that checks for file group matches
        if file_type in file_type_list:
            destination = file_group_dest[file_group]  # sets destination based on file group
            if file_type in delete_def: # checks for file types in delete whitelist
                del_resp = input(f'{f.name} found.\nDo you want to delete it? (Will skip recycle bin)\n')
                if del_resp == 'yes' or del_resp == 'y':
                    # TODO Add recycle bin support for windows
                    os.remove(f.path)
                    print('Deleted File.')
                    return 'skip' #  prevents file from being copied if it was deleted
            if file_type in special_case_dest:
                destination = special_case_dest[file_type] # sets destination based on special case
            for keyword, keyword_data in keywords_dest.items():  # for loop that checks for keyword matches
                if keyword.lower() in f.name.lower(): # checks for match with upper case removed
                    if file_type in keyword_data[0]:
                        destination = keyword_data[1]
                    elif file_group == keyword_data[0][0]:
                        destination = keyword_data[1]
    return destination  # end destination for file entered as f argument


def File_Move(target, destination):
    '''Moves Target file to Destination after making the destination directory if it does not exist.
    It will also leave the file where it is if it already exists at the destination.

    Keyword arguments:

    target -- file to move

    destination -- destination of target file
    '''
    if os.path.isdir(destination) is False:  # checks if destination directory exist
        os.mkdir(destination) # makes directory if it does not exist
    if os.path.exists(os.path.join(destination, target.name)): # checks if file was moved previously and cancels move
        print(f'{target.name} already exists at destination.\nLeaving file as is.')
    else:
        shutil.move(target.path, destination)


threads = []  # Initializes the thead list for use in Move_By_Name() and Main()


# TODO Add progress bar.
def Move_By_Name(watched_folder):
    '''This function checks each file in the watched folder and figures out the destination if any exist.
    Once a destinations are found, it moves the files via threads. It also returns a count of the total files moved.

    Keyword arguments:

    watched_folder -- folder watched within the main function
    '''
    files_moved_count = 0
    for f in os.scandir(watched_folder):
        if not f.name.startswith('.') and f.is_file():
            destination = Set_Destination(watched_folder, f)
            if destination != 'skip':  # skips file move if file was deleted in Set_Destination function
                files_moved_count += 1
                file_move_thread = Thread(target=File_Move, args=(f, destination))
                file_move_thread.start()
                threads.append(file_move_thread)
    return files_moved_count  # returns total files moved for use later


def Set_Watched_Folder(watched_folder):
    '''Sets the Watched folder via tkinter Directory Dialog if you type cd.
    Otherwise it uses default for the watched folder.

    Keyword arguments:

    watched_folder -- folder watched within the main function
    '''
    tk.Tk().withdraw() # hides blank tkinter window that pop up otherwise
    response = input("Press Enter to continue with default\nType cd to enter new directory\n")
    if response == 'cd':  # change directory command
        watched_folder = tk.filedialog.askdirectory(initialdir="C:/", title="Select Directory")
    return watched_folder


def Main(watched_folder):
    '''This is the main function that introduces the script and sets up the backbone for everything.

    Keyword arguments:

    watched_folder -- folder watched within the main function
    '''
    print('Auto Folder Cleaner')
    if autostart != 1:  # determines if program asks to change directory or not
        watched_folder = Set_Watched_Folder(watched_folder)
    else:
        print(f'Autostarting in {watched_folder}.')
    overall_start = time.perf_counter() # start time for checking elaspsed runtime
    file_moved_count = Move_By_Name(watched_folder)
    for thread in threads:
        thread.join()
    print(f'\nFinished file check of {watched_folder}.\n{file_moved_count} files moved.')
    Run_Delete_Empty_Folders(watched_folder)
    overall_finish = time.perf_counter() # stop time for checking elaspsed runtime
    elapsed_time = round(overall_finish-overall_start, 2)
    if elapsed_time != 0:  # converts elapsed seconds into readable format
        converted_elapsed_time = str(dt.timedelta(seconds=elapsed_time))
    else:
        converted_elapsed_time = 'Instant'
    print(f'Overall Time Elapsed: {converted_elapsed_time}\n')
    input("Press Enter to Exit\n")
    sys.exit()


if __name__ == '__main__':
    Main(watched_folder)
