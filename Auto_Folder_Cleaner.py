from pyfiglet import Figlet
import tkinter.filedialog
import tkinter as tk
import threading
import fnmatch
import shutil
import time
import sys
import os

# Checks for keywords in file names.
# Todo Set to only count keywords for certain file types.

KeywordDef = {
    'Wallpaper': 'C:/Downloads/Wallpapers',
}

file_type_def = {
    'image': ('.jpg', '.png', '.gif'),
    'video': ('.mp4', '.wave')
}

# Checks for specific file types.
file_def_loc = {
    '.docx': 'C:/Downloads/Documents',
    '.mp4': 'C:/Downloads/Video',
    '.png': 'C:/Downloads/Images',
    '.jpg': 'C:/Downloads/Images',
    '.txt': 'C:/Downloads/Documents',
    '.exe': 'C:/Downloads/Installers',
    '.wav': 'C:/Downloads/Audio Files',
    '.zip': 'C:/Downloads/Compressed Files',
    '.rar': 'C:/Downloads/Compressed Files',
    '.7z': 'C:/Downloads/Compressed Files',
}

WatchedFolderDef = 'D:/Downloads'
WatchedFolder = ''
autostart = 0 #  Set to 1 to autostart without asking for if you want to change the directory.

# These file types will cause the script to ask if you want to delete them.
# Inputting yes/y deletes the .exe file.
# Inputting no/n means it reverts to moving to file_def_loc.
DeleteDef = {'.exe', '.test', '.zip', '.rar', '.7z'}
threads = []

def FileMove(Target, Dest):
    if Dest != 'cancel':
        if os.path.isdir(Dest) is False:
            os.mkdir(Dest)
        if os.path.exists(f'{Dest}/{Target}'):
            print('File already exists. Leaving File where it is.')
            return
        file_size = os.path.getsize(f'{WatchedFolderDef}/{Target}')/(1024*1024*1024) # Converts bytes to gigs - Use /(1024*1024) if MB
        if  round(file_size, 2) > 1:
            print('Large File Found, prepare for longer then normal transfer.')
        shutil.move(WatchedFolderDef + '/' + Target, Dest)

def FileDelete(Target, Type):
    MoveDestination = ''
    dont_cancel = True
    InstallerDelResp = input(f'{Target} found.\nDo you want to delete it?\n')
    if InstallerDelResp == 'yes' or InstallerDelResp == 'y':
        os.remove(f'{WatchedFolderDef}/{Target}')
        print('Deleted File.')
        dont_cancel = False
    elif InstallerDelResp == 'no' or InstallerDelResp == 'n':
        print(f'Ok, copying {Target} to the {Type} default folder.\n')
    else:
        print(f'Unknown Response, copying {Target} to the {Type} default folder.\n')
    if dont_cancel:
        FileMove(Target, file_def_loc[Type])

def MoveByName(TargetDir):
    for File in os.listdir(TargetDir):
        for FileType in file_def_loc:
            if File.endswith(FileType):
                OutputText = f'Specific {FileType} not found.\nMoving file named {File} to default folder.\n'
                MoveDestination = file_def_loc[FileType]
                for Keyword in KeywordDef:
                    if fnmatch.fnmatch(File, f'*{Keyword}*'):
                        OutputText = f'{Keyword} keyword found in file named {File}.\n'
                        MoveDestination = KeywordDef[Keyword]
                for ToDel in DeleteDef:
                    if fnmatch.fnmatch(File, f'*{ToDel}*'):
                        FileDelete(File, ToDel)
                        MoveDestination = False
                print(OutputText)
                if MoveDestination:
                    t = threading.Thread(target=FileMove, args=(File, MoveDestination))
                    t.start()
                    threads.append(t)

def StartFunction():
    tk.Tk().withdraw()
    WatchedFolder = input("Press Enter to continue with default\nType cd to enter new directory\n")
    if WatchedFolder == 'cd':
        WatchedFolder = tk.filedialog.askdirectory(initialdir="C:/", title="Select Directory")
        if WatchedFolder == '':
            print('No Directory Selected\nSwitching to Default Directory.\n')
            WatchedFolder = WatchedFolderDef
    else:
        WatchedFolder = WatchedFolderDef
    return WatchedFolder

if __name__ == '__main__':
    title = 'Auto Folder Cleaner'
    try:
        text = Figlet(font='slant')
        print(text.renderText(f'{title}\n'))
    except:
        print(title)
    if autostart != 1:
        WatchedFolder = StartFunction()
    else:
        WatchedFolder = WatchedFolderDef
        print(f'Autostarting in {WatchedFolderDef}.\n')
        overall_start = time.perf_counter()
        MoveByName(WatchedFolder)

    for thread in threads:
        thread.join()

    print(f'Finished File check of {WatchedFolder}.')
    overall_finish = time.perf_counter()
    elapsed_time = round(overall_finish-overall_start, 2)
    print(f'Overall Time Elapsed: {elapsed_time} Seconds.\n')

    input("Press Enter to Exit")
    sys.exit()
