#include <maya/MStatus.h>
#include <maya/MArgList.h>
#include <maya/MFnPlugin.h>
#include <maya/MObject.h>
#include <maya/MGlobal.h>
#include <maya/MDagPath.h>
#include <maya/MItSelectionList.h>
#include <maya/MSelectionList.h>
#include <maya/MString.h>
#include <maya/MPoint.h>

#include <maya/MItCurveCV.h>
#include <maya/MItSurfaceCV.h>
#include <maya/MItMeshVertex.h>

#include <maya/MIOStream.h>
#include <maya/MSyntax.h>
#include <maya/MArgParser.h>
#include <maya/MGlobal.h>
#include <maya/MFnMesh.h>
#include <maya/MDagPath.h>
#include <maya/MDagPath.h>

#include <sstream>

#include "apiutils.h"
#include "utilcmds.h"


selectNearVertices::selectNearVertices()
{
}

selectNearVertices::~selectNearVertices() {}

void* selectNearVertices::creator()
{
	return new selectNearVertices;
}

bool selectNearVertices::isUndoable() const
{
	return true;
}

MStatus selectNearVertices::undoIt()
{
	return MS::kSuccess;
}

MSyntax selectNearVertices::syntax()
{
	MSyntax s;
	s.addFlag("-p", "-point", MSyntax::kDouble, MSyntax::kDouble, MSyntax::kDouble);
	s.addFlag("-m", "-mesh", MSyntax::kString);
	s.addFlag("-c", "-count", MSyntax::kLong);
	return s;
}

MStatus selectNearVertices::doIt(const MArgList& args)
{
	MArgParser p(syntax(), args);
	MPoint pnt;
	if (p.isFlagSet("p"))
	{
		double px = p.flagArgumentDouble("p", 0);
		double py = p.flagArgumentDouble("p", 1);
		double pz = p.flagArgumentDouble("p", 2);
		pnt = MPoint(px, py, pz);
	}
	MObject mesh;
	if (p.isFlagSet("m"))
	{
		MSelectionList slist;
		MGlobal::getSelectionListByName(p.flagArgumentString("m", 0), slist);
		slist.getDependNode(0, mesh);
	}
	if (mesh.isNull())
	{
		return MS::kFailure;
	}
	int cnt = 1;
	if (p.isFlagSet("c"))
	{
		cnt = p.flagArgumentInt("c", 0);
	}

	apiutils::NNSearch nn = apiutils::NNSearch();
	MSelectionList slist = nn.getNearVerticesOnMesh(pnt, mesh, cnt);
	MGlobal::setActiveSelectionList(slist);
	
	return redoIt();
}

MStatus selectNearVertices::redoIt()
{
	

	return MS::kSuccess;
}

MStatus initializePlugin(MObject obj)
{
	std::cout.rdbuf(cerr.rdbuf());

	MStatus   status;
	MFnPlugin plugin(obj, "cygames", "1.0", "Any");

	status = plugin.registerCommand("selectNearVertices", selectNearVertices::creator);
	if (!status) {
		status.perror("registerCommand");
		return status;
	}

	status = plugin.registerCommand("findCloseUVsOnHardEdge", findCloseUVsOnHardEdge::creator);
	if (!status) {
		status.perror("registerCommand");
		return status;
	}

	status = plugin.registerCommand("findUvOverlappedFaces", findUvOverlappedFaces::creator);
	if (!status) {
		status.perror("registerCommand");
		return status;
	}

	return status;
}

MStatus uninitializePlugin(MObject obj)
{
	MStatus   status;
	MFnPlugin plugin(obj);

	status = plugin.deregisterCommand("selectNearVertices");
	if (!status) {
		status.perror("deregisterCommand");
		return status;
	}

	status = plugin.deregisterCommand("findCloseUVsOnHardEdge");
	if (!status) {
		status.perror("deregisterCommand");
		return status;
	}

	status = plugin.deregisterCommand("findUvOverlappedFaces");
	if (!status) {
		status.perror("deregisterCommand");
		return status;
	}

	return status;

}

std::ostream& operator<<(std::ostream& stream, const findUvOverlappedFaces::Face& face)
{
	stream << "center=" << face.center << " sqrad=" << face.radius << " hasUV=" << face.hasUV << endl;
	for (int i = 0;i < face.rays.size();i++)
	{
		stream << "  " << "origin=" << face.rays[i].origin << " dir=" << face.rays[i].dir << endl;
	}
	return stream;
}
