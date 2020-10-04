My Python Scripts for Nuke

Jump to Documentation:

[Reload All Reads](https://github.com/gquelch/Nuke-Public-Scripts#reloadallreads)

[Grade Convert](https://github.com/gquelch/Nuke-Public-Scripts#gradeconvert)

[Branch Mask](https://github.com/gquelch/Nuke-Public-Scripts#branchMask)

[Open Read Path](https://github.com/gquelch/Nuke-Public-Scripts#openreadpath)

[Get ABC](https://github.com/gquelch/Nuke-Public-Scripts#getabc)

<br></br>


## ReloadAllReads

This script will simply reload all Read nodes in your Nuke file

<br></br>
   
   
   
## gradeConvert

Sometimes I find myself working on a grade node, and deciding I want to use Saturation, or adjust specifically the mids. Instead of creating an additional colour correct, you can copy over gamma and gain to a colour correct, and keep working.

**Please note this will not work with Black point and White point, only Gamma, Gain and Lift**

<br></br>
   
   
## branchMask

A robust alternative to the default nuke branch function that works correctly when branching several nodes with different mask inputs and connections. 

<br></br>

## openReadPath

This will open up a file browser at the file path for any read nodes you have selected

<br></br>
   
## getABC

This tool is  for listing available ABC (alembic) files in a directory, **it wont work right out of the box** and that is because everyone and every company stores their publish files differently.

in order for this to work there are two functions you'll need to tweak

Once you have done the tweaks and can run the script, you should be presented with a list of alembics, here you can tick which ones you want to import, if you have a camera node selected, and you tick to import a camera, you will be given an option to replace the camera you have selected with your new one, useful for updating camera alembics in new shots!

<br></br>

**GQ_getABCPath()**

This is where you will give the script your ABC path, in the past I have been able to use the file path of the shot I am working on, to create the ABC path

for instance, this may be our file path:

*F:/Projects/Foo/ep_01/sh_010/comp/ep_01_sh010.nk*

and our alembics could be stored here:

*P:/Publish/Foo/ep_01/sh_010/anim/*


We can split the first path by "/" and swap the appropriate parts of the string, in this case: the Project/Publish folder name and the comp/anim folder name

Then we would just need to re-join that list into a string, and we would have created our ABC path

<br></br>

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

<br></br>

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
