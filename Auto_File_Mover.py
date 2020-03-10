import os
import sys
import shutil
import fnmatch

WatchedFolder = 'D:/Downloads'

KeywordDef = {
    'Wallpaper': 'D:/Google Drive/Photos/Wallpapers'
}

FileTypeDef = {
    '.docx': 'D:/Downloads/Documents',
    '.mp4': 'D:/Downloads/Video',
    '.png': 'D:/Downloads/Images',
    '.jpg': 'D:/Downloads/Images',
    '.txt': 'D:/Downloads/Documents',
    '.exe': 'D:/Downloads/Installers'
}


def FileMove(Target, Dest):
    if os.path.isdir(Dest) is True:
        pass
    else:
        os.mkdir(Dest)
    shutil.move(WatchedFolder + '/' + Target, Dest)
    print('Move Complete.')


#  todo reincorporate into MoveByName Function.
def FileDelete(Target, Type):
    print('Found an ' + Type + ' named ' + Target + '.')
    InstallerDelResp = input('Do you want to delete it?')
    if InstallerDelResp == 'yes' or InstallerDelResp == 'y':
        os.remove(WatchedFolder + '/' + Target)
        print('Deleted File.')
    else:
        print('Ok, copying ' + Target + 'to the ' + Type + ' default folder.')
        shutil.move(WatchedFolder + '/' + Target, FileTypeDef[Type])


def MoveByName(TargetDir):
    for File in os.listdir(TargetDir):
        for FileType in FileTypeDef:
            if File.endswith(FileType):
                print(File + " Found.")
                OutputText = 'Specific ' + FileType + ' not found. Moving file named ' + File + ' to default folder.'
                MoveDestination = FileTypeDef[FileType]
                for keyword in KeywordDef:
                    if fnmatch.fnmatch(File, '*' + keyword + '*'):
                        OutputText = keyword + ' Found named ' + File
                        MoveDestination = KeywordDef[keyword]
                print(OutputText)
                FileMove(File, MoveDestination)


WatchedFolderSet = input("Press Enter to continue with default \n Type cd to enter new directory") or WatchedFolder
MoveByName(WatchedFolderSet)
print('Finished File check of ' + WatchedFolderSet + '.')
input("Press Enter to Exit")
sys.exit()
