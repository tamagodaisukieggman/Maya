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


// Local functions.
//
bool buildBoundingCircle(MFnMesh& fnMesh, std::vector<findUvOverlappedFaces::Face>& faces)
{
	faces.clear();
	for (int i = 0;i < fnMesh.numPolygons();i++)
	{
		MIntArray vlist;
		MPoint cntr;
		bool hasUV = true;
		MPointArray uvs;
		int vcnt = fnMesh.polygonVertexCount(i);
		for (int j = 0;j < vcnt;j++)
		{
			float u, v;
			MStatus stat = fnMesh.getPolygonUV(i, j, u, v);
			if (stat != MS::kSuccess)
			{
				hasUV = false;
				break;
			}
			uvs.append(MPoint(u, v, 0));
			cntr += MVector(u, v, 0);
		}

		findUvOverlappedFaces::Face face;
		if (!hasUV)
		{
			face.hasUV = false;
			faces.push_back(face);
		}
		else
		{
			cntr = cntr / vcnt;
			float d2max = 0;
			MPoint prev = uvs[uvs.length() - 1];
			for (int j = 0;j < uvs.length();j++)
			{
				float d2 = pow(cntr.x - uvs[j].x, 2) + pow(cntr.y - uvs[j].y, 2);
				if (d2 > d2max)
				{
					d2max = d2;
				}
				findUvOverlappedFaces::Ray ray;
				ray.origin = uvs[j];
				ray.dir = prev - uvs[j];
				prev = uvs[j];

				face.rays.push_back(ray);
			}
			face.center = cntr;
			face.radius = sqrt(d2max);
			face.hasUV = true;
			faces.push_back(face);
		}
	}
	return true;
}

bool checkEdgeCrossing(const std::vector<findUvOverlappedFaces::Face>& faces, int f1, int f2)
{
	for (int i = 0;i < faces[f1].rays.size();i++)
	{
		const findUvOverlappedFaces::Ray& ray1 = faces[f1].rays[i];
		float o1x = ray1.origin.x;
		float o1y = ray1.origin.y;
		float v1x = ray1.dir.x;
		float v1y = ray1.dir.y;
		float n1x = v1y;
		float n1y = -v1x;

		for (int j = 0;j < faces[f2].rays.size();j++)
		{
			const findUvOverlappedFaces::Ray& ray2 = faces[f2].rays[j];
			float o2x = ray2.origin.x;
			float o2y = ray2.origin.y;
			float v2x = ray2.dir.x;
			float v2y = ray2.dir.y;
			float n2x = v2y;
			float n2y = -v2x;

			float denum = v2x * n1x + v2y * n1y;
			if (fabs(denum) < 0.000001) continue;
			float t2 = ((o1x - o2x)* n1x + (o1y - o2y) * n1y) / denum;
			if (t2 < 0.00001 || t2 > 0.99999) continue;

			denum = v1x * n2x + v1y * n2y;
			if (fabs(denum) < 0.000001) continue;
			float t1 = ((o2x - o1x)* n2x + (o2y - o1y) * n2y) / denum;
			if (t1 > 0.00001 && t1 < 0.99999) return true;
		}
	}
	return false;
}

bool checkInclusion(const std::vector<findUvOverlappedFaces::Face>& faces, int f1, int f2)
{
	if (!faces[f1].hasUV || !faces[f2].hasUV) return false;
	if (faces[f1].rays.size() == 0) return false;
	const MPoint& org = faces[f1].rays[0].origin;
	if (faces[f2].rays.size() < 3) return false;

	MPoint prev = faces[f2].rays[faces[f2].rays.size() - 1].origin;
	MVector prev_cp;
	for (int i = 0;i < faces[f2].rays.size();i++)
	{
		const MPoint& p = faces[f2].rays[i].origin;
		MVector cp = (prev - org) ^ (p - org);
		if (i > 0)
		{
			if (cp.angle(prev_cp) > 1.570796)
			{
				goto NOT_INCLUDED;
			}
		}
		prev_cp = cp;
		prev = p;

	}
	return true;

NOT_INCLUDED:
	return false;
}

void append(MIntArray& ar, int v)
{
	bool ex = false;
	for (int i = 0;i < ar.length();i++)
	{
		if (ar[i] == v)
		{
			ex = true;
			break;
		}
	}
	if (!ex) ar.append(v);
}

void findOverlapped(const std::vector<findUvOverlappedFaces::Face>& faces, MIntArray& res)
{
	for (int i = 0;i < faces.size();i++)
	{
		if (!faces[i].hasUV) continue;
		for (int j = i+1 ;j < faces.size();j++)
		{
			if (!faces[j].hasUV) continue;
			
			MVector v = faces[i].center - faces[j].center;
			float d2 = v.x * v.x + v.y * v.y;
			if (d2 >= pow(faces[i].radius + faces[j].radius, 2))
			{
				continue;
			}
			if (checkEdgeCrossing(faces, i, j) 
				|| checkInclusion(faces, i, j) || checkInclusion(faces, j, i))
			{
				append(res, i);
				append(res, j);
			}
		}
	}
}




findUvOverlappedFaces::findUvOverlappedFaces()
{
}

findUvOverlappedFaces::~findUvOverlappedFaces() {}

void* findUvOverlappedFaces::creator()
{
	return new findUvOverlappedFaces;
}

bool findUvOverlappedFaces::isUndoable() const
{
	return true;
}

MStatus findUvOverlappedFaces::undoIt()
{
	return MS::kSuccess;
}

MSyntax findUvOverlappedFaces::syntax()
{
	MSyntax s;
	s.addFlag("-m", "-mesh", MSyntax::kString);
	s.makeFlagMultiUse("m");
	return s;
}

MStatus findUvOverlappedFaces::doIt(const MArgList& args)
{
	MArgParser p(syntax(), args);
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

MStatus findUvOverlappedFaces::redoIt()
{


	return MS::kSuccess;
}


MStatus findUvOverlappedFaces::execute(MObjectArray &meshes)
{
	clearResult();
	for (int i = 0;i < meshes.length();i++)
	{
		procMesh(meshes[i]);
	}
	return MS::kSuccess;
}



MStatus findUvOverlappedFaces::procMesh(MObject mesh)
{
	MStatus stat;
	MFnMesh fnMesh(mesh, &stat);

	if (stat != MS::kSuccess)
	{
		return stat;
	}

	MStringArray results;
	buildBoundingCircle(fnMesh, faces);
	//for (int i = 0;i < faces.size();i++)
	//{
	//	cout << i << " " << faces[i] << endl;
	//}
	MIntArray res;
	findOverlapped(faces, res);
	char buf[256];
	for (int i = 0;i < res.length();i++)
	{
		sprintf(buf, "%s.f[%d]", fnMesh.partialPathName().asChar(), res[i]);
		results.append(buf);
	}
	
	appendToResult(results);
	

	return MS::kSuccess;
}


