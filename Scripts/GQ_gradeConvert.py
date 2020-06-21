import os
import nuke
import nukescripts


def gq_gradeConvertWin():

    p = nuke.Panel("GQ_gradeConvert")

    p.addEnumerationPulldown("Tone","Master Shadows Midtones Highlights") #get user input for colour correct target

    if not p.show():
        return

    target = p.value("Tone") #set user input to "target"

    gq_gradeConvert(target)

def gq_gradeConvert(target):
    if target == "Master":
        gain = "gain"
        gamma = "gamma"
        add = "offset"
    if target == "Shadows":
        gain = "shadows.gain"
        gamma = "shadows.gamma"
        add = "shadows.offset"
    if target == "Midtones":
        gain = "midtones.gain"
        gamma = "midtones.gamma"   
        add = "midtones.offset"    
    if target == "Highlights":
        gain = "highlights.gain"
        gamma = "highlights.gamma"  
        add = "highlights.offset" 

    mySel = nuke.root().selectedNodes()
    

    for i in mySel:
        if i.Class() == "Grade":
            c = nuke.nodes.ColorCorrect()

            #colour inputs
            c.knob(gain).setValue(i.knob("white").getValue())
            c.knob(gamma).setValue(i.knob("gamma").getValue())
            c.knob(add).setValue(i.knob("add").getValue())

            #mix and mask inputs
            c.knob("mix").setValue(i.knob("mix").getValue())
            iMaskInput = i.input(1)
            iColInput = i.input(0)

            c.connectInput(1,iMaskInput)
            c.connectInput(0,iColInput)

            #set position
            c.knob("xpos").setValue(i.knob("xpos").getValue()+100)
            c.knob("ypos").setValue(i.knob("ypos").getValue())

        else:
            print "this only works for grades"

gq_gradeConvertWin()
