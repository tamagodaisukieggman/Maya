##--------------------------------------------------------------------------
##
## ScriptName : renameWizard
## Contents   : rename item form libaray list
## Author     : Joe Wu
## URL        : http://im3djoe.com
## Since      : 2023/07
## Version    : 1.3  First version for public test
##				
## Install    : copy and paste script into a python tab in maya script editor
## Other Note : test in maya 2023 windows / 2020 Linux enviroment
## Bug Report : please email me n2197472@hotmail.com
##
##
## the script is for personal or/and commercial work whether you are a freelance artist or working in the studio.
## please don't distribute/share, change the script or reuse the script code to make your own script.
##--------------------------------------------------------------------------


import maya.cmds as mc
#import pymel.core as pm
import maya.mel as mel
import os
import re
import random


def checkFilterSel():
    targetName = mc.textScrollList('renameListTable',q=1,si=1)
    filterFieldName = mc.textField('filterText',q=1, tx =1)
    if filterFieldName:
        cleanRWFilter()
        mc.textScrollList('renameListTable',e=1, si=targetName)
                
                                
def removeNameNumber():
    allTransNode = mc.ls(sl=1,fl=1,transforms=1)
    selListGeo = []
    selListGrp = []
    for c in allTransNode:
        getType = isGroup(c)
        if getType != 1:
            selListGeo.append(c)
        else:
            selListGrp.append(c)
    doList = [selListGeo,selListGrp]
    for d in doList:
        for s in d:
            if '_geo' in s or '_grp' in s:
                checkItem = s.split('_')
                newList = []
                for k in checkItem:
                    if k == '':
                        newList.append('')
                    else:
                        checkType = k.isdigit()
                        if checkType == 0:
                            newList.append(k)
                finalName = '_'.join(newList)
                if finalName != s :
                    mc.rename(s, finalName)

def removeNameMTag():
    allTransNode = mc.ls(sl=1,fl=1,transforms=1)
    selListGeo = []
    for c in allTransNode:
        getType = isGroup(c)
        if getType != 1:
            selListGeo.append(c)
    
    for s in selListGeo:
        geoNameKeep=''
        if '__' in s:
            geoNameKeep = s.split('__')[0]
            newName = geoNameKeep + '_geo'
            newName = newName.split('|')[-1]
            mc.rename(s,newName)

def removeMixCharacterAndNumber():
    allTransNode = mc.ls(dag=1,fl=1,transforms=1)
    selListGeo = []
    for c in allTransNode:
        getType = isGroup(c)
        if getType == 0:
            selListGeo.append(c)
    for s in selListGeo:
        if '_geo' in s or '_grp' in s:
            checkItem = s.split('_')
            newList = []
            for k in checkItem:
                if k == '':
                    newList.append('')
                else:
                    checkType = k[0].isdigit()
            
                    if checkType == 0:
                        newItem = re.sub(r'\d+', '', k)
                        newList.append(newItem)
                    else:
                        newList.append(k)
            finalName = '_'.join(newList)
            if finalName != s :
                mc.rename(s, finalName)


def createNewLibUI():
    if mc.window("renameWizardCreateNewListUI", exists = True):
        mc.deleteUI("renameWizardCreateNewListUI")
    renameWizardCreateNewListUI = mc.window('renameWizardCreateNewListUI',title='Create New Library', width=(300))
    mainLayout = mc.columnLayout(adjustableColumn=True)
    
    mc.text(l ='',h=10)
    mc.rowColumnLayout(nc= 3 ,cw=[(1,100),(2,5),(3,150)])
    folderText = mc.text(label='Folder Name:')
    mc.text(l ='',h=10)
    folderField = mc.textField('newFolderName')
    
    mc.text(l ='',h=5)
    mc.setParent( '..' )
    mc.rowColumnLayout(nc= 3 ,cw=[(1,100),(2,5),(3,150)])
    subText = mc.text(label='List Name:')
    mc.text(l ='',h=10)
    subField = mc.textField('newListName')
    
    
    mc.setParent( '..' )
    mc.text(l ='',h=5)
    mc.rowColumnLayout(nc= 2 ,cw=[(1,190),(2,60)])
    mc.text(l ='',h=5)
    createButton = mc.button(label='Create',c='createNewLibGo()')
    
    mc.setParent(mainLayout)
    mc.showWindow(renameWizardCreateNewListUI)


def createNewLibGo():
    path = mc.textField('reNameLibPath', q=1, tx =1)
    modeState = mc.radioButtonGrp('dictMode',q=1,sl=1)
    mode = ''
    if modeState == 1:
        mode = 'Asset'
    else:
        mode = 'Material'
    folderName = mc.textField('newFolderName',q=1,tx=1)
    subName =  mc.textField('newListName',q=1,tx=1)
    path = path + '/' + mode
    # Create the main folder if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)
    # Create the subfolder if it doesn't exist
    subFolderPath = os.path.join(path, folderName)
    if not os.path.exists(subFolderPath):
        os.makedirs(subFolderPath)
    # Create the file if it doesn't exist
    filePath = os.path.join(subFolderPath, subName + '.list')
    if not os.path.exists(filePath):
        open(filePath, 'w').close()
    mc.deleteUI("renameWizardCreateNewListUI")
    updateCato()
    mc.optionMenu('categoryFolder', e =1 , v = folderName)
    updateSubList()
    mc.optionMenu('listSubName',  e =1 , v = subName)
    mc.textScrollList('renameListTable', e=1, ra=1)


def cleanRWFilter():
    filterName = mc.textField('filterText',e=1, tx ='')
    
def highLigtRList():
    highLightList = mc.ls(sl=1,fl=1)
    removeList = ['L', 'B', 'M','R','F','geoShape','geo','grp']
    textSList = mc.textScrollList('renameListTable', q=1,ai=1)
    mc.textScrollList('renameListTable',e=1, da=1)
    for h in highLightList:
        guessName = h.split('_')
        guessName = [item for item in guessName if not item.isdigit()]
        cleanList = list(set(guessName) - set(removeList))
        array = [item for item in cleanList if item]
        for t in textSList:
            for a in array:
                if a in t:
                    mc.textScrollList('renameListTable',e=1, si=a)

def fixShapeName():
    shapeList = mc.ls(dag=1,shapes=1)
    removelist = ['perspShape' ,'topShape', 'frontShape', 'sideShape']
    cleanList = list(set(shapeList) - set(removelist))
    for c in cleanList:
        parentNode = mc.listRelatives(c,f=1, p=1)[0].split('|')[-1]
        mc.rename(c,(parentNode+'Shape'))

def shader2Name():
    shaderList = mc.ls('*_SHDSG',fl=1)
    for s in shaderList:
        shape_node = mc.sets(s, q=1)
        if shape_node:
            transform_node = mc.listRelatives(shape_node, parent=True)
            meshList = list(set(transform_node))
            shaderName = s.replace('_SHDSG','')
            for m in meshList:
                geoNameKeep=''
                if '__' in m:
                    geoNameKeep = m.split('__')[0]
                else:    
                    geoNameKeep = m.split('_geo')[0]
                newName = geoNameKeep + '__' + shaderName + '_geo'
                newName = newName.split('|')[-1]
                mc.rename(m,newName)
            


    
    
def perfectSceneNumber():
    #avoid error when Duplicate Name exist
    checkDState = findDuplicateNames()
    if checkDState == 0:
        allTransNode = mc.ls(dag=1,fl=1,transforms=1)
        selListGeo = []
        selListGrp = []
        for c in allTransNode:
            getType = isGroup(c)
            if getType == 1:
                selListGrp.append(c)
            else:
                selListGeo.append(c)
        
        toDoList = [selListGeo,selListGrp]
        x = 0
        for t in toDoList:
            nameList = []
            for name in t:
                match_obj = re.search(r'\d+', name)
                if match_obj:
                    number_index = match_obj.start()
                    nameList.append(name[:number_index])
            unique_list = list(set(nameList))
            unique_list = sorted(unique_list)
            for u in unique_list:
                mList = mc.ls(u + '*', fl=1,transforms=1)
                onlyList = []
                for m in mList:
                    getType = isGroup(m)
                    if x == 0:
                        if getType == 0:
                            onlyList.append(m)
                    else:
                         if getType == 1:
                            onlyList.append(m)
                i = 1
                for m in onlyList:
                    number = re.findall('\d+', m)
                    if number:
                        checkNumber = int(number[0])
                        if i != checkNumber:
                            correctNumber = '{:03d}'.format(i)
                            correctName = re.sub(r"\d+", correctNumber, m)
                            mc.rename(m,correctName)
                        i=i+1
            x=x+1

def removeOneUnderScore(dir):
    selList = mc.ls(sl=1,fl=1)
    for s in selList:
        newString = ''
        if '_' in s:
            if dir == 0:
                underscore_index = s.index('_') + 1
                newString = s[underscore_index:]
            else:
                underscore_index = s.rindex('_')
                newString = s[:underscore_index]
            mc.rename(s,newString)

def removeOneLetter(dir):
    selList = mc.ls(sl=1,fl=1)
    for s in selList:
        newString=''
        if dir == 0:
            newString = s[1:]
        else:
            newString = s[:-1]
        mc.rename(s,newString)




def autoSetFB():
    jointSelected = mc.ls(sl=1,fl=1,l=1)
    selListGeo = []
    selListGrp = []
    selListLoc = []
    #seperate geo and group
    for c in jointSelected:
        getType = isGroup(c)
        if getType == 1:
            selListGrp.append(c)
        elif getType == 2:
            selListLoc.append(c)
        else:
            selListGeo.append(c)
    
    if selListGrp:
        splitDict = []
        for item in selListGrp:
            splitItem = item.split('|')
            numSplits = len(splitItem) - 1
            splitDict.append([item, numSplits])
        
        splitDict.sort(key=lambda x: x[1], reverse=True)
        newArray = [item for item, _ in splitDict]
        selListGrp = newArray
    
    doList = [selListGeo, selListLoc, selListGrp]
    for d in doList:
        for s in d:
            collectAxisXData = []
            bbox = mc.xform(s, query=True, boundingBox=True,ws=1)
            collectAxisXData.append(bbox[2])
            collectAxisXData.append(bbox[5])
            foundPos = ''
            if all(z < 0 for z in collectAxisXData):
                foundPos =  'B'
            elif all(z > 0 for z in collectAxisXData):
                foundPos =  'F'
                    
            pathNodes = s.split('|')
            myObj = pathNodes[-1]
            removeSide = myObj.split('_')
                           
            removeList = ['B','F'] 
            for item in removeList:
                if item in removeSide:
                    removeSide.remove(item)
            if foundPos != '':
                removeSide.insert(0, foundPos)
                result = '_'.join(removeSide)
            else:
                result = '_'.join(removeSide)
            if myObj != result:
                mc.rename(s,result)


def autoSetLR():
    jointSelected = mc.ls(sl=1,fl=1,l=1)
    selListGeo = []
    selListGrp = []
    selListLoc = []
    #seperate geo and group
    for c in jointSelected:
        getType = isGroup(c)
        if getType == 1:
            selListGrp.append(c)
        elif getType == 2:
            selListLoc.append(c)
        else:
            selListGeo.append(c)
    
    if selListGrp:
        splitDict = []
        for item in selListGrp:
            splitItem = item.split('|')
            numSplits = len(splitItem) - 1
            splitDict.append([item, numSplits])
        
        splitDict.sort(key=lambda x: x[1], reverse=True)
        newArray = [item for item, _ in splitDict]
        selListGrp = newArray
    
    doList = [selListGeo, selListLoc, selListGrp]
    for d in doList:
        for s in d:
            collectAxisXData = []
            bbox = mc.xform(s, query=True, boundingBox=True,ws=1)
            collectAxisXData.append(bbox[0])
            collectAxisXData.append(bbox[3])
            foundSide = ''
            if all(x < 0 for x in collectAxisXData):
                foundSide =  'L'
            elif all(x > 0 for x in collectAxisXData):
                foundSide =  'R'
                    
            pathNodes = s.split('|')
            myObj = pathNodes[-1]
            removeSide = myObj.split('_')
                           
            removeList = ['L','R'] 
            for item in removeList:
                if item in removeSide:
                    removeSide.remove(item)
            if foundSide != '':
                if removeSide[0]== 'B' or removeSide[0]== 'F':
                    removeSide.insert(1, foundSide)
                else:
                    removeSide.insert(0, foundSide)
                result = '_'.join(removeSide)
            else:
                result = '_'.join(removeSide)
            if myObj != result:
                mc.rename(s,result)
   
    

def quickFixEnd():
    jointSelected = mc.ls(sl=1,fl=1,l=1)
    selListGeo = []
    selListGrp = []
    selListLoc = []
    #seperate geo and group
    for c in jointSelected:
        getType = isGroup(c)
        if getType == 1:
            selListGrp.append(c)
        elif getType == 2:
            selListLoc.append(c)
        else:
            selListGeo.append(c)
    #fix geo, loc first avoid error after group rename

    removeList = ['geo','loc','grp'] 
    for s in selListGeo:
        pathNodes = s.split('|')
        myObj = pathNodes[-1]
        removeEnd = myObj.split('_')
        for item in removeList:
            if item in removeEnd:
                removeEnd.remove(item)
        result = '_'.join(removeEnd)  
        if '_geo' not in result:
            #print(result + '_geo')
            mc.rename(s, result + '_geo')
    
    for s in selListLoc:
        pathNodes = s.split('|')
        myObj = pathNodes[-1]
        removeEnd = myObj.split('_')
        for item in removeList:
            if item in removeEnd:
                removeEnd.remove(item)
        result = '_'.join(removeEnd)  
        if '_loc' not in result:
            mc.rename(s, result + '_loc')
    
    # reorder list, start rename the deepest children avoid error
    splitDict = []
    for item in selListGrp:
        splitItem = item.split('|')
        numSplits = len(splitItem) - 1
        splitDict.append([item, numSplits])
    
    splitDict.sort(key=lambda x: x[1], reverse=True)
    newArray = [item for item, _ in splitDict]
    
    for s in newArray:
        pathNodes = s.split('|')
        myObj = pathNodes[-1]
        removeEnd = myObj.split('_')
        for item in removeList:
            if item in removeEnd:
                removeEnd.remove(item)
        result = '_'.join(removeEnd)
        if '_grp' not in result:
            mc.rename(s, result + '_grp')
    #final debug and name mix character and number in geo, eg apple3_new1 --> apple_new 
    removeMixCharacterAndNumber()
    
def quickPrefix(dir,fixName):
    if mc.objExists('tempListGEOStore'):
        mc.delete('tempListGEOStor*')
    if mc.objExists('tempListGRPStore'):
        mc.delete('tempListGRPStor*')
    mc.createDisplayLayer(empty=True, name='tempListGEOStore')
    mc.createDisplayLayer(empty=True, name='tempListGRPStore')   
    jointSelected = mc.ls(sl=1,fl=1,l=1)
    selListGeo = []
    selListGrp = []
    #seperate geo and group
    for c in jointSelected:
        getType = isGroup(c)
        if getType == 1:
            selListGrp.append(c)
        else:
            selListGeo.append(c)
    #fix geo first avoid error after group rename
    
    if selListGeo:
        for e in selListGeo:
            mc.connectAttr('tempListGEOStore.drawInfo', e+'.drawOverride',f=1)
        for s in selListGeo:
            pathNodes = s.split('|')
            myObj = pathNodes[-1]
            removeSide = myObj.split('_')
            if dir == 0:
                removeList = []
                if fixName == 'R' or  fixName == 'L':
                    removeList = ['R','L','M'] 
                elif fixName == 'F' or  fixName == 'B':
                    removeList = ['F','B','M'] 
                elif fixName == 'M':
                    removeList = ['R','L','F','B','M'] 
                for item in removeList:
                    if item in removeSide:
                        removeSide.remove(item)
                if removeSide[0]== 'L' or removeSide[0]== 'R':
                    removeSide.insert(1, fixName)
                else:
                    removeSide.insert(0, fixName)
                result = '_'.join(removeSide)
                mc.rename(s, result)

    if selListGrp:    
        for t in selListGrp:
            mc.connectAttr('tempListGRPStore.drawInfo', t+'.drawOverride',f=1)  
        CMD = 'layerEditorSelectObjects tempListGRPStore;'
        mel.eval(CMD)
        fixGrpName = mc.ls(sl=1,fl=1,l=1)
        while len(fixGrpName)>0:
            #for j in jointSelected:
            pathNodes = fixGrpName[0].split('|')
            numTokens = len(pathNodes)
            myObj = pathNodes[numTokens - 1]
            removeSide = myObj.split('_')
            if dir == 0:
                removeList = []
                if fixName == 'R' or  fixName == 'L':
                    removeList = ['R','L','M'] 
                elif fixName == 'F' or  fixName == 'B':
                    removeList = ['F','B','M']
                elif fixName == 'M':
                    removeList = ['R','L','F','B','M']   
                for item in removeList:
                    if item in removeSide:
                        removeSide.remove(item)
                if removeSide[0]== 'L' or removeSide[0]== 'R':
                    removeSide.insert(1, fixName)
                else:
                    removeSide.insert(0, fixName)
                result = '_'.join(removeSide)
                mc.rename(fixGrpName[0], result)
                mc.select(result,d=1)
            fixGrpName = mc.ls(sl=1,fl=1,l=1)
    CMD = 'layerEditorSelectObjects tempListGRPStore;'
    mel.eval(CMD)
    newGrpList = mc.ls(sl=1,fl=1)
    CMD = 'layerEditorSelectObjects tempListGEOStore;'
    mel.eval(CMD)
    mc.select(newGrpList,add=1)
    mc.delete('tempListGEOStor*')
    mc.delete('tempListGRPStor*')

def carryName():
    currentSel = mc.ls(sl=1,fl=1,l=1)
    for c in currentSel:
        selType = isGroup(c)
        if selType == 0:
            parentNode = cmds.listRelatives(c, p=True) or []
            getType = isGroup(parentNode)
            if getType == 1:
                nodeName = parentNode[0].replace('_grp','')
                i = 1
                new_num = str(i).zfill(3)
                checkName = nodeName + '_' + new_num +'_geo'
                checkExist = mc.objExists(checkName)
                while checkExist == 1:
                    i = i+1
                    new_num = str(i).zfill(3)
                    checkName = nodeName + '_' + new_num +'_geo'
                    checkExist = mc.objExists(checkName)
                mc.rename(c,checkName)

    

def renameMagic():
    targetName = mc.textScrollList('renameListTable',q=1,si=1)
    autoSide = mc.checkBox('AutoCheckSide', q=1, v=1 )
    autoPos = mc.checkBox('AutoCheckPosition', q=1, v=1 )
    autoHide = mc.checkBox('autoHideBox', q=1, v=1 )
    modeState = mc.radioButtonGrp('dictMode',q=1, sl=1)
    kMTState = mc.checkBox('keepMTag',q=1, v=1 )
    if targetName: 
        if len(targetName) == 1:
            currentSel = mc.ls(sl=1,fl=1,l=1)
            if mc.objExists('temListStore'):
                mc.delete('temListStore')
            layer = mc.createDisplayLayer(empty=True, name='temListStore')
            #bug, this will add all children to display layer
            #mc.editDisplayLayerMembers('temListStore', currentSel)
            for e in currentSel:
                mc.connectAttr('temListStore.drawInfo', e+'.drawOverride',f=1)
            matchListGeo= []
            matchListGrp= []
            selListGeo = []
            selListGrp = []
            #seperate geo and group
            for c in currentSel:
                getType = isGroup(c)
                if getType == 1:
                    selListGrp.append(c)
                else:
                    selListGeo.append(c)
            if modeState == 1:
                allTransNode = mc.ls( dag=1,transforms=1,l=1)
                delimiter_pattern = re.compile(r'[_|]')
                for a in allTransNode:
                    getType = isGroup(a)
                    if getType == 1:
                        checkName = re.split(delimiter_pattern, a)
                        for k in checkName:
                            if k == targetName[0]:
                                getType = isGroup(a)
                                if getType == 1:
                                    matchListGrp.append(a)
                
                for a in allTransNode:
                    objOnly = a.split('|')[-1]
                    checkName = objOnly.split('_')
                    for k in checkName:
                        if k == targetName[0]:
                            matchListGeo.append(a)
                     
                #reneme GEO
                shortNameGeoList = mc.ls(matchListGeo,fl=1)
                numberList = []
                missing_nums = []
                if shortNameGeoList:
                    shortNameGeoList = list(set(shortNameGeoList))
                    for s in shortNameGeoList:
                        number = re.findall('\d+', s)
                        if number:
                            numberList.append(int(number[0]))
                if numberList:
                    missing_nums = [num for num in range(1, max(numberList)+len(selListGeo)+1) if num not in numberList]
                else:
                    missing_nums = range(1, 1001)
    
                for i in range(len(selListGeo)):
                    storeMaterial = ''
                    if '__' in selListGeo[i]:
                        storeMaterial = selListGeo[i].split('__')[-1].replace('_geo','')
                    new_num = str(missing_nums[i]).zfill(3)
                    new_name = targetName[0] + '_' + new_num
                    if autoPos == 1:
                        getPos = autoGetFB(selListGeo[i])
                        if getPos:
                            new_name = getPos + new_name
                    if autoSide == 1:
                        getSide = autoGetLR(selListGeo[i])
                        if getSide:
                            new_name = getSide + new_name
                    if kMTState == 1:
                        if storeMaterial:
                            new_name = new_name + '__' +storeMaterial
                    else:
                        mc.sets(selListGeo[i], e=True, forceElement = 'initialShadingGroup')
                    mc.rename(selListGeo[i],new_name)
                    
                #reneme GROUP
                numberList = []
                missing_nums = []
                for s in matchListGrp:
                    number = re.findall('\d+', s)
                    if number:
                        for n in number:
                            numberList.append(int(n))
                if numberList:
                    missing_nums = [num for num in range(1, max(numberList)+len(selListGrp)+1) if num not in numberList]
                else:
                    missing_nums = range(1, 1001)
    
                mc.select(selListGrp)
                startRenameGrp = mc.ls(sl=1,fl=1,l=1)
                if len(startRenameGrp) == 1:
                    new_name = targetName[0]
                    if autoPos == 1:
                        getPos = autoGetFB(startRenameGrp[0])
                        if getPos:
                            new_name = getPos + new_name
                    if autoSide == 1:
                        getSide = autoGetLR(startRenameGrp[0])
                        if getSide:
                            new_name = getSide + new_name
                    mc.rename(startRenameGrp[0], new_name +'_grp')
                elif len(startRenameGrp) > 1:
                    i=0
                    while len(startRenameGrp)>0:
                        new_num = str(missing_nums[i]).zfill(3)
                        new_name = targetName[0] + '_' + new_num
                        if autoPos == 1:
                            getPos = autoGetFB(startRenameGrp[0])
                            if getPos:
                                new_name = getPos + new_name
                        if autoSide == 1:
                            getSide = autoGetLR(startRenameGrp[0])
                            if getSide:
                                new_name = getSide + new_name
                        if mc.objExists(new_name):
                            i = i + 1
                        else:
                            mc.rename(startRenameGrp[0], new_name)
                            mc.select(new_name,d=1)
                            startRenameGrp = mc.ls(sl=1,fl=1,l=1)
                            i = i + 1
            else:
                if selListGeo:
                    for s in selListGeo:
                        geoNameKeep=''
                        if '__' in s:
                            geoNameKeep = s.split('__')[0]
                        else:    
                            geoNameKeep = s.split('_geo')[0]
                        newName = geoNameKeep + '__' + targetName[0] + '_geo'
                        newName = newName.split('|')[-1]
                        mc.rename(s,newName)
                        targetName = mc.textScrollList('renameListTable',q=1,si=1)
                    if mc.objExists(targetName[0]+'_SHD') == 0:
                        shd = mc.shadingNode('lambert', name=(targetName[0]+'_SHD'), asShader=True)
                        shdSG = mc.sets(name=(targetName[0]+'_SHDSG'), empty=True, renderable=True, noSurfaceShader=True)
                        mc.connectAttr((shd +'.outColor'), (shdSG +'.surfaceShader'))
                        R1 = random.random()
                        R2 = random.random()
                        R3 = random.random()
                        mc.setAttr (targetName[0]+'_SHD.color', R1,R2,R3, type = 'double3' )
                    CMD = 'layerEditorSelectObjects temListStore;'
                    mel.eval(CMD)
                    collectNew = mc.ls(sl=1,fl=1)
                    mc.sets(collectNew, e=True, forceElement = targetName[0]+'_SHDSG')
  
                    
            CMD = 'layerEditorSelectObjects temListStore;'
            mel.eval(CMD)
            quickFixEnd()
            if autoHide == 1:
                mc.HideSelectedObjects()
            
            mc.delete('temListStore')

def autoGetFB(sel):
    checkGrp = isGroup(sel)
    children = []
    if checkGrp == 1:
        children = cmds.listRelatives(sel, children=True) or []
    else:
        children.append(sel)
    collectAxisXData = []
    for c in children:
        bbox = mc.xform(c, query=True, boundingBox=True,ws=1)
        collectAxisXData.append(bbox[2])
        collectAxisXData.append(bbox[5])
    foundPos = ''
    if all(z < 0 for z in collectAxisXData):
        foundPos =  'B_'
    elif all(z > 0 for z in collectAxisXData):
        foundPos =  'F_'
    return foundPos     

def autoGetLR(sel):
    checkGrp = isGroup(sel)
    children = []
    if checkGrp == 1:
        children = cmds.listRelatives(sel, children=True) or []
    else:
        children.append(sel)
    collectAxisXData = []
    for c in children:
        bbox = mc.xform(c, query=True, boundingBox=True,ws=1)
        collectAxisXData.append(bbox[0])
        collectAxisXData.append(bbox[3])
    foundSide = ''
    if all(x < 0 for x in collectAxisXData):
        foundSide =  'L_'
    elif all(x > 0 for x in collectAxisXData):
        foundSide =  'R_'
    return foundSide        

def isGroup(node):# 1 = group, 0 =  geo , 2=locator
    result = 0
    if mc.objectType(node, isType = 'joint'):
        result = 0
    kids = mc.listRelatives(node, c=1,f=1)
    if kids:
        for kid in kids:
            if not mc.objectType(kid, isType = 'transform'):
                checkType = mc.nodeType(kid)
                if checkType == 'locator':
                    result = 2
                else:
                    result = 0
            else:
                result = 1    
    else:
        result = 1
    return result


def colourDuplicate():                               
    meshes = mc.ls(dag=1,transforms =1,shortNames=True)
    nameOnly = []
    for m in meshes:
        removeP = m.split('|')[-1]
        removeMtag = removeP.split('__')[0]
        removeGrp = removeMtag.replace('_grp','')
        removeGeo = removeGrp.replace('_geo','')
        checkName = removeGeo.replace('|','')
        nameOnly.append(checkName)
    
    seen = set()
    duplicates = []
    for item in nameOnly:
        if item in seen and item not in duplicates:
            duplicates.append(item)
        else:
            seen.add(item)
    
    getFullList = []
    
    for d in duplicates:
        check = mc.ls((d+'*'),fl=1,l=1)
        rR = random.random() 
        rG = random.random()  
        rB = random.random()  
        for c in check:
            mc.setAttr(c + ".useOutlinerColor", 1)
            mc.setAttr(c + ".outlinerColor", rR, rG, rB)
        getFullList = getFullList + check
    if len(duplicates):
        mc.button('checkDulButton', e=1,bgc=(0.5,0.2,0.2)) 
        mc.select(getFullList)
    else:
        mc.button('checkDulButton', e=1,bgc=(0.2,0.5,0.2))   
        mc.select(cl=1)
        for m in meshes:
            mc.setAttr(m + ".useOutlinerColor", 0)
    outliner_panels = mc.getPanel(type="outlinerPanel")
    for outliner_panel in outliner_panels:
        mc.outlinerEditor(outliner_panel, edit=True, refresh=True)

def findDuplicateNames():
    objs = [ x for x in mc.ls(shortNames=True) if '|' in x ]
    if len(objs):
        objs.sort(key=lambda x: x.count('|'))
        objs.reverse()
        print( '\n****************************************')
        print( 'Duplicate names were found in your scene\n\n')
        print( '\n'.join(objs))
        print( '****************************************\n')
        mc.button('checkDulButton', e=1,bgc=(0.5,0.2,0.2))   
        transformNode = mc.ls(objs,transforms=1)
        mc.select(transformNode)
        return 1
    else:
        mc.button('checkDulButton', e=1,bgc=(0.2,0.5,0.2))   
        mc.select(cl=1)
        return 0
        
def selectFromListRun():
    loadSel =  mc.textScrollList('renameListTable',q=1,si=1)
    if loadSel:
        collectData = []
        for a in loadSel:
            listCheck = mc.ls('*' + a +'*',transforms=1,l=1)
            collectData = list(set(collectData) .union(set(listCheck)))
        for a in loadSel:
            listCheck = mc.ls( a +'*',transforms=1,l=1)
            collectData = list(set(collectData) .union(set(listCheck)))  
        if collectData:
            mc.select(collectData)
        else:
            mc.select(cl=1)
        

def removeSelectFromListRun():
    loadSel =  mc.textScrollList('renameListTable',q=1,si=1)
    if loadSel:
        for a in loadSel:
            if a in mc.textScrollList('renameListTable', q=1, ai=1):
                mc.textScrollList('renameListTable', e=1, ri=a)
    saveRenameLib()

def addSelectToListRun():
    filterFieldName = mc.textField('filterText',q=1, tx =1)
    cleanRWFilter()
    loadList =  mc.textScrollList('renameListTable',q=1,ai=1)
    currentSel = mc.ls(sl=1,fl=1,l=1)
    modeState = mc.radioButtonGrp('dictMode',q=1, sl=1)
    collectName = []
    combineList = []
    cleanList = []
    if modeState == 1:
        for c in currentSel:
            removeParent = c.split('|')[-1]
            result = ''.join(i for i in removeParent if not i.isdigit())
            collectName.append(result)
        rubbishName = ['pCylinder','polySurface','pasted_','pCube','pSphere','test']
        filterName = [s for s in collectName if not any(r in s for r in rubbishName)]
        cleanList = []
        for f in filterName:
            removeMtag = f.split('__')[0]
            removeGrp = removeMtag.replace('_grp','')
            removeGeo = removeGrp.replace('_geo','')
            checkName = removeGeo.replace('|','')
            #filter any L,R,F,B
            checkName = checkName.split('_')
            noNumber = [x for x in checkName if not (isinstance(x, str) and x.isnumeric())]
            cleanName = [item for item in noNumber if len(item) > 1]
            cleanList.append('_'.join(cleanName))
    else:
        onlyGeo=[]
        for c in currentSel:
            getType = isGroup(c)
            if getType == 0:
                if '__' in c:
                    onlyGeo.append(c)
        
        for g in onlyGeo:
            matName = g.split('__')[-1].replace('_geo','')
            cleanList.append(matName)
        cleanList =list(set(cleanList))
    if loadList:
        combineList = list(set(loadList).union(set(cleanList)))
    else:
        combineList = cleanList                    
    combineList = list(set(combineList))    
    if filterFieldName:
        combineList.append(filterFieldName)
        cleanList.append(filterFieldName)
    collectList= sorted(combineList)
    mc.textScrollList('renameListTable', e=1, ra=1)
    for c in collectList:
        mc.textScrollList('renameListTable', e=1, append = c)
    mc.textScrollList('renameListTable',e=1,si=cleanList)
    saveRenameLib()

def saveRenameLib():
    cleanRWFilter()
    loadList =  mc.textScrollList('renameListTable',q=1,ai=1)
    newList = '\r\n'.join(loadList)
    cato =  mc.optionMenu('categoryFolder', q=True,v=True)
    sub  =  mc.optionMenu('listSubName', q=True,v=True)
    libPath = mc.textField('reNameLibPath', q=1, tx=1)
    modeState = mc.radioButtonGrp('dictMode',q=1, sl=1)
    loadLibPath = ''
    if modeState == 1:
        loadLibPath = libPath + '/Asset/'
    else:
        loadLibPath = libPath + '/Material/'
    txtPath = loadLibPath + '/' + cato + '/' + sub + '.list'
    fileWrite = open(txtPath, 'w')
    fileWrite.write(newList)
    fileWrite.close()


def updateCato():
    global setLibPath
    menu = mc.optionMenu('categoryFolder', q=True,itemListLong=True)
    if menu:
        mc.deleteUI(menu, menuItem=True)
    libPath = mc.textField('reNameLibPath', q=1, tx=1)
    modeState = mc.radioButtonGrp('dictMode',q=1, sl=1)
    loadLibPath = ''
    if modeState == 1:
        loadLibPath = libPath + '/Asset/'
    else:
        loadLibPath = libPath + '/Material/'
    checkDir = os.path.isdir(loadLibPath)
    if checkDir == True :
        subFolder = next(os.walk(loadLibPath+'/'))[1]
        for s in subFolder:
            mc.menuItem( parent = ( 'categoryFolder'), label = s )


def updateSubList():
    selected = mc.optionMenu('categoryFolder', q=True,v=True)
    readList(selected)
    updateTextList(0)


def readList(listFile):
    menu = mc.optionMenu('listSubName', q=True,itemListLong=True)
    if menu:
        mc.deleteUI(menu, menuItem=True)
    libPath = mc.textField('reNameLibPath', q=1, tx=1)
    modeState = mc.radioButtonGrp('dictMode',q=1, sl=1)
    loadLibPath = ''
    if modeState == 1:
        loadLibPath = libPath + '/Asset/'
    else:
        loadLibPath = libPath + '/Material/'
    
    if loadLibPath:
        checkDir = os.path.isdir(loadLibPath + '/' + listFile + '/')
        if checkDir == True :
            textList = os.listdir((loadLibPath + '/' + listFile + '/'))
            textList = sorted(textList)
            for t in textList:
                if '.list' in t:
                    update=t.split('.')[0]
                    mc.menuItem( parent = ( 'listSubName'), label = update )

def updateTextList(mode):
    cato =  mc.optionMenu('categoryFolder', q=True,v=True)
    sub  =  mc.optionMenu('listSubName', q=True,v=True)
    libPath = mc.textField('reNameLibPath', q=1, tx=1)
    modeState = mc.radioButtonGrp('dictMode',q=1, sl=1)
    filterName = mc.textField('filterText',q=1, tx =1)
    loadLibPath = ''
    if modeState == 1:
        loadLibPath = libPath + '/Asset/'
    else:
        loadLibPath = libPath + '/Material/'
    if loadLibPath:
        txtPath = loadLibPath +  cato + '/' + sub + '.list'
        checkFile = os.path.isfile(txtPath)
        if checkFile == True :
            getList = []
            with open(txtPath) as f:
                line = f.read()
                if line:
                    getList = line.split('\n')
            getList = [item for item in getList if item]
            mc.textScrollList('renameListTable', e=1, ra=1)
            if getList:
                getList = sorted(getList)
                for g in getList:
                    g = g.split('\r')[0]
                    if mode == 0:
                        mc.textScrollList('renameListTable', e=1, append = g)
                    elif mode == 1:
                        if filterName in g:
                            mc.textScrollList('renameListTable', e=1, append = g)
                    
###########################################################################                    
def renameModeSwitch():
    modeState = mc.radioButtonGrp('dictMode',q=1, sl=1)
    if modeState == 1:
        mc.button('ReNameIcon',e=1,bgc = (1,0.75,0.3))
    else:
        mc.button('ReNameIcon',e=1,bgc = (0.3,0.3,0.7))
    updateCato()
    updateSubList()
    storeSwitch()
    setGloablFolderSub()
    updateTextList(0)
    cleanRWFilter()
    
def loadSavedLibPath():
    global setLibPath
    global rwFolder
    global rwSub
    global rwMode
    global rwFolderOld
    global rwSubOld
    rwFolder = ''
    rwFolderOld = ''
    rwSub = ''
    rwSubOld =''
    rwMode = 1
    usd = mc.internalVar(usd=True)
    tempsavePath = usd + 'renameWizardPath'
    checkFile = os.path.isfile(tempsavePath)  
    if checkFile == True:
        getList = []
        with open(tempsavePath) as f:
            line = f.read()
            if line:
                getList = line.split('\r\n')
                checkPath = getList[0].split('#')[0]
                mc.textField('reNameLibPath', edit =True, tx = checkPath )
                setLibPath = checkPath
                rwMode = getList[0].split('#')[1]
                rwFolder = getList[0].split('#')[2]
                rwSub =  getList[0].split('#')[3]
                if rwMode:
                    mc.radioButtonGrp('dictMode',e=1, sl = int(rwMode))
                updateCato()
                if rwFolder:
                    mc.optionMenu('categoryFolder', e =1 , v = rwFolder)
                updateSubList()
                if rwSub:
                    mc.optionMenu('listSubName',  e =1 , v = rwSub)
                rwMode = mc.radioButtonGrp('dictMode',q=1, sl = 1)
                if rwMode == 1:
                    mc.button('ReNameIcon',e=1,bgc = (1,0.75,0.3))
                else:
                    mc.button('ReNameIcon',e=1,bgc = (0.3,0.3,0.7))
                updateTextList(0)
                
def updateGloablFolderSub():
    global rwFolder
    global rwSub
    global rwMode
    rwFolder = mc.optionMenu('categoryFolder', q =1 , v = 1)
    rwSub = mc.optionMenu('listSubName', q =1 , v = 1)
    rwMode = mc.radioButtonGrp('dictMode',q=1, sl = 1)


def storeSwitch():
    global rwFolder
    global rwSub
    global rwMode
    global rwFolderOld
    global rwSubOld
    rwFolderOld = rwFolder
    rwSubOld = rwSub
    
def setGloablFolderSub():
    global rwFolderOld
    global rwSubOld
    item_list = mc.optionMenu('categoryFolder', q=True, ils=True)
    qList= []
    for i in range(0,len(item_list)):
        mc.optionMenu('categoryFolder',e=1, sl = (i+1))
        check = mc.optionMenu('categoryFolder',q=1, v =1)
        if rwFolderOld == check:
            break
    updateSubList()
    item_list = mc.optionMenu('listSubName', q=True, ils=True)
    qList= []
    for i in range(0,len(item_list)):
        mc.optionMenu('listSubName',e=1, sl = (i+1))
        check = mc.optionMenu('listSubName',q=1, v =1)
        if rwSubOld == check:
            break

def storeFolderSub():
    global setLibPath
    global rwFolder
    global rwSub
    global rwMode
    
    usd = mc.internalVar(usd=True)
    tempsavePath = usd + 'renameWizardPath'
    fileWrite = open(tempsavePath, 'w')
    storeData = setLibPath + '#' + str(rwMode) + '#' + rwFolder + '#' + rwSub
    fileWrite.write(storeData)
    fileWrite.close()

###########################################################################################


def setRenameLibPath():
    global setLibPath
    #setLibPath = pm.fileDialog2(fm=3, okc='selectFolder', cap='Select Libarary Folder')[0]
    setLibPath = mc.fileDialog2(fm=3, okc='selectFolder', cap='Select Library Folder')[0]
    mc.textField('reNameLibPath', edit =True, tx = setLibPath )
    usd = mc.internalVar(usd=True)
    tempsavePath = usd + 'renameWizardPath'
    fileWrite = open(tempsavePath, 'w')
    fileWrite.write(setLibPath)
    fileWrite.close()
    updateCato()
    updateSubList()

def renameWizard():
    renameWizardUI()
    loadSavedLibPath()

def renameWizardUI():
    mel.eval('source dagMenuProc;')
    if mc.window("renameWizardUI", exists = True):
        mc.deleteUI("renameWizardUI")
    renameWizardUI = mc.window("renameWizardUI",title = "Rename Wizard v1.30",w = 400,h = 600)
    mc.columnLayout()
    mc.rowColumnLayout(nc= 2 ,cw=[(1,250),(2,150)])
    mc.paneLayout()
    mc.columnLayout()
    mc.rowColumnLayout(nc= 3 ,cw=[(1,50),(2,120),(3,20)])
    mc.text(l ='Filter:',h=10)
    mc.textField('filterText', tx ='',tcc='updateTextList(1)')
    mc.button(label='x', bgc = (0.2, 0.2, 0.2), c=lambda *x:cleanRWFilter())
    mc.setParent( '..' )
    mc.textScrollList('renameListTable', h= 600, allowMultiSelection= 1, sc ='checkFilterSel()' )
    mc.rowColumnLayout(nc= 3 ,cw=[(1,120),(2,3),(3,120)])
    mc.button(label='<< Outliner',bgc = (0.2, 0.2, 0.2), c=lambda *x:selectFromListRun()) 
    mc.text(l ='',h=10)
    mc.button(label='Library >>',bgc = (0.2, 0.2, 0.2), c=lambda *x:highLigtRList())
    mc.setParent( '..' )
    mc.text(l ='')
    mc.text(l ='  Library Path:')
    mc.rowColumnLayout(nc=3,cw=[(1,10),(2,170),(3,60)])
    mc.text(l ='')
    mc.textField('reNameLibPath', tx ='')
    mc.button('setLiblButton',  l= 'Set', en=True,  bgc = (0.24, 0.24, 0.24),c= 'setRenameLibPath()')
    mc.setParent( '..' )
    mc.setParent( '..' )
    mc.setParent( '..' )
    mc.frameLayout(w=150, label = 'Dictionary',bgc=(0,0,0))
    mc.columnLayout(adj=1)
    mc.radioButtonGrp('dictMode',nrb=2, sl=1, cw=((1,70),(2,50)), la2=("Asset", "Material"),cc='renameModeSwitch()')
    mc.optionMenu('categoryFolder', w=120, h =30,bgc = [0.24,0.24,0.24],cc = 'updateSubList(),updateGloablFolderSub()')
    mc.menuItem( label= '' )
    mc.optionMenu('listSubName', w=120, h =30,bgc = [0.24,0.24,0.24],cc = 'updateTextList(0),updateGloablFolderSub()')
    mc.menuItem( label= '' )
    mc.button(label='Create New List', bgc = (0.2, 0.2, 0.2), c=lambda *x:createNewLibUI())
    mc.setParent( '..' )
    mc.frameLayout(w=150, label = 'List Edit',bgc=(0,0,0))
    mc.columnLayout(adj=1)
    mc.rowColumnLayout(nc= 3 ,cw=[(1,72),(2,2),(3,72)])
    mc.button(label='Add', bgc = (0.2, 0.4, 0.2),c=lambda *x:addSelectToListRun())
    mc.text(l ='',h=10)
    mc.button(label='Remove ', bgc = (0.4, 0.2, 0.2), c=lambda *x:removeSelectFromListRun())
    mc.setParent( '..' )
    mc.text(l ='',h=10)
    mc.frameLayout(w=150, label = 'Quick Tools',bgc=(0,0,0))
    mc.columnLayout(adj=1)
    mc.rowColumnLayout(nc= 4 ,cw=[(1,36),(2,36),(3,5),(4,74)])
    mc.button(label='L_',bgc = (0.15,0.28, 0.3 ),c= "quickPrefix(0,'L')" )
    mc.button(label='R_',bgc = (0.15,0.28, 0.3 ),c= "quickPrefix(0,'R')" )
    mc.text(l ='',h=10)
    mc.button(label='auto L/R',bgc = (0.15, 0.17, 0.3 ),c="autoSetLR()" )
    mc.setParent( '..' )
    mc.rowColumnLayout(nc= 5 ,cw=[(1,24),(2,24),(3,24),(4,5),(5,74)])
    mc.button(label='F_',bgc = (0.15,0.28, 0.3 ),c= "quickPrefix(0,'F')" )
    mc.button(label='M_',bgc = (0.15,0.28, 0.3 ),c= "quickPrefix(0,'M')" )
    mc.button(label='B_',bgc = (0.15,0.28, 0.3 ),c= "quickPrefix(0,'B')" )
    mc.text(l ='',h=10)
    mc.button(label='auto F/B',w=35,bgc = (0.15, 0.17, 0.3 ),c="autoSetFB()" )
    mc.setParent( '..' )
    mc.rowColumnLayout(nc= 5 ,cw=[(1,24),(2,24),(3,24),(4,5),(5,74)])
    mc.text(l ='',h=10)
    mc.text(l ='',h=10)
    mc.text(l ='',h=10)
    mc.text(l ='',h=10)
    mc.button(label='auto END',w=35,bgc = (0.15, 0.17, 0.3 ),c="quickFixEnd()" )
    mc.setParent( '..' )
    mc.rowColumnLayout(nc= 2 ,cw=[(1,74),(2,74)])
    mc.setParent( '..' )
    mc.text(l ='',h=10)
    mc.rowColumnLayout(nc= 7 ,cw=[(1,10),(2,26),(3,36),(4,5),(5,36),(6,26),(7,10)])
    mc.text(l ='>',h=10)
    mc.button(label='[]',bgc = (0.42,0.22, 0.22 ),c="removeOneLetter(0)" )
    mc.button(label='_',bgc = (0.42,0.22, 0.22 ),c="removeOneUnderScore(0)" )
    mc.text(l ='',h=10)
    mc.button(label='_',bgc = (0.42,0.22, 0.22 ),c="removeOneUnderScore(1)" )
    mc.button(label='[]',bgc = (0.42,0.22, 0.22 ),c="removeOneLetter(1)" )
    mc.text(l ='<',h=10)
    mc.setParent( '..' )
    mc.rowColumnLayout(nc= 5 ,cw=[(1,10),(2,62),(3,5),(4,62),(5,10)])
    mc.text(l ='>',h=10)
    mc.button(label='x 001',bgc = (0.42,0.22, 0.22 ),c="removeNameNumber()" )
    mc.text(l ='',h=10)
    mc.button(label='x M-Tag',bgc = (0.42,0.22, 0.22 ),c="removeNameMTag()" )
    mc.text(l ='<',h=10)
    mc.setParent( '..' )
    mc.text(l ='',h=10)
    mc.columnLayout(adj=1)
    mc.button(label='Carry Group Name', bgc = (0.2, 0.2, 0.2),c=lambda *x:carryName()) 
    mc.button(label='Fix Shape Name', bgc = (0.2, 0.2, 0.2),c=lambda *x:fixShapeName()) 
    mc.button(label='Shader to Name', bgc = (0.2, 0.2, 0.2),c=lambda *x:shader2Name()) 
    mc.button(label='Perfect Number', bgc = (0.2, 0.2, 0.2),c=lambda *x:perfectSceneNumber())
    mc.button('checkDulButton',label='Check Dulpicate', bgc = (0.2, 0.2, 0.2), c=lambda *x:colourDuplicate())
    mc.setParent( '..' )
    mc.frameLayout(w=150, label = 'Auto' ,bgc=(0,0,0))
    mc.columnLayout(adj=1)
    mc.text(l ='',h=5)
    mc.checkBox('AutoCheckSide', l= "Left / Right", v=0 )
    mc.checkBox('AutoCheckPosition', l= "Front / Back", v=0 )
    mc.checkBox('keepMTag', l= "keep Material Tag", v=0 )
    mc.text(l ='',h=10)
    mc.checkBox('autoHideBox', l= "Hide After Rename",v=0)
    mc.text(l ='',h=20)
    mc.button('ReNameIcon',label='ReName',bgc = (1,0.75,0.3), w=140,h=140, c=lambda *x:renameMagic())
    mc.setParent( '..' )
    mc.showWindow(renameWizardUI)
    mc.scriptJob(uiDeleted=["renameWizardUI", storeFolderSub])

renameWizard()
#Utility