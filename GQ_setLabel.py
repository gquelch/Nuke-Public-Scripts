import nuke

def gq_setLabel():

    nuke.root().begin()
    nodeSel = nuke.root().selectedNodes()

    if len(nodeSel) > 0:

        p = nuke.Panel("GQ_SetLabel")

        p.addSingleLineInput('New Label', nodeSel[0].knob("label").getValue())
        p.addBooleanCheckBox('TCL Value?', False)

        if not p.show():
            return

        label = p.value("New Label")
        TCLCheck = p.value("TCL Value?")

        if TCLCheck == True:
            label = "[ value " + label + " ]"
        else:
            pass



            
        for node in nodeSel:

            if node.Class() == "Group":
                node.begin()

                groupNodeSel = nuke.selectedNodes()
                
                for groupNode in groupNodeSel:
                    groupNode.knob("label").setValue(label)

        
            node.knob("label").setValue(label)
    
    else:
        print "Please select a node"