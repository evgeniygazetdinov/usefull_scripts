#all operation move and creating subfolder


import os
import subprocess

class File_manager:
    def __init__(self):

        self.home_folder = 'image_parser'


    def find_path(self):
        return os.getcwd()


    def take_home(self):
        return os.environ['HOME']+'/'+self.home_folder

    def move_to_root(self):
        root = self.take_home()
        os.chdir(root)


    def create_folder(self,name_folder):
        subprocess.call("mkdir {}".format(str(name_folder)),shell = True)


    def move_to_directory(self,name_folder):
        path = self.take_home()
        os.chdir(path+'/'+str(name_folder))


    def create_and_move(self,name_folder):
        self.create_folder(name_folder)
        print(os.getcwd())
        print("folder {} created!".format(name_folder))
        self.move_to_directory(name_folder)
        print("You in  {} folder!".format(name_folder))



