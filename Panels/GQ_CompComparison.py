import os
import json
import nuke
import nukescripts

# Create Folder + Files #
shotDataFolder = r"C:\NukeComparisonTool"
shotDataFile = "shots.json"

shotsDataPath = r"C:\NukeComparisonTool\shots.json"

if os.path.exists(shotDataFolder) == False:
    os.mkdir(shotDataFolder)

if os.path.exists(shotsDataPath) == False:
    f = open(shotsDataPath, "w")
    f.close()


class GQ_shotComparison(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, "GQ_shotComparison")
        
        try:
            shotsData = getData(shotsDataPath)
        except:
            shotsData =  ""
            print "no data yet"
                
        setupsList = ["New_Setup"]
        
        for key in shotsData:
            setupsList.append(key)

        

        ## KNOBS ##        
        self.setups = nuke.Enumeration_Knob('setups', "Setups", setupsList)
        
        self.newSetupName = nuke.String_Knob("newSetupName","Name")
        self.newSetupName.clearFlag(nuke.STARTLINE)
      
        self.shotPath = nuke.File_Knob("shotPath","Shot Path")    

        self.addPath = nuke.PyScript_Knob("addPath", "Add Path")
        self.addPath.setFlag(nuke.STARTLINE)
        
        self.setupShots = nuke.Multiline_Eval_String_Knob("setupShots", "Shots in Setup")
        self.setupShots.setEnabled(False)
        
        self.createReads = nuke.PyScript_Knob("createReads", "Create Reads")
        self.createReads.setFlag(nuke.STARTLINE)
        
        self.deleteDivider = nuke.Text_Knob("")

        self.selectShot = nuke.Enumeration_Knob('selectShot', "Remove Shot", [""])
        self.selectShot.setFlag(nuke.STARTLINE)        
        self.removeShot = nuke.PyScript_Knob("removeShot", "Remove Selected Shot")
        self.removeShot.clearFlag(nuke.STARTLINE)
        
        self.removeSetup = nuke.PyScript_Knob("removeSetup", "Remove Selected Setup")
        self.removeSetup.setFlag(nuke.STARTLINE)

     
        ## LAYOUT ##
        self.addKnob(self.setups)
        self.addKnob(self.newSetupName)
        self.addKnob(self.shotPath)
        self.addKnob(self.addPath)
        self.addKnob(self.setupShots)
        self.addKnob(self.createReads)
        
        self.addKnob(self.deleteDivider)
        
        self.addKnob(self.selectShot)
        self.addKnob(self.removeShot)
        self.addKnob(self.removeSetup)

        
        
    def knobChanged(self, knob):
        
        ## SCRIPTS ##
        if knob == self.setups:
            setupSelected = self.setups.value()
            
            if setupSelected == "New_Setup":
                self.setupShots.setValue("")
            
            else:        
                gq_updateShots(self, setupSelected)
        
        if knob == self.addPath:     
            setupSelected = self.setups.value()
            pathSelected = self.shotPath.value()
        
            gq_addShots(self, setupSelected, pathSelected)
            
            
        if knob == self.removeShot:
            setupSelected = self.setups.value()
            shotSelected = self.selectShot.value()
            
            if setupSelected == "New_Setup":
                pass
            
            else:        
                gq_removeDictKey(self, setupSelected, shotSelected)           
            
        if knob == self.removeSetup:        
            setupSelected = self.setups.value()
            
            if setupSelected == "New_Setup":
                pass
            
            else:        
                gq_removeDictEntry(self, setupSelected)
                
        if knob == self.createReads:        
            setupSelected = self.setups.value()
            
            if setupSelected == "New_Setup":
                pass
            
            else:        
                gq_createReads(self, setupSelected)
            
            
def gq_addShots(self, setup, path):
    try:
        shotsData = getData(shotsDataPath)
    except:
        shotsData =  {}
        print "no data yet"

    # Create new setup Dict Entry #
    if setup == "New_Setup":
        newSetupStr = self.newSetupName.getValue()
        self.newSetupName.setValue("")
        
        x = {newSetupStr: {}}

        shotsData.update(x)


        setupsList = ["New_Setup"]        
        for key in shotsData:
            setupsList.append(key)
            
        self.setups.setValues(setupsList)
        
        self.setups.setValue(newSetupStr)

        setup = newSetupStr
        
           
    if len(shotsData[setup].items()) == 0:
        newShotInt = 1
    else:    
        newShotInt = int(sorted(shotsData[setup])[-1].split("_")[1]) + 1

    newShotStr = "shot_" + str(newShotInt).zfill(3)
    


    x = {newShotStr: path}

    shotsData[setup].update(x)
    
    writeData(shotsData,shotsDataPath)
    
    self.shotPath.setValue("")
    
    
    gq_updateShots(self, setup)
    
def gq_updateShots(self, setup):
    shotData = getData(shotsDataPath)
    
    shotsList = []
    shotNames = []
    
    
    for key in sorted(shotData[setup]):
        #getting file name
        shotNameSplit = shotData[setup][key].split("/")[-1]
        
        line = key + ": " + shotNameSplit
        shotsList.append(line)
        shotNames.append(key)
        
    shotsString = "\n".join(shotsList)

    self.setupShots.setValue(shotsString)
    self.selectShot.setValues(shotNames)

def gq_removeDictEntry(self, setup):
    shotsData = getData(shotsDataPath)
    
    del shotsData[setup]
    
    writeData(shotsData,shotsDataPath)
    
    setupsList = ["New_Setup"]
    for key in shotsData:
        setupsList.append(key)    
        
    self.setups.setValues(setupsList)
    self.setups.setValue(0)
    self.setupShots.setValue("")

def gq_removeDictKey(self, setup, shot):
    shotsData = getData(shotsDataPath)
    
    del shotsData[setup][shot]
    writeData(shotsData,shotsDataPath)
    
    if len(shotsData[setup].keys()) == 0:
        gq_removeDictEntry(self, setup)
    
    else:
        gq_updateShots(self, setup)
        
def gq_createReads(self, setup):
    shotsData = getData(shotsDataPath)
    frameHoldList = []

    for key in shotsData[setup]:
        file = shotsData[setup][key]
        

        fileSplit = file.rsplit("/",1)
        


        for seq in nuke.getFileNameList(fileSplit[0]):
            seqSplit = seq.split(".")[0]
            fileNameSplit = fileSplit[1].split(".")[0]

            
            if seqSplit == fileNameSplit:
                r = nuke.nodes.Read()
                r.knob("file").fromUserText(fileSplit[0] + "/" + seq)
                
                fh = nuke.nodes.FrameHold()
                fh.connectInput(0,r)
                
                frameHoldList.append(fh)
     

    # Contact Sheet #
    cs = nuke.nodes.ContactSheet()
    cs.knob("width").setExpression("inputs<=3?width*inputs:width*3")
    cs.knob("height").setExpression("height*rows")
    cs.knob("rows").setExpression("inputs<=3?1:2")
    cs.knob("columns").setExpression("inputs<=3?inputs:3")
    cs.knob("roworder").setValue(0)
    
    i = 0    
    while i < len(frameHoldList):
        cs.connectInput(i,frameHoldList[i])
        i += 1

def getData(shotsDataPath):      
    
    shotSetups = json.load(open(shotsDataPath))

    return shotSetups

def writeData(dict,shotsDataPath):

    json.dump(dict, open(shotsDataPath,"w"))


def showPanel():
    p = GQ_shotComparison()
    p.showModalDialog()

def addPanel():
    return GQ_shotComparison().addToPane()


def addPanelToPane():
    paneMenu = nuke.menu('Pane')
    paneMenu.addCommand('GQ_shotComparison', addPanel)
    nukescripts.registerPanel('com.ohufx.GQ_shotComparison', addPanel)
    #GQ_shotComparison().show()
    
addPanelToPane()
