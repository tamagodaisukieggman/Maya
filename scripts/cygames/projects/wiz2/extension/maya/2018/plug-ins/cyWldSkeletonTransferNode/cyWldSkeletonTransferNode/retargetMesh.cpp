#include <time.h>

#include <maya/MGlobal.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MFnMesh.h.>
#include <maya/MFnMeshData.h>
#include <maya/MItMeshEdge.h>

#include "cyWldSkeletonTransferNode.h"


MObject cyWldSkeletonTransferNode::attachedInMeshPg;
MObject cyWldSkeletonTransferNode::attachedOutMeshPg;

class ThreadParams
{
public:
	ThreadParams(MFnMesh& _fnAtMesh) : fnAtMesh(_fnAtMesh) {}

	int id;
	int nThreads;
	int nv;
	int nIter;
	MPointArray* pnts;
	MFnMesh& fnAtMesh;
	apiutils::NNSearch* nn;
	cyWldSkeletonTransferNode* transferNode;
	int* progress;
	HANDLE* mutex;
};

int cyWldSkeletonTransferNode::progress(0);

DWORD WINAPI cyWldSkeletonTransferNode::ThreadFunc(LPVOID lpParam)
{
	ThreadParams* args = (ThreadParams*)lpParam;
	int smooth = 1;
	int dim = 3;
	char cmdstr[1024];

	int thid = args->id;
	int nThreads = args->nThreads;
	int nv = args->nv;
	int nIter = args->nIter;
	MFnMesh& fnAtMesh = args->fnAtMesh;
	MPointArray* pnts = args->pnts;
	apiutils::NNSearch* nn = args->nn;
	cyWldSkeletonTransferNode* transferNode = args->transferNode;
	//int* progress = args->progress;
	HANDLE* mutex = args->mutex;

	for (unsigned vertexId = thid;vertexId < nv;vertexId+=nThreads)
	{
		
		MPoint inpnt;
		fnAtMesh.getPoint(vertexId, inpnt, MSpace::kWorld); 


		MPoint res = MPoint::origin;
		double totaldist = 0;
		int nsearch = nIter * dim * smooth + 10;
		MIntArray candIds = nn->getNearVertexIndicesOnMesh(inpnt, nsearch);

		for (int iterid = 0;iterid < nIter;iterid++)
		{
			MPoint _res;
			double dist;
			
			MStatus stat = transferNode->calcACand(iterid, dim, smooth, candIds, inpnt, vertexId, _res, dist);
			if (stat == MS::kSuccess)
			{
				res += _res / dist;
				totaldist += 1.0 / dist;
			}
		}
		res = MPoint(res.x / totaldist, res.y / totaldist, res.z / totaldist);
		(*pnts)[vertexId] = res;
		
		
		//WaitForSingleObject(*mutex, 0);
		
		if (0 && thid == 0)
		{
			//int v = progress;
			//if (v > 50) v = 50;

			//progress+=20;
			//sprintf(cmdstr, "progressWindow -edit -progress %d", v);
			sprintf(cmdstr, "progressWindow -edit -progress %d", int(double(vertexId + 1) / nv * 100));
			MGlobal::executeCommand(cmdstr);
		}
		
		//ReleaseMutex(*mutex);
	}
	
	return 0;
}



MStatus cyWldSkeletonTransferNode::retargetMesh(const MPlug& plug, MDataBlock& data)
{
	MStatus stat;

	MArrayDataHandle outputArrayHandle = data.outputArrayValue(attachedOutMeshPg);
	MArrayDataHandle atmeshHandle = data.inputArrayValue(attachedInMeshPg, &stat);
	int dim = 3;
	//int smooth = data.inputValue(smoothPg).asInt();
	int smooth = 1;
	int nIter = data.inputValue(iterPg).asInt();

	for (int meshId = 0;meshId < atmeshHandle.elementCount();meshId++)
	{
		atmeshHandle.jumpToElement(meshId);
		MObject atmesh = atmeshHandle.inputValue().asMesh();
		MFnMesh fnAtMesh(atmesh);
		int nv = fnAtMesh.numVertices();

		srcCoords.resize(nv);
		dstCoords.resize(nv);
		inverseBases.resize(nv);
		comps.resize(nv);
		tweaks.resize(nv);
		
		MPointArray pnts;
		pnts.setLength(nv);

		char cmdstr[1024];
		
		DWORD threadId;
		int nThreads = 1;
		HANDLE* hThreads = new HANDLE[nThreads];
		int progress = 0;
		//HANDLE mutex = CreateMutex(NULL, TRUE, NULL);
		for (int i = 0;i < nThreads;i++)
		{
			ThreadParams args(fnAtMesh);
			args.id = i;
			args.nv = nv;
			args.nIter = nIter;
			args.pnts = &pnts;
			args.nn = &nn;
			args.transferNode = this;
			args.nThreads = nThreads;
			args.progress = &progress;
			//args.mutex = &mutex;

			//hThreads[i] = CreateThread(NULL, 0, ThreadFunc, &args, 0, &threadId);
			ThreadFunc(&args);
		}
		
		//WaitForMultipleObjects(nThreads, hThreads, TRUE, INFINITE);
		//for (int i = 0;i < nThreads;i++)
		//{
		//	CloseHandle(hThreads[i]);
		//}
		//delete(hThreads);

		MFnMeshData fnMeshData;
		MObject meshData = fnMeshData.create();
		MFnMesh fnOutMesh;
		MIntArray vertexCount;
		MIntArray vertexList;
		fnAtMesh.getVertices(vertexCount, vertexList);
		fnOutMesh.create(nv, fnAtMesh.numPolygons(), pnts, vertexCount, vertexList, meshData);

		for (int i=0;i<fnAtMesh.numEdges();i++)
		{
			int2 vlist;
			fnAtMesh.getEdgeVertices(i, vlist);
			int eindex = -1;
			for (int j = 0;j < fnOutMesh.numEdges();j++)
			{
				int2 vlist2;
				fnOutMesh.getEdgeVertices(j, vlist2);
				if (vlist[0] == vlist2[0] && vlist[1] == vlist2[1] || 
					vlist[0] == vlist2[1] && vlist[1] == vlist2[0])
				{
					eindex = j;
					break;
				}
			}
			if (eindex < 0)
			{
				sprintf(buf, "cannot found edge: %d", i);
				MGlobal::displayInfo(buf);
				continue;
			}

			bool sm = fnAtMesh.isEdgeSmooth(i);
			fnOutMesh.setEdgeSmoothing(eindex, sm);
		}

		

		outputArrayHandle.jumpToElement(meshId);
		outputArrayHandle.outputValue().setMObject(meshData);
	}

	outputArrayHandle.setAllClean();

	return MS::kSuccess;
}

