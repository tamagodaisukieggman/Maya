# -*- coding: utf-8 -*-
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.cmds as cmds
import maya.mel as mel
import math
import os
import csv

def getCSVdata():
    csvpath = "//cgs-str-fas05/100_projects/117_mutsunokami/30_design/environment/document/Env_AlphaTest.csv"
    rethash = {}
    with open(csvpath) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i > 2:
                if row[2] != "":
                    rawData = {}
                    rgbArry = []
                    rgbVal = row[3].split(",")
                    rgbArry.append(rgbVal[0])
                    rgbArry.append(rgbVal[1])
                    rgbArry.append(rgbVal[2])
                    rawData["id"]= row[2]
                    rawData["rgb"]= rgbArry
                    rawData["detail"]= row[5]
                    rethash[row[2]] = rawData          
    return rethash
                
def addVColor(rgbArryFloat_R, rgbArryFloat_G, rgbArryFloat_B):
    print "test"
    print rgbArryFloat_R, rgbArryFloat_G, rgbArryFloat_B
    csvDataHash = getCSVdata()
    selTarget = cmds.ls(selection=True)
    cmds.polyColorPerVertex(selTarget, r=float(rgbArryFloat_R), g=float(rgbArryFloat_G), b=float(rgbArryFloat_B), a=1.0, cdo=True)

          
def create_SPMatVcolorWindow():
    csvDataHash = getCSVdata()
    cmds.window(title='Create_SPMatVcolor')
    cmds.columnLayout()
    materialID = ""
    for idName, rawDataList in csvDataHash.items():
        materialID = idName
        ColorVal = rawDataList["rgb"]
        ColorValR = float(ColorVal[0])
        ColorValG = float(ColorVal[1])
        ColorValB = float(ColorVal[2])
        ColorValR = ColorValR/255
        ColorValG = ColorValG/255
        ColorValB = ColorValB/255
        cmds.button(materialID, label=materialID, backgroundColor=(ColorValR,ColorValG,ColorValB), width=200,command="createSPVcolor.addVColor("+str(ColorValR)+", "+str(ColorValG)+", "+str(ColorValB)+")")
    
    cmds.showWindow()



