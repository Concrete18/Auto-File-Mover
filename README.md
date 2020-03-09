# Auto File Mover

This script searches a watched directory in order to move files based on their filetypes and keywords. It works by using For Loops to go through files in the watched directory. It checks for matches in a file type and keyword Dictionaries.

## Preferences Example
```Python
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
```
