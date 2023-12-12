import json
import maya.cmds as cmds #import maya commands

#opens window that prompts user to select a file
def selectFilePath(*args):
    
    #pops up dialog that allows user to select a place to load documents
    filePath = cmds.fileDialog2(fm=0, dir="C:\\Users\\Eric\\Desktop\	est.txt", cap="Select File To Load:", ff="*.txt")
    cmds.textField("dataTF", edit=True, text=filePath[0]);
    
#apply data
def Apply(*args):
    
    #take in filePath selected from textField
    filePath = cmds.textField("dataTF", q=True, tx=True)
    rootNode = cmds.textField("rootTF", q=True, tx=True)
    
    #need both filePath and rootNode for it to work
    if filePath == "-":
        print "No filePath Specified"
    elif rootNode == "-":
        print "No root node selected"
    else:
        f=open(filePath, 'r')
        j_data= json.loads(f.readline())
        f.close()
        
        #list of keys(objects)
        objectList = j_data.keys()
        for object in objectList:
            print object
            keyframes = j_data[str(object)]
            keyframesList = j_data[str(object)].keys()
            
            for key in keyframesList:
                attributes = keyframes[str(key)] #attributes of specific key
                attributesList = keyframes[str(key)].keys()
                
                cmds.currentTime(key)
                cmds.select(object)
                for attr in attributesList:
                    #skip if locked                    
                    if cmds.getAttr(object+'.'+attr,lock=True) == True:
                        continue
                    else:
                        print attributes[attr]
                        cmds.setAttr(object+'.'+attr, float(attributes[attr]), clamp=True)
                        cmds.setKeyframe(v=float(attributes[attr]), at=attr)

#PURPOSE: To transfer animation data from one rigged mesh to
#another mesh of the same rig. Specifically to speed up iteration
#of animations on different characters using the same rig by creating
#seperate .mb files within Unity so that each animation can be edited 
#independently using the @ naming convention method of animating.

#WRITTEN BY ERIC MUSSER - ERKMUSS.SQUARESPACE.COM - ENJOY :D

#NOTES BEFORE USING
#Scenes must have same naming convention - it looks for names between rigs.
#Scenes must have same standard unit (grid size) otherwise units won't convert

import json
import maya.cmds as cmds #import maya commands

#opens window that prompts user to select a xml file
def selectFilePath(*args):
    
    #pops up dialog that allows user to select a place to load documents
    filePath = cmds.fileDialog2(fm=0, dir="C:\\Users\\Eric\\Desktop\	est.txt", cap="Select File To Load:", ff="*.txt")
    cmds.textField("dataTF", edit=True, text=filePath[0]);
    
#apply data
def Apply(*args):
    
    #take in filePath selected from textField
    filePath = cmds.textField("dataTF", q=True, tx=True)
    rootNode = cmds.textField("rootTF", q=True, tx=True)
    
    #need both filePath and rootNode for it to work
    if filePath == "-":
        print "No filePath Specified"
    elif rootNode == "-":
        print "No root node selected"
    else:
        f=open(filePath, 'r')
        j_data= json.loads(f.readline())
        f.close()
        
        #list of keys(objects)
        objectList = j_data.keys()
        for object in objectList:
            print object
            keyframes = j_data[str(object)]
            keyframesList = j_data[str(object)].keys()
            
            for key in keyframesList:
                attributes = keyframes[str(key)] #attributes of specific key
                attributesList = keyframes[str(key)].keys()
                
                cmds.currentTime(key)
                cmds.select(object)
                for attr in attributesList:
                    #skip if locked                    
                    if cmds.getAttr(object+'.'+attr,lock=True) == True:
                        continue
                    else:
                        print attributes[attr]
                        cmds.setAttr(object+'.'+attr, float(attributes[attr]), clamp=True)
                        cmds.setKeyframe(v=float(attributes[attr]), at=attr)

def setRoot(*args):
    
    #select heirarchy of root
    selection = cmds.ls(sl= True)
    if selection == []:
        print "Nothing Selected"
    else:
        #change textField text to root name
        cmds.textField("rootTF", edit=True, text=selection[0]);
            
       
def exportData(*args):
    #takes value from text field to use in creating xml file
    root = cmds.textField("rootTF", q=True, tx=True)
        
    #make root readable and check for no selection    
    if root == '-':
        print "Nothing selected for root node."
    else:
        #select hiearchy of root, then add those selections to a variable
        cmds.select(root, hi=True)
        selection = cmds.ls(sl=True);
        
        #empty dictionary for storing objects
        objectDict = {}
        
        #go through each object in selected heirarchy
        for object in selection:
            cmds.select(object)
            #get first and last frame of current object in heirarchy
            firstKey = cmds.findKeyframe(time=(0, 1000), which='first') 
            lastKey = cmds.findKeyframe(time=(0, 1000), which='last')
            
            
            #to deal with objects that aren't keyed
            if int(firstKey) == int(lastKey):
                continue
            else:
                #create empty dict for storing keyframes
                keyframeDict = {}
                
                #go through each frame of animation
                for frame in range(int(firstKey),int(lastKey)):
                    
                    #make sure on the right frame
                    cmds.currentTime(frame)
                    
                    #create empty dict for storing attributes
                    attributeDict = {}
                    
                    #get the translation
                    object_translation = cmds.getAttr(object + ".translate")
                    attributeDict["translateX"] = str(object_translation[0][0])
                    attributeDict["translateY"] = str(object_translation[0][1])
                    attributeDict["translateZ"] = str(object_translation[0][2])
                    
                    #get the rotation
                    object_rotation = cmds.getAttr(object + ".rotate")
                    attributeDict["rotateX"] = str(object_rotation[0][0])
                    attributeDict["rotateY"] = str(object_rotation[0][1])
                    attributeDict["rotateZ"] = str(object_rotation[0][2])
                    
                    #add attribute data to keyframeDict
                    keyframeDict[str(frame)] = attributeDict
                        
                #add keyframe data to object    
                objectDict[str(object)] = keyframeDict

        #prompt user for a location to save their file
        filePath = cmds.fileDialog2(fm=0, dir="C:\\Users\\Eric\\Desktop\	est.txt", cap="Select Location To Save File:", ff="*.txt")
        f=open(filePath[0], 'w')
        f.write(json.dumps(objectDict,skipkeys = True))
        f.close()
        
        print "Sent to " + filePath[0]    

#delete window if it exists
if cmds.window("passData", q=True, exists=True):
    cmds.deleteUI("passData", wnd=True);
    
#create user interface
cmds.window("passData", t="Pass Animation Data", rtf=True, s=False);
cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 100), (2, 200), (3, 100)]);

#first row
cmds.text("Root_Node");
cmds.textField("rootTF", text="-", ed=False);
cmds.button("Set Root", c=setRoot);

#second row
cmds.text("Data_File");
cmds.textField("dataTF", text="-", ed=False);
cmds.button("Select File Path", c=selectFilePath);

#third row
cmds.text("");
cmds.button("Export Current Data...", c=exportData);
cmds.button("Apply Data", c=Apply);

cmds.showWindow("passData");