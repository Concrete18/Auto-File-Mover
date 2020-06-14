# Auto Folder Cleaner

This script searches a watched directory in order to move files based on their filetypes and keywords. It works by using For Loops to go through files in the watched directory. It checks for matches in a file type and keyword Dictionaries.

## Preferences Example
```Python
WatchedFolderDef = 'D:/Downloads'

# Checks for keywords in file names.
KeywordDef = {
    'Wallpaper': 'D:/Downloads/Wallpapers',
}

# Checks for specific file types.
FileTypeDef = {
    '.docx': 'D:/Downloads/Documents',
    '.mp4': 'D:/Downloads/Video',
    '.png': 'D:/Downloads/Images',
    '.jpg': 'D:/Downloads/Images',
    '.txt': 'D:/Downloads/Documents',
    '.exe': 'D:/Downloads/Installers',
    '.wav': 'D:/Downloads/Audio Files',
}

# These file types will cause the script to ask if you want to delete them.
# No means it reverts to moving to FileTypeDef.
DeleteDef = {'.exe', '.test'}
```
