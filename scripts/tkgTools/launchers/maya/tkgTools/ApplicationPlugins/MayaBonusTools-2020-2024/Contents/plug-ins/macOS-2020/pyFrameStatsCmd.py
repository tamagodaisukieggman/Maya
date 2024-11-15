# ===========================================================================
# Copyright 2015 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================

"""
This command is used to provide frame statistics to help comparing the 
performance of animation playback or viewport manipulation, for example 
in different viewport or differnt version of Maya.

To use it, make sure that pyFrameStatsCmd.py is in your MAYA_PLUG_IN_PATH
then do the following:
import maya
maya.cmds.loadPlugin("pyFrameStatsCmd.py")
maya.cmds.frameStats(frameCount = True)
maya.cmds.frameStats(frameIndex = 0, frameInfo = True)
maya.cmds.frameStats(frameIndex = 0, dirtyPropagation = True)
maya.cmds.frameStats(frameIndex = 0, evaluation = True)
maya.cmds.frameStats(frameIndex = 0, render = True)

NOTE: All events are gathered until a frameEndRender event occurs, 
at which point the collected events are assigned to that frame. 
The the collection ('currentFrame') is cleared and we start the 
next frame.
It only make sense to talk about frame when viewport refresh, 
for example, when playback or manipulation happens.
Anything happen before the rendering of that frame will be taken as 
the preparation of the first frame.
So if you start recording events, do a couple of other things, then 
do a playback. Any events generated by those "couple of other things" 
will appear in the stats for the first frame.
In this case, you may want to ignore the first frame info, because 
it contains more things that is not related to frame rendering than 
other frames following it.

"""

import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

class eventInfo():
	def __init__(self):
		self.eventName = ''
		self.eventType = ''
		self.eventDuration = 0

class frameInfo():
	def __init__(self):
		self.frameIndex = -1
		self.eventsInFrame = []
		self.dirtyPropagationSum = 0
		self.evaluationSum = 0
		self.renderSum = 0
	
	def addEvent(self, eventInfo):
		self.eventsInFrame.append(eventInfo)
	
	def getEventCount(self):
		return len(self.eventsInFrame)

# command
class PyFrameStatsCmd(OpenMayaMPx.MPxCommand):
	kPluginCmdName = "frameStats"

	frameCountFlag = '-fc'
	frameCountFlagLong = '-frameCount'
	
	frameIndexFlag = '-fi'
	frameIndexFlagLong = '-frameIndex'
	
	dirtyPropagationFlag = '-dp'
	dirtyPropagationFlagLong = '-dirtyPropagation'
	
	evaluationFlag = '-ev'
	evaluationFlagLong = '-evaluation'
	
	renderFlag = '-re'
	renderFlagLong = '-render'
	
	frameInfoFlag = '-fr'
	frameInfoFlagLong = '-frameInfo'
	
	dirtyPropagationEvents = ['SetCurrentTime', 'PreRefreshTopLevel']
	evaluationEvents = ['Vp2PrepareToUpdate', 'Vp1TraverseView']
	renderEvents = ['Vp1UpdateCache', 'Vp1RefreshTraversal', 'Vp1PostTraversal']
	frameEndRenderEvents = ['Vp2BuildRenderLists', 'Vp1PostRefresh']
		
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)
		self.kFrameCount = 0
		self.kFrameList = []

	@staticmethod
	def cmdCreator():
		return OpenMayaMPx.asMPxPtr( PyFrameStatsCmd() )

	@staticmethod
	def createSyntax():
		"""
		The frameCount/fc flag:       get the frame count in the profiling buffer.
		The frameIndex/fi flag:       specify the index of the frame.
		The dirtyPropagation/dp flag: query the time spent on dirty propagation for the frame specified by frameIndex.
		The evaluation/ev flag:       query the time spent on evaluation for the frame specified by frameIndex.
		The render/rn flag:           query the time spent on rendering for the frame specified by frameIndex.
		The frameInfo/fr flag:        query the event info for the frame specified by frameIndex.
		Time is in unit of microseconds.
		"""
		syntax = OpenMaya.MSyntax()
		syntax.addFlag(PyFrameStatsCmd.frameCountFlag, PyFrameStatsCmd.frameCountFlagLong)
		syntax.addFlag(PyFrameStatsCmd.frameIndexFlag, PyFrameStatsCmd.frameIndexFlagLong, OpenMaya.MSyntax.kUnsigned)
		syntax.addFlag(PyFrameStatsCmd.dirtyPropagationFlag, PyFrameStatsCmd.dirtyPropagationFlagLong)
		syntax.addFlag(PyFrameStatsCmd.evaluationFlag, PyFrameStatsCmd.evaluationFlagLong)
		syntax.addFlag(PyFrameStatsCmd.renderFlag, PyFrameStatsCmd.renderFlagLong)
		syntax.addFlag(PyFrameStatsCmd.frameInfoFlag, PyFrameStatsCmd.frameInfoFlagLong)
		return syntax
	
	@staticmethod
	def prepareFrameData(self):
		"""
		Get all events in current profiling buffer and wrap them up into frames
		"""
		
		eventCount = OpenMaya.MProfiler.getEventCount()
		currentFrame = frameInfo()
		for i in range(0, eventCount):
			eventName = OpenMaya.MProfiler.getEventName(i)
			
			if eventName in PyFrameStatsCmd.dirtyPropagationEvents:
				currentEventInfo = eventInfo()
				currentEventInfo.eventName = eventName
				currentEventInfo.eventType = 'DirtyPropagation'
				currentEventInfo.eventDuration = OpenMaya.MProfiler.getEventDuration(i)
				currentFrame.addEvent(currentEventInfo)
				currentFrame.dirtyPropagationSum += currentEventInfo.eventDuration
			elif eventName in PyFrameStatsCmd.evaluationEvents:
				currentEventInfo = eventInfo()
				currentEventInfo.eventName = eventName
				currentEventInfo.eventType = 'Evaluation'
				currentEventInfo.eventDuration = OpenMaya.MProfiler.getEventDuration(i)
				currentFrame.addEvent(currentEventInfo)
				currentFrame.evaluationSum += currentEventInfo.eventDuration
			elif eventName in PyFrameStatsCmd.renderEvents or eventName in PyFrameStatsCmd.frameEndRenderEvents:
				currentEventInfo = eventInfo()
				currentEventInfo.eventName = eventName
				currentEventInfo.eventType = 'Render'
				currentEventInfo.eventDuration = OpenMaya.MProfiler.getEventDuration(i)
				currentFrame.addEvent(currentEventInfo)
				currentFrame.renderSum += currentEventInfo.eventDuration
				
				if eventName in PyFrameStatsCmd.frameEndRenderEvents:
					currentFrame.frameIndex = self.kFrameCount
					self.kFrameList.append(currentFrame)
					self.kFrameCount = self.kFrameCount + 1
					currentFrame = frameInfo()

	def doIt(self, args):
		self.prepareFrameData(self)
		
		# Use an MArgDatabase to Parse our command
		argdb = OpenMaya.MArgDatabase(self.syntax(), args)
		
		# frameCount flag
		if argdb.isFlagSet(PyFrameStatsCmd.frameCountFlag):
			self.setResult(self.kFrameCount)
		
		# frameIndex flag
		if argdb.isFlagSet(PyFrameStatsCmd.frameIndexFlag):
			frameIndex = argdb.flagArgumentInt(PyFrameStatsCmd.frameIndexFlag, 0)
			# dirtyPropagationFlag
			if argdb.isFlagSet(PyFrameStatsCmd.dirtyPropagationFlag):
				self.setResult(self.kFrameList[frameIndex].dirtyPropagationSum)
			# evaluationFlag
			if argdb.isFlagSet(PyFrameStatsCmd.evaluationFlag):
				self.setResult(self.kFrameList[frameIndex].evaluationSum)
			# renderFlag
			if argdb.isFlagSet(PyFrameStatsCmd.renderFlag):
				self.setResult(self.kFrameList[frameIndex].renderSum)
			# frameInfoFlag
			if argdb.isFlagSet(PyFrameStatsCmd.frameInfoFlag):
					frame = self.kFrameList[frameIndex]
					eventCount = frame.getEventCount()
					result = '\n'
					for event in frame.eventsInFrame:
						result = "{}{}{}{}{}{}{}{}".format(result, 'Time:', str(event.eventDuration).ljust(20), '|', event.eventType.ljust(20), '|', event.eventName.ljust(20) , '\n')
					self.setResult(result)

# Initialize the plug-in
def initializePlugin(plugin):
	pluginFn = OpenMayaMPx.MFnPlugin(plugin)
	try:
		pluginFn.registerCommand(
			PyFrameStatsCmd.kPluginCmdName, PyFrameStatsCmd.cmdCreator, PyFrameStatsCmd.createSyntax
		)
	except:
		sys.stderr.write(
			"Failed to register command: %s\n" % PyFrameStatsCmd.kPluginCmdName
		)
		raise

# Uninitialize the plug-in
def uninitializePlugin(plugin):
	pluginFn = OpenMayaMPx.MFnPlugin(plugin)
	try:
		pluginFn.deregisterCommand(PyFrameStatsCmd.kPluginCmdName)
	except:
		sys.stderr.write(
			"Failed to unregister command: %s\n" % PyFrameStatsCmd.kPluginCmdName
		)
		raise
