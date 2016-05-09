import os

f_zip = "arxiv2git.zip"

def package():
    clean()
    cmd = 'zip {} *.json *.js *.css *.png'
    os.system(cmd.format(f_zip))

def clean():
    os.system("rm -vf {}".format(f_zip))
    os.system("rm -vf *~ \#*")
