picPySort

Goal of this tool is to sort/organize photos on the disk in folders named after date and place (if EXIF of a file contains such information) where the photo was taken.

Example: 
For the picture taken in May 2009, in Berlin in the vicinity of Tiergarten. 
PICTURES_DESTINATION\2009\05 - Tiergarten, Berlin, Germany\LGE Nexus 5\myPhoto.jpg
2009
	05 - Tiergarten, Berlin, Germany
		LGE Nexus 5
			myPhoto.jpg

If EXIF will contain Make and Model of your camera, there will be additional level (folder). 
Why add this (make and model)?
Because I can and I thought that it would be useful to know who took the picture your girl or the cat (given that they heave different cameras).

What you need to run it?
Of course python installed, development was started on Python 3.6 and with some additional libraries. 
Their names, at the end of the commands how to add them from command line:
pip install exifread
pip install requests
pip install geopy

How to use it (This is not about how to run a python script)?
At the beginning of the script there few variables which you should edit.
PICTURES_SOURCE = "c:\\src\\"									- this should point to where your photos are
PICTURES_DESTINATION = "c:\\dst\\"								- this is where they end up sorted
HOME = (51.406998372, 116.223499106)							- this latitude and longitude of your home. Why? I don't wont to see my address next to most of the photos
HOME_AREA = 35													- for pictures taken in radius of 35 km from HOME, tags won't be added
OTHER_AREA = 15													- OTHER_AREA? There is a limit for the geocode translate requests, script won't ask for geocode if it is in within 15 km from known location
REMOVE_FROM_ADDRESS = [", Poland", "Gmina", "/", "\\", "-"]		- Stuff you won't to leave out from the address, kind of similar to HOME, I  know that majority of my photos were taken in Poland
REMOVE_FROM_MODEL = ["/", "<", ">"]								- Stuff you must leave out as Model of your phone will be the name of the folder 
 