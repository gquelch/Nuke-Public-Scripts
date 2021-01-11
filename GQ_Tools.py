# Executing this script will add the panel to your Nuke Panel Menu, under "Custom"
#I recommended importing this script into your menu.py file in order for it always be available in Nuke
#I have a guide on that here:
#https://gquelch.github.io/2020/06/21/Simplify-Executing-and-Sharing-Nuke-Scripts/

# Version 4 #

import json
import sys
import os
import nuke
import nukescripts


# You can use this path to Auto-Fill the script search location
beginScriptsPath = r""


class GQ_Tools(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, "GQ_Tools")


        ## KNOBS ##
        # Node Disable #
        self.classInput = nuke.String_Knob("classInput","Type")
        self.classSelect = nuke.PyScript_Knob('classSelect', 'Select Type')

        self.enableAll = nuke.PyScript_Knob("enableAll", "Enable All")
        self.enableAll.setFlag(nuke.STARTLINE)

        self.disableHeavy = nuke.PyScript_Knob("disableHeavy", "Disable Heavy")

        self.disableDivider = nuke.Text_Knob("")

        # Read Properties #
        self.readBefore = nuke.Enumeration_Knob('readBefore', "Before", ['hold', "loop", "bounce", "black"])
        self.readAfter = nuke.Enumeration_Knob('readAfter', "Before", ['hold', "loop", "bounce", "black"])
        self.readAfter.clearFlag(nuke.STARTLINE)
        
        self.setBeforeAfter = nuke.PyScript_Knob("setBeforeAfter", "Set Before + After")


        self.readStart = nuke.Int_Knob('readStart', "Start", 100)
        self.readEnd = nuke.Int_Knob('readEnd', "End", 200)
        self.readEnd.clearFlag(nuke.STARTLINE)
        
        self.setStartEnd = nuke.PyScript_Knob("setStartEnd", "Set Start + End")

        self.startAt = nuke.Int_Knob('startAt', "Start At")
        self.setStartAt = nuke.PyScript_Knob("setStartAt", "Set Start At")

        self.readDivider = nuke.Text_Knob("")


        ## LAYOUT ##
        # Node Disable #
        self.addKnob(self.classInput)
        self.addKnob(self.classSelect)
        self.addKnob(self.enableAll)
        self.addKnob(self.disableHeavy)

        self.addKnob(self.disableDivider)

        # Read Properties #
        self.addKnob(self.readBefore)
        self.addKnob(self.readAfter)
        self.addKnob(self.setBeforeAfter)

        self.addKnob(self.readStart)
        self.addKnob(self.readEnd)
        self.addKnob(self.setStartEnd)
        self.addKnob(self.startAt)
        self.addKnob(self.setStartAt)

        self.readStart.setValue(int(nuke.Root()['first_frame'].getValue()))
        self.readEnd.setValue(int(nuke.Root()['last_frame'].getValue()))


    def knobChanged(self, knob):

        ## SCRIPTS ##
        if knob == self.classInput:
            gq_selectClass(self)        
        
        if knob == self.classSelect:
            gq_selectClass(self)

        if knob == self.enableAll:
            gq_enableAll()

        if knob == self.disableHeavy:
            gq_disableHeavy()

        if knob == self.setStartEnd:
            gq_setStartEnd(self)

        if knob == self.setBeforeAfter:
            gq_setBeforeAfter(self)

        if knob == self.setStartAt:
            gq_setStartAt(self)
    


## SCRIPT FUNCTIONS ##
def gq_selectClass(self):
    userClasses = self.classInput.getValue()

    userClassesSplit = userClasses.split(" ")

    nuke.root().begin()
    nuke.selectAll()
    allNodes = nuke.root().selectedNodes()

    for node in allNodes:
        if node.Class() not in userClassesSplit:
            node.setSelected(False)

def gq_enableAll():
    nuke.root().begin()
    nuke.selectAll()
    allNodes = nuke.selectedNodes()

    for node in allNodes:
        if node.knob("disable"):
            node.knob("disable").setValue( False )

        else:
            print (node.name() + " has no Disable")

def gq_disableHeavy():
    nuke.root().begin()
    allNodes = nuke.allNodes()
    classTypes = ["Defocus", "VectorBlur", "MotionBlur", "pgBokeh", "ZDefocus2"]

    for node in allNodes:
        for cType in classTypes:
            if cType in node.Class():
                node.knob("disable").setValue(True)

def gq_setBeforeAfter(self):
    nuke.root().begin()
    curNodes = nuke.root().selectedNodes()

    userBefore = int(self.readBefore.getValue())
    userAfter = int(self.readAfter.getValue())
   
    for n in curNodes:
       if n.Class() == "Read":

            n.knob("before").setValue(userBefore)
            n.knob("after").setValue(userAfter)

def gq_setStartEnd(self):
    nuke.root().begin()
    curNodes = nuke.root().selectedNodes()
    
    startFrame = int(self.readStart.getValue())
    endFrame = int(self.readEnd.getValue())
    
    for n in curNodes:
        if n.Class() == "Read":  
            n.knob("first").setValue(int(startFrame))
            n.knob("origfirst").setValue(int(startFrame))
            n.knob("last").setValue(int(endFrame))
            n.knob("origlast").setValue(int(endFrame))

def gq_setStartAt(self):
    nuke.root().begin()
    curNodes = nuke.root().selectedNodes()
    
    startAt = str(self.startAt.getValue())
    
    for n in curNodes: 
        if n.Class() == "Read":
            n.knob("frame_mode").setValue("1")
            n.knob("frame").setValue(startAt)

def showPanel():
    GQ_Tools().show()

def addPanel():
    return GQ_Tools().addToPane()

def addPanelToPane():
    paneMenu = nuke.menu('Pane')
    paneMenu.addCommand('GQ_Tools', addPanel)
    nukescripts.registerPanel('com.ohufx.GQ_Tools', addPanel)