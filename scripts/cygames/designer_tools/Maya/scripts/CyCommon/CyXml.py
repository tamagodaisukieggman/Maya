# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

from xml.dom import minidom, Node
import os.path

#-------------------------------------------------------------------------------------------
#   CyXmlクラス
#-------------------------------------------------------------------------------------------
class CyXml:

    @staticmethod
    def CreateDocument(filePath, rootNodeName):

        doc = minidom.Document()

        root = doc.createElement(rootNodeName)
        doc.appendChild(root)

        tempFile = open(filePath, "w")
        tempFile.write(doc.toprettyxml('  ', '\n', 'utf-8'))
        tempFile.close()

        return doc

    @staticmethod
    def SaveDocument(filePath, xmlDoc):

        if os.path.isfile(filePath) == False:
            return

        tempStr = xmlDoc.toprettyxml('  ', '\n', 'utf-8')
        tempFile = open(filePath, "w")
        
        tempStr = tempStr.replace('  \n','')
        tempStr = tempStr.replace('\n\n','\n')
        tempStr = tempStr.replace('\n    ','\n  ')
        
        tempFile.write(tempStr)        
        tempFile.close()

    @staticmethod
    def GetDocument(filePath):

        if os.path.isfile(filePath) == False:
            return None

        try:
            return minidom.parse(filePath)
        except:
            return None      

    @staticmethod
    def GetNodeList(nodeName,rootNode):

        result = []

        parentNodes = []
        if nodeName != "":
                parentNodes = rootNode.getElementsByTagName(nodeName)
        else:
                parentNodes.append(rootNode)

        if parentNodes == None:
                return result

        if len(parentNodes) == 0:
                return result

        parentNode = parentNodes[0]

        for node in parentNode.childNodes:

                if node.nodeType != node.ELEMENT_NODE:
                        continue

                result.append(node)

        return result;

    @staticmethod
    def GetAttrValue(attrName, rootNode):

            for index in range(rootNode.attributes.length):

                    item = rootNode.attributes.item(index)


                    if item.name == attrName:
                            return item.value
                            break
            return ""

    
