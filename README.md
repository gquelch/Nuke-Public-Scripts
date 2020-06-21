My Python Scripts for Nuke

Jump to Documentation:

[GQ_Tools](https://github.com/gquelch/Nuke-Public-Scripts#gq_tools)

[Shot Comparison](https://github.com/gquelch/Nuke-Public-Scripts/blob/master/README.md#shot-comparison)

[Reload All Reads](https://github.com/gquelch/Nuke-Public-Scripts#reloadallreads)

[Grade Convert](https://github.com/gquelch/Nuke-Public-Scripts#gradeconvert)

[Open Read Path](https://github.com/gquelch/Nuke-Public-Scripts#openreadpath)

[Get ABC](https://github.com/gquelch/Nuke-Public-Scripts#getabc)

I recommend reading my guide on [importing scripts and panels](https://gquelch.github.io/2020/06/21/Simplify-Executing-and-Sharing-Nuke-Scripts/) in order to simplify the process of adding and executing these scripts inside of Nuke, especially for the GQ_Tools and Shot Comparison Panels.

## GQ_Tools

This is my *Master* Tool, it has a few built in functions, one of the main things it can do is load and execute other python scripts, this allows  you to easily change and update scripts in a folder, without restarting nuke or adding them to a pipeline. It also allows you to get around the need to copy and paste scripts into the script editor, or loading them into a specific Nuke menu.

You are able to set a default location of your script library (line 9), it's not necessary, but means you don't have to paste it in every time. I set this to wherever I am currently saving my scripts, you might want to change this per project, or to a global scripts directory on a network drive.

   
### Selection Tools

The top set of tools have some quick actions that let you select nodes by class, you just write each class you want to select, separated by spaces

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

---
   
## Shot Comparison
I built this tool to assist with shot consistency, it allows users to save images of Movs as a path in different groups, say 5 shots from the same angle, which you want to compare.

You can save as many shots as you like, in as many groups as you would like, you can then create a contact sheet from these easily for comparison.

---
   
## ReloadAllReads

This script will simply reload all Read nodes in your Nuke file

---
   
   
   
## gradeConvert

Sometimes I find myself working on a grade node, and deciding I want to use Saturation, or adjust specifically the mids. Instead of creating an additional colour correct, you can copy over gamma and gain to a colour correct, and keep working.

**Please note this will not work with Black point and White point, only Gamma, Gain and Lift**

---
   
   
   
## openReadPath

This will open up a file browser at the file path for any read nodes you have selected

---
   
   
   
## getABC

This tool is  for listing available ABC (alembic) files in a directory, **it wont work right out of the box** and that is because everyone and every company stores their publish files differently.

in order for this to work there are two functions you'll need to tweak

Once you have done the tweaks and can run the script, you should be presented with a list of alembics, here you can tick which ones you want to import, if you have a camera node selected, and you tick to import a camera, you will be given an option to replace the camera you have selected with your new one, useful for updating camera alembics in new shots!

**GQ_getABCPath()**

This is where you will give the script your ABC path, in the past I have been able to use the file path of the shot I am working on, to create the ABC path

for instance, this may be our file path:

*F:/Projects/Foo/ep_01/sh_010/comp/ep_01_sh010.nk*

and our alembics could be stored here:

*P:/Publish/Foo/ep_01/sh_010/anim/*

We can split the first path by "/" and swap the appropriate parts of the string, in this case: the Project/Publish folder name and the comp/anim folder name

Then we would just need to re-join that list into a string, and we would have created our ABC path

This would let us dynamically build the path for any shot we open, just from the path of the comp file - no integration with any tracking software necessary

that script would look like this:

```python
def GQ_getABCPath():
	#file path
	path = nuke.root().knob('name').value()
	
	pathSplit = path.split("/")
	
	#Project/Publish swap
	pathSplit[1] = "Publish"
	#Comp/Anim swap
	pathSplit[5] = "anim"
	
	abcPath = "/".join(pathSplit[:-1]) #[:-1] will remove the nuke file name from the path
	
	return abcPath
```

There are many different options here, including making use of tracking software intergration such as fTrack or Shotgun, or potentially ENV variables, it really depends on how you or your studio operates

**GQ_ABCTypeCheck(ABCDict)**

The other thing you will have to do which is studio specific is sort through the returned ABC files to separate our Geo caches from Camera caches

This is important because both require a different node to be created in Nuke, again, this is down to how your own studio deals with file naming

If your cache files contained CAM and GEO in the file name, then it would be as simple as  this:

```python
def GQ_ABCTypeCheck(ABCDict):
	## Split ABC Types ##

	geoList = []
	camList = []

	for key in ABCDict:
		if ABCDict[key] == True:

			if "CAM" in key:
				camList.append(key)

			if "GEO" in key:
				geoList.append(key)


	return camList, geoList
```

You'll want to keep the return strings the same for both of these scripts, this ensures that the rest of the script will function properly without you having to mess around with it too much
