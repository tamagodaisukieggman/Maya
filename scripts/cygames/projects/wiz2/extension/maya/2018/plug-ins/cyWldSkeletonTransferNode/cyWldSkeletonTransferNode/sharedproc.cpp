#include <time.h>
#include <maya/MGlobal.h>
#include <maya/MFnMesh.h>
#include "cyWldSkeletonTransferNode.h"



void setVariables(MArrayDataHandle& srcmeshData, MObjectArray& srcmeshes, MPointArray& srcAllPnts, MIntArray& srcPntToObj, MIntArray& srcPntLocalId)
{
	int n = srcmeshData.elementCount();
	int nv = 0;
	for (int i = 0;i < n;i++)
	{
		nv += MFnMesh(srcmeshData.inputValue().asMesh()).numVertices();
		srcmeshData.next();
	}

	srcmeshes.setLength(n);
	srcAllPnts.setLength(nv);
	srcPntToObj.setLength(nv);
	srcPntLocalId.setLength(nv);

	int cv = 0;
	srcmeshData.jumpToArrayElement(0);
	for (int i = 0;i<n;i++)
	{
		MObject mesh = srcmeshData.inputValue().asMesh();
		MFnMesh fnMesh(mesh);
		int index = srcmeshData.elementIndex();
		for (int j = 0;j < fnMesh.numVertices();j++)
		{
			MPoint p;
			fnMesh.getPoint(j, p, MSpace::kWorld);
			srcPntToObj[cv] = index;
			srcAllPnts[cv] = p;
			srcPntLocalId[cv] = j;
			cv++;
		}

		if (index >= srcmeshes.length())
		{
			srcmeshes.setLength(index + 1);
		}
		srcmeshes[index] = mesh;
		srcmeshData.next();
	}
}

MStatus cyWldSkeletonTransferNode::sharedproc(const MPlug& plug, MDataBlock& data)
{
	apiutils::resetElapsedTime("Start");
	MStatus stat;

	if (stat != MS::kSuccess) return MS::kFailure;
	MArrayDataHandle srcmeshData = data.inputArrayValue(srcmeshPg, &stat);
	if (stat != MS::kSuccess) return MS::kFailure;
	MArrayDataHandle dstmeshData = data.inputArrayValue(dstmeshPg, &stat);
	if (stat != MS::kSuccess) return MS::kFailure;
	if (srcmeshData.elementCount() == 0 || dstmeshData.elementCount() == 0)
	{
		return MS::kSuccess;
	}

	int verbouse = data.inputValue(verbouseLvPg).asInt();
	int _matchMode = data.inputValue(matchModePg).asInt();
	auto matchMode = static_cast<apiutils::MatchMode>(_matchMode);


	unsigned int outHandleIndex = 0;

	

	if (!data.isClean(outSrcmeshPg))
	{
		setVariables(srcmeshData, srcmeshes, srcAllPnts, srcPntToObj, srcPntLocalId);
		apiutils::elapsedTime("Finished setVariable.");
		nn.build(srcAllPnts);
		apiutils::elapsedTime("Finished building.");
	}

	if (!data.isClean(outDstmeshPg))
	{
		setVariables(dstmeshData, dstmeshes, dstAllPnts, dstPntToObj, dstPntLocalId);
		apiutils::elapsedTime("Finished setVariable.");
	}
	
	if (verbouse >= 1)
	{
		MGlobal::displayInfo(this->name());
	}

	
	if (corresponds.size() == 0
		|| (matchMode == apiutils::POSITION && (!data.isClean(outSrcmeshPg) || !data.isClean(outDstmeshPg)))
		|| !data.isClean(outMatchModePg)
		)
	{
		corresponds.clear();
		corresponds.resize(srcmeshes.length());
		for (int i = 0;i < srcmeshes.length();i++)
		{
			if (srcmeshes[i] == MObject::kNullObj)
			{
				continue;
			}
			if (i >= dstmeshes.length())
			{
				int n = MFnMesh(srcmeshes[i]).numVertices();
				corresponds[i].setLength(n);
			}
			else
			{
				if (dstmeshes[i] == MObject::kNullObj)
				{
					continue;
				}
				apiutils::computeCorrespondance(srcmeshes[i], dstmeshes[i], matchMode, corresponds[i]);
				apiutils::elapsedTime((MString("Finished correspondance for : ") + i).asChar());
			}
		}
	}

	apiutils::elapsedTime("Finished correspondance.");

	return MS::kSuccess;
}