//
// Copyright (C) cygames
// 
// File: pluginMain.cpp
//
// Author: Maya Plug-in Wizard 2.0
//

#include "curveLocatorNode.h"

#include <maya/MFnPlugin.h>

static bool sUseLegacyDraw = (getenv("MAYA_ENABLE_VP2_PLUGIN_LOCATOR_LEGACY_DRAW") != NULL);


MStatus initializePlugin(MObject obj)
{
	MStatus   status;
	MFnPlugin plugin(obj, PLUGIN_COMPANY, "0.1", "Any");
	status = plugin.registerNode(
		"curveLocator",
		curveLocator::id,
		&curveLocator::creator,
		&curveLocator::initialize,
		MPxNode::kLocatorNode,
		sUseLegacyDraw ? NULL : &curveLocator::drawDbClassification);
	if (!status) {
		status.perror("registerNode");
		return status;
	}
	if (!sUseLegacyDraw)
	{
		status = MHWRender::MDrawRegistry::registerDrawOverrideCreator(
			curveLocator::drawDbClassification,
			curveLocator::drawRegistrantId,
			CurveLocatorDrawOverride::Creator);
		if (!status) {
			status.perror("registerDrawOverrideCreator");
			return status;
		}
	}
	return status;
}
MStatus uninitializePlugin(MObject obj)
{
	MStatus   status;
	MFnPlugin plugin(obj);
	if (!sUseLegacyDraw)
	{
		status = MHWRender::MDrawRegistry::deregisterDrawOverrideCreator(
			curveLocator::drawDbClassification,
			curveLocator::drawRegistrantId);
		if (!status) {
			status.perror("deregisterDrawOverrideCreator");
			return status;
		}
	}
	status = plugin.deregisterNode(curveLocator::id);
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}
	return status;
}
