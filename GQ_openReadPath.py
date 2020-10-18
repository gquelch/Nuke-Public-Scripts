import os
import nuke

nuke.root().begin()

def open_file():
    mySel = nuke.selectedNodes()

    for i in mySel:
        filePath = mySel[0].knob("file").getValue()

        filePathSplit = filePath.rsplit("/",1)

        os.startfile(filePathSplit[0])  