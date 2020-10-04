import nuke
import nukescripts


def GQ_branchMask():
    mySel = nuke.root().selectedNodes()
    
    # Duplicate + Mask Loop
    for i in mySel:

        for n in nuke.allNodes():
            n.setSelected(False)

        iMask = i.input(1)
        iInput = i.input(0)
            
        newNode = nuke.createNode(i.Class(), i.writeKnobs(nuke.WRITE_NON_DEFAULT_ONLY | nuke.TO_SCRIPT), inpanel=False)
        newNode.knob("name").setValue(i.knob("name").getValue() + "_copy")
   
        newNode.knob("xpos").setValue(i.xpos()-100)
        newNode.knob("ypos").setValue(i.ypos())

        newNode.connectInput(1,iMask)

    
    # Inputs Loop
    for i in mySel:
        
        iInput = i.input(0)

        newNode = nuke.toNode(i.name() + "_copy")

        try:
            name = iInput.name() + "_copy"
 
            copiedNode = nuke.toNode(name)
            if copiedNode is not None:
                iInput = copiedNode
            else:
                pass
    
            newNode.connectInput(0,iInput)
        except:
            pass
            # node has no input