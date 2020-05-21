## GQ_Tools

This is my *Master* Tool, it has a few built in functions, but one of the main things it can do is load and execute python scripts, this is a problem I have faced at some studios where it is more difficult to add python scripts into the Nuke UI, this script allows you to get around that.

The first line of the script is for you to add a path, I set this to whever I am currently saving my scripts, you might want to change this per project, or to a global scripts directory on a network drive, but it will initially populate the UI with scripts in this folder

(You can change this path on the fly once the panel has been created, but it will always default to this when made fresh)

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/25415e4a-5318-4918-b52e-a8c020f5d400/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/25415e4a-5318-4918-b52e-a8c020f5d400/Untitled.png)

### Selection Tools

The top set of tools have some quick actions that let you select nodes by class, you just write each class you want to select, seperated by spaces

E.g

Blur Grade Defocus

You can also "Enable all" to enable every node in your script

"Disable Heavy" will disable some regularly used slow nodes:

- Defocus
- VectorBlur
- MotionBlur
- pgBokeh
- ZDefocus

I'm planning to add a UI soon that will allow you to pick which nodes you consider Heavy, rather than hard-coding them myself

### Read Properties

These are fairly self explanatory, allowing you to change properties of all the read nodes you have selected.

### Scripts UI

**Scripts Path** is where you add the directory in which your scripts are saved, this will load automatically when you hit Enter

**Filter Scripts** allows you to search through scripts in that directory

**Found Scripts** will display the scripts in that directory with any filter applied

The dropdown at the bottom of the UI is where you pick and choose the script you want to run

## ReloadAllReads

This script will simply reload all Read nodes in your Nuke file

## gradeConvert

Sometimes I find myself working on a grade node, and deciding I want to use Saturation, or adjust specifically the mids. Instead of creating an additional colour correct, you can copy over gamma and gain to a colour correct, and keep working.

**Please note this will not work with Black point and White point, only Gamma, Gain and Lift**

## openReadPath

This will open up a file browser at the file path for any read nodes you have selected
