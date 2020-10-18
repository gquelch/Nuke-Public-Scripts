import nuke

def reloadAllReads():

    nodes = nuke.allNodes()
    
    for node in nodes:
        if node.Class() == "Read":
            node.knob("reload").execute()