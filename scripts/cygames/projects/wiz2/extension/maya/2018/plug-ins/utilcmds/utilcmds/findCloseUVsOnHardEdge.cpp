#include <maya/MStatus.h>
#include <maya/MArgList.h>
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
#include <maya/MItMeshEdge.h>

#include <maya/MIOStream.h>
#include <maya/MSyntax.h>
#include <maya/MArgParser.h>
#include <maya/MGlobal.h>
#include <maya/MFnMesh.h>
#include <maya/MDagPath.h>

#include <sstream>

#include "apiutils.h"
#include "utilcmds.h"


findCloseUVsOnHardEdge::findCloseUVsOnHardEdge()
{
}

findCloseUVsOnHardEdge::~findCloseUVsOnHardEdge() {}

void* findCloseUVsOnHardEdge::creator()
{
	return new findCloseUVsOnHardEdge;
}

bool findCloseUVsOnHardEdge::isUndoable() const
{
	return true;
}

MStatus findCloseUVsOnHardEdge::undoIt()
{
	return MS::kSuccess;
}

MSyntax findCloseUVsOnHardEdge::syntax()
{
	MSyntax s;
	//s.addFlag("-th", "-threshold", MSyntax::kDouble);
	s.addFlag("-ts", "-texsize", MSyntax::kDouble);
	s.addFlag("-p", "-pixel", MSyntax::kDouble);
	s.addFlag("-m", "-mesh", MSyntax::kString);
	s.makeFlagMultiUse("m");
	return s;
}

MStatus findCloseUVsOnHardEdge::doIt(const MArgList& args)
{
	MArgParser p(syntax(), args);
	if (p.isFlagSet("ts"))
	{
		texsize = p.flagArgumentDouble("ts", 0);
	}
	else
	{
		texsize = 1024;
	}
	if (p.isFlagSet("p"))
	{
		npixels = p.flagArgumentDouble("p", 0);
	}
	else
	{
		npixels = 16;
	}

	MObjectArray meshes;
	if (p.isFlagSet("m"))
	{
		for (int i = 0;i < p.numberOfFlagUses("m");i++)
		{
			MArgList alist;
			p.getFlagArgumentList("m", i, alist);
			MSelectionList slist;
			MStatus stat = MGlobal::getSelectionListByName(alist.asString(0), slist);
			if (stat == MS::kSuccess && slist.length() > 0)
			{
				MObject obj;
				slist.getDependNode(0, obj);
				meshes.append(obj);
			}
		}
	}
	else
	{
		MSelectionList slist;
		MGlobal::getActiveSelectionList(slist);
		for (int i = 0;i < slist.length();i++)
		{
			MObject obj;
			slist.getDependNode(i, obj);
			meshes.append(obj);
		}
	}
	if (meshes.length() == 0)
	{
		return MS::kFailure;
	}

	return execute(meshes);

}

MStatus findCloseUVsOnHardEdge::redoIt()
{


	return MS::kSuccess;
}


MStatus findCloseUVsOnHardEdge::execute(MObjectArray &meshes)
{
	clearResult();

	for (int i = 0;i < meshes.length();i++)
	{
		procMesh(meshes[i]);
	}
	return MS::kSuccess;
}

int findLocalVertexID(MFnMesh& fnMesh, int fid, MItMeshEdge& itEdge, int vindex)
{
	MIntArray g_vlist;
	fnMesh.getPolygonVertices(fid, g_vlist);
	for (int j = 0;j < g_vlist.length();j++)
	{
		if (vindex == g_vlist[j])
		{
			return j;
		}
	}
	return -1;
}

MStatus findCloseUVsOnHardEdge::procMesh(MObject mesh)
{
	MItMeshEdge itEdge(mesh);
	MStatus stat;
	MFnMesh fnMesh(mesh, &stat);

	if (stat != MS::kSuccess)
	{
		return stat;
	}

	float th = pow(npixels / texsize, 2);

	MStringArray results;
	for (;!itEdge.isDone();itEdge.next())
	{
		if (itEdge.isSmooth() || itEdge.onBoundary())
			continue;
		
		MIntArray faces;
		int nf = itEdge.getConnectedFaces(faces);
		if (nf != 2)
		{
			continue;
		}
		for (int i = 0;i < 2;i++)
		{
			MIntArray uvids(2);
			float2 uv[2];
			for (int j = 0;j < faces.length();j++)
			{
				int fid = faces[j];
				int local_vid = findLocalVertexID(fnMesh, fid, itEdge, itEdge.index(i));
				
				if (local_vid < 0)
				{
					goto LOCALID_NOTFOUND;
				}
				fnMesh.getPolygonUVid(fid, local_vid, uvids[j]);
				//printf("edge:%d_%d g_vindex:%d = face:%d uvid:%d\n", itEdge.index(), i, itEdge.index(i), fid, uvids[j]);
				fnMesh.getUV(uvids[j], uv[j][0], uv[j][1]);
				//printf("uv: %f %f\n", uv[j][0], uv[j][1]);
			}
			float d2 = pow(uv[0][0] - uv[1][0], 2) + pow(uv[0][1] - uv[1][1], 2);
			//printf("d2:%f th:%f\n", d2, th);
			if (d2 < th)
			{
				goto IRREGULAR_EDGE;
			}
		}
	CLEARED:
		continue;
	LOCALID_NOTFOUND:
		continue;
	IRREGULAR_EDGE:
		char buf[256];
		sprintf(buf, "%s.e[%d]", fnMesh.partialPathName().asChar(), itEdge.index());
		results.append(buf);
		continue;
	}
	appendToResult(results);
	

	return MS::kSuccess;
}
