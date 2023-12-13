# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

import math

#-------------------------------------------------------------------------------------------
#   Vectorクラス
#-------------------------------------------------------------------------------------------
class CyVector:

    #===========================================
    # 2つの位置の距離を計測
    #===========================================
    @staticmethod
    def GetDistance(value0, value1):

        return math.sqrt(CyVector.GetSqrtDistance(value0,value1))

    #===========================================
    # 2つの位置の距離を計測
    #===========================================
    @staticmethod
    def GetSqrtDistance(value0, value1):

        if len(value0) != 3:
            return 10000000

        if len(value0) != len(value1):
            return 10000000

        result = 0
        for p in range(len(value0)):

            result += (value1[p] - value0[p]) * (value1[p] - value0[p])

        return result

#-------------------------------------------------------------------------------------------
#   Vector3クラス
#-------------------------------------------------------------------------------------------
class CyVector3:

    def __init__(self):

        self.x=0
        self.y=0
        self.z=0

#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------    
 
def Copy(source):
 
    result = [0,0,0]
 
    result[0]=source[0]
    result[1]=source[1]
    result[2]=source[2]
 
    return result
 
#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------    
 
def Add(source,dest):
 
    result = [0,0,0]
 
    tempVec0 = Copy(source)
    tempVec1 = Copy(dest)
 
    result[0]=tempVec0[0]+tempVec1[0]
    result[1]=tempVec0[1]+tempVec1[1]
    result[2]=tempVec0[2]+tempVec1[2]
 
    return result
 
#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------    
 
def Sub(source,dest):
 
    result = [0,0,0]
 
    tempVec0 = Copy(source)
    tempVec1 = Copy(dest)
 
    result[0]=tempVec0[0]-tempVec1[0]
    result[1]=tempVec0[1]-tempVec1[1]
    result[2]=tempVec0[2]-tempVec1[2]
 
    return result
 
#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------    
 
def Multiply(source,dest):
 
    result = [0,0,0]
 
    tempVec0 = Copy(source)
    tempVec1 = Copy(dest)
 
    result[0]=tempVec0[0]*tempVec1[0]
    result[1]=tempVec0[1]*tempVec1[1]
    result[2]=tempVec0[2]*tempVec1[2]
 
    return result
 
#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------    
 
def Divide(source,dest):
 
    result = [0,0,0]
 
    tempVec0 = Copy(source)
    tempVec1 = Copy(dest)
 
    if tempVec1[0]*tempVec1[1]*tempVec1[2] != 0:
         
        result[0]=tempVec0[0]/tempVec1[0]
        result[1]=tempVec0[1]/tempVec1[1]
        result[2]=tempVec0[2]/tempVec1[2]
         
    else:
         
        result[0]=tempVec0[0]
        result[1]=tempVec0[1]
        result[2]=tempVec0[2]
 
    return result
 
#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------    
 
def LengthSq(source):
 
    result = 0
 
    tempVec0 = Copy(source)
 
    result = math.pow(tempVec0[0],2) + math.pow(tempVec0[1],2) + math.pow(tempVec0[2],2)
 
    return result
 
#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------    
 
def Length(source):
 
    result = 0
 
    tempVec0 = Copy(source)
 
    result = LengthSq(tempVec0)
 
    result = math.sqrt(result)
 
    return result
 
#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------    
 
def Distance(source,dest):
 
    result = 0
 
    tempVec0 = Copy(source)
    tempVec1 = Copy(dest)
 
    tempVec2 = Sub(tempVec0,tempVec1)
 
    result = Length(tempVec2)
 
    return result
     
 
#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------    
 
def Normalize(source):
 
    result = [0,0,0]
 
    tempVec0 = Copy(source)
 
    thisLength = Length(tempVec0)
 
    if thisLength != 0:
        result[0] = tempVec0[0]/thisLength
        result[1] = tempVec0[1]/thisLength
        result[2] = tempVec0[2]/thisLength
 
    return result
 
#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------    
 
def AddValue(source,value):
 
    result = [0,0,0]
 
    tempVec0 = Copy(source)
 
    result[0]=tempVec0[0]+value
    result[1]=tempVec0[1]+value
    result[2]=tempVec0[2]+value
 
    return result
 
#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------    
 
def MultiplyValue(source,value):
 
    result = [0,0,0]
 
    tempVec0 = Copy(source)
 
    result[0]=tempVec0[0]*value
    result[1]=tempVec0[1]*value
    result[2]=tempVec0[2]*value
 
    return result
 
#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------    
 
def DivideValue(source,value):
 
    result = [0,0,0]
 
    tempVec0 = Copy(source)
 
    if value!=0:
        result[0]=tempVec0[0]/value
        result[1]=tempVec0[1]/value
        result[2]=tempVec0[2]/value
    else:
        result[0]=tempVec0[0]
        result[1]=tempVec0[1]
        result[2]=tempVec0[2]
 
    return result
 
#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------    
 
def Dot(source,dest,normal):
 
    result = 0
 
    tempVec0 = Copy(source)
    tempVec1 = Copy(dest)
 
    if normal == 1:
 
        tempVec0 = Normalize(tempVec0)
        tempVec1 = Normalize(tempVec1)
 
    tempVec2 = Multiply(tempVec0,tempVec1)
    result=tempVec2[0]+ tempVec2[1] + tempVec2[2]
 
    return result
 
#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------    
 
def Angle(source,dest):
 
    result = 0
 
    tempVec0 = Copy(source)
    tempVec1 = Copy(dest)
 
    dot = Dot(tempVec0,tempVec1,1)
 
    result = math.degrees(math.acos(dot))
 
    return result
 
     
 
#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------    
 
def Cross(source,dest,normal):
 
    tempVec0 = Copy(source)
    tempVec1 = Copy(dest)
 
    if normal == 1:
 
        tempVec0 = Normalize(tempVec0)
        tempVec1 = Normalize(tempVec1)
 
    result = [0,0,0]
    result[0] = tempVec0[1]*tempVec1[2] - tempVec0[2]*tempVec1[1]
    result[1] = tempVec0[2]*tempVec1[0] - tempVec0[0]*tempVec1[2]
    result[2] = tempVec0[0]*tempVec1[1] - tempVec0[1]*tempVec1[0]
 
    if normal == 1:
        result = Normalize(result)
 
    return result
 
#-------------------------------------------------------------------------------------------
#   反射ベクトルを取得
#-------------------------------------------------------------------------------------------    
 
def Reflect(source,normVec,normal):
 
    tempVec0 = Copy(source)
    tempVec1 = Copy(normVec)
    tempVec1 = Normalize(tempVec1)
 
    if normal == 1:
 
        tempVec0 = Normalize(tempVec0)
 
    result = [0,0,0]
    tempValue00=Dot(tempVec0,tempVec1,0)
    result=MultiplyValue(tempVec1,tempValue00*2.0)
    result=Sub(tempVec0,result)
 
    return result
 
#-------------------------------------------------------------------------------------------
#   4x4の行列で変換した値を出力
#-------------------------------------------------------------------------------------------    
def Transform(source,matrix):
 
    result = [0,0,0]
    num = 4
 
    tempVec0 = Copy(source)
    tempVec0.append(1)
 
    tempVec1=[0,0,0,1]
 
    for i in range(num):
 
        tempValue00=0
        for j in range(num):
            tempValue00+=tempVec0[j]*matrix[j][i]
 
        tempVec1[i]=tempValue00
 
    for i in range(len(result)):
 
        result[i]=tempVec1[i]
 
    return result
 
#-------------------------------------------------------------------------------------------
#   回転、スケール、移動の順番でマトリックスをかけた値を出力
#-------------------------------------------------------------------------------------------    
 
def TransformRST(source,rot,scale,trans):
 
    tempVec0 = Copy(source)
 
    tempVec0 = Transform(tempVec0,Com_Matrix.Scale(scale))
 
    tempVec0 = Transform(tempVec0,Com_Matrix.RotateX(rot[0]))
    tempVec0 = Transform(tempVec0,Com_Matrix.RotateY(rot[1]))
    tempVec0 = Transform(tempVec0,Com_Matrix.RotateZ(rot[2]))
     
    tempVec0 = Transform(tempVec0,Com_Matrix.Translate(trans))
 
    return tempVec0
 
#-------------------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------------------  
def Lerp(source,dest,lerpValue):
 
    result = [0,0,0]
 
    tempVec0 = Copy(source)
    tempVec1 = Copy(dest)
 
    result[0]=tempVec0[0]*(1-lerpValue)+tempVec1[0]*lerpValue
    result[1]=tempVec0[1]*(1-lerpValue)+tempVec1[1]*lerpValue
    result[2]=tempVec0[2]*(1-lerpValue)+tempVec1[2]*lerpValue
 
    return result
 
#-------------------------------------------------------------------------------------------
#   軸方向から回転値を求める
#-------------------------------------------------------------------------------------------  
def GetRotateFromVectors(xVector,yVector,zVector,mode):
 
    rot = [0,0,0]
 
    if mode == 0:
 
        rot[2] = math.atan2(xVector[1],xVector[0])
        rot[1] = -math.asin(xVector[2])
 
        tempValue=math.cos(rot[1])
 
        if tempValue !=0:
            try:
                rot[0] = math.asin(yVector[2]/tempValue)
            except:
                temp = 0
                 
            if(zVector[2]<0):
                rot[0]=math.radians(180)-rot[0]
        else:
            rot[2] = math.atan2(yVector[0],yVector[1])
            rot[1] = -math.asin(xVector[2])
            rot[0] = 0
 
    if mode == 5:
 
        rot[2] = math.atan2(zVector[1],zVector[2])
        rot[1] = -math.asin(zVector[0])
 
        tempValue=math.cos(rot[1])
 
        if tempValue !=0:
            try:
                rot[0] = math.asin(yVector[0]/tempValue)
            except:
                temp = 0
                 
            if(xVector[0]<0):
                rot[0]=math.radians(180)-rot[0]
        else:
            rot[2] = math.atan2(yVector[2],yVector[1])
            rot[1] = -math.asin(zVector[0])
            rot[0] = 0
 
    for i in range(len(rot)):
 
        rot[i]=math.degrees(rot[i])
 
    return rot
