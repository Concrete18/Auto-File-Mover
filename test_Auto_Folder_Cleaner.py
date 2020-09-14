from Auto_Folder_Cleaner import Set_Destination, Get_File_Type
from unittest.mock import patch
import unittest
import json
import os

class TestAFC(unittest.TestCase):

    files = ['videofile.mkv', 'wallpaper.png', 'wallpaper.mp4']
    main_dir = os.getcwd()

    def setUp(self, files, main_dir):
        os.makedirs(os.path.join(main_dir, 'testing'))
        os.chdir(os.path.join(main_dir, 'testing'))
        for _file in files:
            with open(_file, "x")  as f:
                f = open(_file, "w")
                f.write("Test Text")
        os.chdir(main_dir)

    def test_Set_Destination(self):
        # Tests for correct file destination being returned properly based on json config.
        self.assertEqual(Set_Destination('C:/Downloads', 'videofile.mkv'), "C:/Downloads/HD Videos")
        self.assertEqual(Set_Destination('C:/Downloads', 'wallpaper.png'), "D:/Google Drive/Photos/Wallpapers")
        self.assertEqual(Set_Destination('C:/Downloads', 'wallpaper.mp4'), "C:/Downloads/Videos")


    def test_Get_File_Type(self):
        # Tests Get_File_Type function to be sure it works with a variety of file names.
        self.assertEqual(Get_File_Type('wallpaper.png'), ".png")
        self.assertEqual(Get_File_Type('wallpaper.png.zip'), ".zip")
        self.assertEqual(Get_File_Type('wal.l.pap.er.p.n.g.zip'), ".zip")

    # def test_Delete_Check(self):
    #     # Tests to see if function asks to delete files in delete_def.
    #     self.assertEqual(Set_Destination('C:/Downloads', 'installer.exe'), "skip")

    def tearDown(self, main_dir):
        for _file in files:
            os.rmdir(os.path.join(main_dir, 'testing'))


if __name__ == '__main__':
    unittest.main()
