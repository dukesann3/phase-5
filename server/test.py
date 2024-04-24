import os

dir_path = os.path.dirname(os.path.realpath(__file__))

for root, dirs, files in os.walk(dir_path):
    for file in files: 
 
        # change the extension from '.mp3' to 
        # the one of your choice.
        print(file)
        if file.endswith('.jpg'):
            print (root+'/'+str(file))