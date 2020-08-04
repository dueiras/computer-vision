 import os
 def change_extension(path, extension):
     """
     A function that changes the extensions of all images in a folder

    --------
     INPUTS
    -Path: (str) the folder path for the imagens
    -Extension: (str) the desirable extension, as ".png" e.g.
     """  
    for filename in os.listdir(path):
        prefix = filename.split(".")[0]
        new_filename = path + '\\' + prefix + extension
        try:
            os.rename(path+'\\'+filename, new_filename)
        except FileExistsError:
            #If the file was already changed before
            pass