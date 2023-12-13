//
// Copyright (C) cygames
// 
// File: apiutilsCmd.cpp
//
// MEL Command: apiutils
//
// Author: Maya Plug-in Wizard 2.0
//

#include <vector>
#include <time.h>

#include <maya/MIntArray.h>
#include <maya/MItMeshVertex.h>
#include <maya/MGlobal.h>
#include <maya/MDagPath.h>
#include <maya/MFnMesh.h>
#include <maya/MPointArray.h>
#include <maya/MPoint.h>
#include <maya/MItMeshFaceVertex.h>



#include "apiutils.h"



namespace apiutils
{
	

	NNSearch::NNSearch() : scaleFactor(1000)
	{
	}

	NNSearch::~NNSearch()
	{
		delete nn;
	}

	void NNSearch::build(MPointArray& pnts)
	{
		delete nn;
		
		std::vector<IntPoint3d> _pnts;
		_pnts.reserve(pnts.length());
		for (int i = 0;i < pnts.length();i++)
		{
			_pnts.push_back(IntPoint3d(pnts[i].x * scaleFactor, pnts[i].y * scaleFactor, pnts[i].z * scaleFactor));
		}
		
		//nn = new sfcnn < MPoint, 3, double>(&pnts[0], pnts.length(), 4);
		nn = new sfcnn <IntPoint3d, 3, int>(&_pnts[0], pnts.length(), 4);
		cnt = pnts.length();
	}

	MSelectionList NNSearch::getNearVerticesOnMesh(MPoint pnt, MObject mesh, int cnt)
	{

		MStatus stat;
		MSelectionList res;

		MDagPath path;
		MDagPath::getAPathTo(mesh, path);

		MFnMesh fnMesh(mesh, &stat);
		if (stat != MS::kSuccess)
		{
			return res;
		}

		MPointArray pa;
		for (int i = 0;i < fnMesh.numVertices();i++)
		{
			MPoint p;
			fnMesh.getPoint(i, p);
			pa.append(p);
		}
		sfcnn < MPoint, 3, double> nn(&pa[0], pa.length());

		std::vector<long unsigned int> answer;
		nn.ksearch(pnt, cnt, answer);

		MObjectArray comps;
		MItMeshVertex itVert(mesh);
		for (auto itr = answer.begin();itr != answer.end(); ++itr)
		{
			int prev;
			int vertexid = *itr;

			stat = itVert.setIndex(*itr, prev);
			//itVert.currentItem(&stat);
			stat = stat;
			MGlobal::displayInfo("path:" + path.fullPathName());
			MStatus st = res.add(path, itVert.currentItem());
			MGlobal::displayInfo("st:" + st.errorString());
			//MStatus st = res.add(itVert.currentItem());
			int j = 0;
		}
		int l = res.length();

		return res;

	}

	MIntArray NNSearch::getNearVertexIndicesOnMesh(MPoint pnt, int _cnt)
	{
		MIntArray res;
		std::vector<long unsigned int> answer;
		IntPoint3d _pnt(pnt.x*scaleFactor, pnt.y*scaleFactor, pnt.z*scaleFactor);
		nn->ksearch(_pnt, std::min(_cnt, cnt), answer);

		MObjectArray comps;
		MItMeshVertex itVert(mesh);
		for (auto itr = answer.begin();itr != answer.end(); ++itr)
		{
			int vertexid = *itr;
			res.append(vertexid);

		}

		return res;

	}

	int getVertexIdFromUvId(MObject& mesh, int uvid)
	{

		MItMeshVertex itVert(mesh);
		bool has = false;
		int vid = -1;
		for (; !itVert.isDone(); itVert.next())
		{
			MIntArray uvs;
			itVert.getUVIndices(uvs);
			for (int j = 0;j < uvs.length();j++)
			{
				//char buf[256];
				//sprintf(buf, "inputUVid=%d --> vertid=%d uv[%d]=%d", uvid, itVert.index(), j, uvs[j]);
				//MGlobal::displayInfo(buf);
				if (uvs[j] == uvid)
				{
					has = true;
					vid = itVert.index();
					break;
				}
			}
			if (has)
			{
				break;
			}
		}
		return vid;
	}

	clock_t elp = 0;
	void resetElapsedTime(const char *mes)
	{
		elp = 0;
		MGlobal::displayInfo(mes);
	}
	void elapsedTime(const char *mes)
	{
		if (elp == 0)
		{
			MGlobal::displayInfo(mes);
			elp = clock();
			return;
		}
		clock_t now = clock();
		char buf[256];
		sprintf(buf, "%s >> elapsedTime:%f (sec)", mes, (double)(now - elp) / CLOCKS_PER_SEC);
		MGlobal::displayInfo(buf);
		elp = now;
	}

	void computeCorrespondance(MObject& src, MObject& dst, MatchMode matchMode, MIntArray& res)
	{
		MFnMesh fnSrc(src);
		MFnMesh fnDst(dst);
		res.setLength(fnSrc.numVertices());

		if (matchMode == MatchMode::VERTEXID)
		{
			int  ndst = fnDst.numVertices();
			for (int i = 0;i < res.length();i++)
			{
				if (i >= ndst)
				{
					res[i] = 0;
				}
				else
				{
					res[i] = i;
				}
			}
		}
		
		else
		{
			if (matchMode == MatchMode::UV)
			{
				//elapsedTime("UV match start.");
				MFloatArray ua, va, ua2, va2;
				fnSrc.getUVs(ua, va);
				MFnMesh fnDst(dst);
				fnDst.getUVs(ua2, va2);

				int sf = 1000;

				
				std::vector<IntPoint2d> dstvs;
				for (int i = 0;i < fnDst.numUVs();i++)
				{
					if (i >= ua2.length() || i >= va2.length())
					{
						break;
					}
					IntPoint2d v(ua2[i] * sf, va2[i] * sf);
					dstvs.push_back(v);
				}
				//elapsedTime("Building UV nn...");
				sfcnn<IntPoint2d, 2, int> nn(&dstvs[0], dstvs.size(), 4); // 3rd arg is nThreads.
				//elapsedTime("Finished UV nn.");
				std::vector<int> uv2vid;
				uv2vid.resize(fnSrc.numUVs(), 0);
				for (int i = 0;i < fnSrc.numPolygons();i++)
				{
					MIntArray vlist;
					fnSrc.getPolygonVertices(i, vlist);
					for (int j = 0;j < vlist.length();j++)
					{
						int uvid;
						fnSrc.getPolygonUVid(i, j, uvid);
						uv2vid[uvid] = vlist[j];
					}
				}

				std::vector<int> uv2vidTgt;
				uv2vidTgt.resize(fnDst.numUVs(), 0);
				for (int i = 0;i < fnDst.numPolygons();i++)
				{
					MIntArray vlist;
					fnDst.getPolygonVertices(i, vlist);
					for (int j = 0;j < vlist.length();j++)
					{
						int uvid;
						fnDst.getPolygonUVid(i, j, uvid);
						uv2vidTgt[uvid] = vlist[j];
					}
				}

				//elapsedTime("ksearch start.");

				for (int uvid = 0;uvid < ua.length();uvid++)
				{
					std::vector<unsigned long> idx;
					IntPoint2d pnt(ua[uvid] * sf, va[uvid] * sf);
					nn.ksearch(pnt, 1, idx);
					int vid = uv2vid[uvid];

					if (vid < 0)
					{
						continue;
					}
					int tid = -1;
					if (idx.size() > 0)
					{
						tid = uv2vidTgt[idx[0]];
					}
					if (tid < 0)
					{
						continue;
					}
					res[vid] = tid;

				}
				//elapsedTime("ksearch done.");
			}
			else if (matchMode == MatchMode::POSITION)
			{
				MFnMesh fnDst(dst);
				std::vector<MPoint> dstvs;
				for (int i = 0;i < fnDst.numVertices();i++)
				{
					MPoint p;
					fnDst.getPoint(i, p);
					dstvs.push_back(p);
				}
				sfcnn<MPoint, 3, double> nn(&dstvs[0], dstvs.size());
				for (int i = 0;i < fnSrc.numVertices();i++)
				{
					MPoint p;
					fnSrc.getPoint(i, p);
					std::vector<unsigned long> idx;
					nn.ksearch(p, 1, idx);
					if (idx.size() > 0)
					{
						res[i] = idx[0];
					}

				}
			}
		}
	}
	
}