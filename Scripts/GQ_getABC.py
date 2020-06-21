import os
import nuke


def GQ_getABC():
    nuke.root().begin()
    
    abcList = []
    geoLoop = 0
    replaceCam = False
    

    mySel = nuke.root().selectedNodes()
    
    alembicPath = GQ_getABCPath()

    #get folders and contents
    for path, subdirs, files in os.walk(alembicPath):
        for file in files:
            if file.endswith(".abc"):
                abcList.append(file)


    #UI for selecting alembics
    p = nuke.Panel("GQ_getABC")
    for i in abcList:
        p.addBooleanCheckBox(i,False)

    if not p.show():
        return



    #selection Dict
    ABCDict = {}

    for i in abcList:
        ABCDict[i] = p.value(i)

    #check for ABCs marked as True, and return as 2 lists (Cam + Geo)
    importABCLists = GQ_ABCTypeCheck(ABCDict)

    camList = importABCLists[0]
    geoList = importABCLists[1]
 

    if len(camList) == 1:
        if len(mySel) == 1:
            if mySel[0].Class() == "Camera2":
                p2 = nuke.Panel("overWrite_Check")

                p2.addBooleanCheckBox("replace selected camera?",False)

                if not p2.show():
                    return

                replaceCam = p2.value("replace selected camera?")    
    
    for cam in camList:
        camPath = alembicPath + "/" + cam

        #repalce selected camera
        if replaceCam == True:    
            mySel[0].knob("file").setValue(camPath)
            mySel[0].knob("frame_rate").setValue(nuke.root()["fps"].getValue())        

        #creating new cameras
        if replaceCam == False:
            c = nuke.nodes.Camera2()

            c.knob("read_from_file").setValue(True)
            c.knob("file").setValue(camPath)
            c.knob("frame_rate").setValue(nuke.root()["fps"].getValue())

            if len(mySel) > 0:
                c.knob("xpos").setValue(mySel[0].knob("xpos").getValue()-150)
                c.knob("ypos").setValue(mySel[0].knob("ypos").getValue()-25)

    for geo in geoList:
        geoPath = alembicPath + "/" + geo

        rg = nuke.nodes.ReadGeo2()

        rg.knob("file").setValue(geoPath)
        rg.knob("frame_rate").setValue(nuke.root()["fps"].getValue())

        if len(mySel) > 0:
            if geoLoop == 0:
                rg.knob("xpos").setValue(mySel[0].knob("xpos").getValue()-250)
                rg.knob("ypos").setValue(mySel[0].knob("ypos").getValue()-25)
            elif geoLoop > 0:
                rg.knob("xpos").setValue(lastRg.knob("xpos").getValue()-100)
                rg.knob("ypos").setValue(lastRg.knob("ypos").getValue())

            geoLoop += 1
            lastRg = rg

def GQ_getABCPath():
    ## Get ABC Path ##

    #file path
    path = nuke.root().knob('name').value()

    '''
    This is where you want to  get the path to your alembics
    This will be different for different studios
    Some places will alembic to a different drive, some to a "publish" version of that shot
    You should be able to retrieve this information from either the shot name itself
    or what i opt for is from the full file path, this usually contains the information, 
    and means you dont need to worry about file naming
    
    You want to return the full path to the folder containing your alembics

    '''


    abcPath =

    return abcPath

def GQ_ABCTypeCheck(ABCDict):
    ## Split ABC Types ##

    geoList = []
    camList = []

    for key in ABCDict:
        if ABCDict[key] == True:

            '''
            Here you want to seperate out 2 types of alembics: Geometry and Cameras
            They both require different nodes to be created in Nuke, meaning we need to define the difference
            I have left an example below where I am checking the file name for either "Rigging" or "Camera"
            
            You may cache things based on obj type, e.g CAM, PRP, CHR, VHL, in which case you could use this to define
            
            if "CAM" in key:
                camList.append(key)

            if "GEO" in key:
                geoList.append(key)
            '''

    return camList, geoList
    
   
GQ_getABC()

