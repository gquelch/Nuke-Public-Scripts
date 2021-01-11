menubar=nuke.menu("Nuke")
m=menubar.addMenu("MyMenu")

try:
    import GQ_Tools
    m.addCommand("GQ_Tools", "GQ_Tools.showPanel()")

    import reloadAllReads
    m.addCommand("reloadAllReads", "reloadAllReads.reloadAllReads()")
    
    import GQ_gradeConvert
    m.addCommand("GQ_gradeConvert", "GQ_gradeConvert.gq_gradeConvertWin()")

    import GQ_branchMask
    m.addCommand("GQ_branchMask", "GQ_branchMask.GQ_branchMask()", "CTRL+ALT+B")

    import GQ_openReadPath
    m.addCommand("GQ_openReadPath", "GQ_openReadPath.open_file()")

    import GQ_setLabel
    m.addCommand("GQ_setLabel", "GQ_setLabel.gq_setLabel()", "ALT+L")
    
except:
    Exception,e: print str(e)