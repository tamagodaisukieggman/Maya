
#include "cyWldSkeletonTransferNode.h"

#include <maya/MFnPlugin.h>

MStatus initializePlugin( MObject obj )
{ 
	MStatus   status;
	MFnPlugin plugin( obj, "cygames", "2018", "Any");

	status = plugin.registerNode( "cyWldSkeletonTransferNode", cyWldSkeletonTransferNode::id, cyWldSkeletonTransferNode::creator,
								  cyWldSkeletonTransferNode::initialize );
	if (!status) {
		status.perror("registerNode");
		return status;
	}

	return status;
}

MStatus uninitializePlugin( MObject obj)
{
	MStatus   status;
	MFnPlugin plugin( obj );

	status = plugin.deregisterNode( cyWldSkeletonTransferNode::id );
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	return status;
}
