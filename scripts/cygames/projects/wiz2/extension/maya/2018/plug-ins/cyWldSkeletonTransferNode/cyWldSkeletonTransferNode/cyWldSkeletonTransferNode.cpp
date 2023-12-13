#include "cyWldSkeletonTransferNode.h"

#include <sstream>
#include <time.h>

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MPoint.h>
#include <maya/MGlobal.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnSingleIndexedComponent.h>
#include <maya/MFnMesh.h>
#include <maya/MDagPath.h>
#include <maya/MMatrix.h>
#include <maya/MTransformationMatrix.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MItMeshVertex.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MQuaternion.h>

#include <maya/MFnMessageAttribute.h>

#include <Eigen/Dense>

MTypeId     cyWldSkeletonTransferNode::id( 0x12c040 );

MObject     cyWldSkeletonTransferNode::inJointMatrices;
MObject     cyWldSkeletonTransferNode::outJointsPos;   
MObject		cyWldSkeletonTransferNode::srcmeshPg;
MObject		cyWldSkeletonTransferNode::dstmeshPg;
MObject		cyWldSkeletonTransferNode::enablePg;
MObject		cyWldSkeletonTransferNode::verbouseLvPg;
MObject		cyWldSkeletonTransferNode::outSrcmeshPg;
MObject		cyWldSkeletonTransferNode::outDstmeshPg;
MObject		cyWldSkeletonTransferNode::matchModePg;
MObject		cyWldSkeletonTransferNode::outMatchModePg;
//MObject		cyWldSkeletonTransferNode::smoothnessPg;
//MObject		cyWldSkeletonTransferNode::averagingPg;
//MObject		cyWldSkeletonTransferNode::smoothPg;
MObject		cyWldSkeletonTransferNode::iterPg;
     

cyWldSkeletonTransferNode::cyWldSkeletonTransferNode() {}
cyWldSkeletonTransferNode::~cyWldSkeletonTransferNode() {}


MPoint cyWldSkeletonTransferNode::getPolygonalOrigin(const MPointArray& pnts, const MIntArray& ids)
{
	MPoint origin;
	for (int j = 0;j < ids.length();j++)
	{
		int index = ids[j];
		if (index >= pnts.length())
		{
			index = pnts.length() - 1;
		}
		origin += pnts[index];
	}
	origin = MPoint(origin.x / ids.length(), origin.y / ids.length(), origin.z / ids.length());
	return origin;
}

bool isPararell0(const MVector& v1, const MVector& v2)
{
	double cos = abs(v1.normal() * v2.normal());
	if (cos > 0.9)
	{
		return true;
	}
	else
	{
		return false;
	}
}


bool isValidAxis(const MVector& cand, const MVectorArray& srcCoord)
{
	if (srcCoord.length() != 2)
	{
		char buf[256];
		sprintf(buf, "srcCoord.length must be 2 here!!");
		MGlobal::displayInfo(buf);
		return false;
	}
	MVector ax = MVector(srcCoord[0]) ^ MVector(srcCoord[1]);
	ax.normalize();
	double v = abs(cand.normal() * ax.normal());
	if (v < 0.1)
	{
		//char buf[256];
		//sprintf(buf, "cand:%f %f %f  v=%f", cand.x, cand.y, cand.z, v);
		//MGlobal::displayInfo(buf);
		//for (int i = 0;i < 2;i++)
		//{
		//	sprintf(buf, "srcCoord[%d]=%f %f %f", i, srcCoord[i].x, srcCoord[i].y, srcCoord[i].z);
		//	MGlobal::displayInfo(buf);
		//}
		return false;
	}
	else {
		return true;
	}
}


double tweakAxis(MVector& cand, const MVectorArray& coords, double angle)
{
	MVector ax1 = MVector(coords[0]) ^ MVector(coords[1]);
	MVector ax2 = ax1 ^ cand;
	ax2.normalize();
	MQuaternion rot(angle, ax2);
	int nrot = 0;
	while (!isValidAxis(cand, coords))
	{
		cand = cand.rotateBy(rot);
		nrot++;
	}
	return angle * nrot;
}

void forceTweakAxis(MVector& v, const MVectorArray& coords, double angle)
{
	MVector ax1 = MVector(coords[0]) ^ MVector(coords[1]);
	MVector ax2 = ax1 ^ v;
	ax2.normalize();
	MQuaternion rot(angle, ax2);
	v = v.rotateBy(rot);
}

MPoint cyWldSkeletonTransferNode::getAverage(const MIntArray& ids)
{
	MPoint avp;
	int nav = 0;
	for (int j = 0;j < ids.length();j++)
	{
		int objid = srcPntToObj[ids[j]];
		int vid = srcPntLocalId[ids[j]];
		if (objid >= corresponds.size() || vid >= corresponds[objid].length())
		{
			sprintf(buf, "objid or vid is out of range.");
			MGlobal::displayInfo(buf);
			continue;
		}
		int tvid = corresponds[objid][vid];
		if (objid < dstmeshes.length())
		{
			MPoint p;
			MFnMesh(dstmeshes[objid]).getPoint(tvid, p, MSpace::kWorld);
			avp += p;
			nav++;
		}
	}
	if (nav == 0)
	{
		MGlobal::displayInfo("nav is zero.");
	}
	avp = avp / nav;
	return avp;
}

MPoint cyWldSkeletonTransferNode::calcOriginForTarget(const std::vector<MIntArray>& actualIds)
{
	MPoint origin;
	for (int i = 0;i < actualIds.size();i++)
	{
		origin += getAverage(actualIds[i]);
	}
	origin = origin / actualIds.size();
	return origin;
}

bool distantEnough(const MPoint cand, const MPointArray& pnts)
{
	for (int i = 0;i < pnts.length();i++)
	{
		const MPoint& p = pnts[i];
		if ((cand.x - p.x)*(cand.x - p.x) + (cand.y - p.y)*(cand.y - p.y) + (cand.z - p.z)*(cand.z - p.z) < 0.0001)
		{
			return false;
		}
	}
	return true;
}

MStatus cyWldSkeletonTransferNode::calcACand(int tryid, int dim, int smooth, MIntArray& neighbours, const MPoint& jntpos, int jntid, MPoint& output, double& dist)
{
	if (dim != 3)
	{
		MGlobal::displayInfo("Dimension must be 3.");
		return MS::kFailure;
	}

	char buf[1024];

	int verbouse = 0;
	int vindex = 5;

	int startid = tryid * dim;

	int nsuccess;
	MPointArray tmpar;
	std::vector<MIntArray> actualIds;
	int ntry = 0;
	while (true)
	{
		tmpar.clear();
		actualIds.clear();
		nsuccess = 0;
		for (int neighbourId = startid;neighbourId < neighbours.length();neighbourId++)
		{
			MPoint cand;
			MIntArray ids;
			int nc = 0;
			for (int i = 0;i < smooth;i++)
			{
				int _id = neighbourId + i * dim;
				if (_id >= neighbours.length())
				{
					continue;
				}
				int index = neighbours[_id];
				cand += srcAllPnts[index];
				nc++;
				ids.append(index);
			}
			if (nc == 0)
			{
				MGlobal::displayInfo(">> nc is zero.");
				return MS::kFailure;
			}
			cand = cand / nc;

			if (!distantEnough(cand, tmpar))
			{
				continue;
			}
			
			if (nsuccess == 1)
			{
				if ((neighbourId - startid) <= ntry)
				{
					continue;
				}
			}
			if (nsuccess == 2)
			{
				if (isPararell0(tmpar[0] - cand, tmpar[1] - cand))
				{
					continue;
				}
			}
			tmpar.append(cand);
			actualIds.push_back(ids);
			if (++nsuccess == dim) break;
		}
		if (nsuccess < 2 || nsuccess == dim)
		{
			break;
		}
		ntry++;
	}
	
	
	////////////////////////////////////////////// oooooooooooooooooooooooo
	

	if (nsuccess < dim)
	{
		sprintf(buf, "Failed to get axis for joint:%d", jntid);
		MGlobal::displayInfo(buf);
		return MS::kFailure;
	}


	MPoint origin(MPoint::origin);
	for (int i = 0;i < tmpar.length();i++)
	{
		origin += tmpar[i];
	}
	origin = origin / tmpar.length();


	
	////////////////////////////////////////////// oooooooooooooooooooooooo



	dist = origin.distanceTo(jntpos);

	srcCoords[jntid].clear();
	tweaks[jntid].clear();
	comps[jntid].clear();
	inverseBases[jntid].clear();
	dstCoords[jntid].clear();

	////////////////////////////////////////////// oooooooooooooooooooooooo
	

	for (int i = 0;i < actualIds.size();i++)
	{
		MVector cand = tmpar[i] - origin;

		if (i == 2)
		{
			double angle = tweakAxis(cand, srcCoords[jntid], 5.0*3.141592 / 180.0);
			//double angle = 0;///////////////////////////////////////////////////////////////
			if (angle > 0)
			{
				tweaks[jntid].append(angle);
			}
		}
		srcCoords[jntid].append(cand);
		if (tweaks[jntid].length() < srcCoords[jntid].length())
		{
			tweaks[jntid].append(0.0);
		}
	}
	
	//////////////////////////////////////////////////////// xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
	

	Eigen::MatrixXd m(3, dim);
	for (int c = 0;c < dim;c++)
	{
		for (int r = 0;r < 3;r++)
		{
			m(r, c) = srcCoords[jntid][c][r];
		}
	}
	m = m.inverse();
	
	for (int j = 0;j < dim;j++)
	{
		inverseBases[jntid].append(MVector(m(j, 0), m(j, 1), m(j, 2)));
		if (verbouse >= 1)
		{
			sprintf(buf, "inverseBase[%d]%d]=(%f, %f, %f)", jntid, j
				, inverseBases[jntid][j].x, inverseBases[jntid][j].y, inverseBases[jntid][j].z);
			MGlobal::displayInfo(buf);
		}
	}

	////////////////////////////////////////////////
	
	MPoint inpnt2 = jntpos - origin;
	//comps[jntid] = MPoint(inverseBases[jntid][0] * inpnt2, inverseBases[jntid][1] * inpnt2, inverseBases[jntid][2] * inpnt2);
	comps[jntid] = std::vector<double>();
	for (int i = 0;i < dim;i++)
	{
		comps[jntid].push_back(inverseBases[jntid][i] * inpnt2);
	}
	///////////////////////////////////////////// xxxxxxxxxxxxxxxxxxxx
	


	MPoint origin2 = calcOriginForTarget(actualIds);
	if (verbouse >= 1)
	{
		sprintf(buf, "origin:(%f, %f, %f) origin2=(%f, %f, %f)", origin.x, origin.y, origin.z, origin2.x, origin2.y, origin2.z);
		MGlobal::displayInfo(buf);
	}

	
	///////////////////////////////////////////// xxxxxxxxxxxxxxxxxxxx

	for (int i = 0;i < actualIds.size();i++)
	{
		MPoint p = getAverage(actualIds[i]);
		MVector coord = p - origin2;

		if (tweaks[jntid][i] > 0.0)
		{
			forceTweakAxis(coord, dstCoords[jntid], tweaks[jntid][i]);
		}
		dstCoords[jntid].append(coord);
	}

	

	if (dstCoords[jntid].length() != srcCoords[jntid].length())
	{
		MGlobal::displayInfo("dstCoords length doesn't match that of srcCoords.");
		return MS::kFailure;
	}

	MPoint res;
	for (int j = 0;j < dstCoords[jntid].length();j++)
	{
		res += comps[jntid][j] * dstCoords[jntid][j];
		if (verbouse >= 1)
		{
			sprintf(buf, "comps[%d][%d]=%f  dstCoords[%d][%d]=(%f, %f, %f)", jntid, j, comps[jntid][j], jntid, j
				, dstCoords[jntid][j].x, dstCoords[jntid][j].y, dstCoords[jntid][j].z);
			MGlobal::displayInfo(buf);
		}
	}
	res += origin2;
	output = res;

	return MS::kSuccess;
	
}



MStatus cyWldSkeletonTransferNode::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus stat;
	MSelectionList tlist;

	bool enabled = data.inputValue(enablePg).asBool();
	if (!enabled)
	{
		return MS::kSuccess;
	}

	char cmdstr[1024];

	verbouse = data.inputValue(verbouseLvPg).asInt();

	if( plug == outJointsPos )
	{
		
		sharedproc(plug, data);
		

		MArrayDataHandle outputArrayHandle = data.outputArrayValue(outJointsPos);
		MArrayDataHandle inJointMatricesData = data.inputArrayValue(inJointMatrices, &stat);

		int nj = inJointMatricesData.elementCount();
		srcCoords.resize(nj);
		dstCoords.resize(nj);
		inverseBases.resize(nj);
		comps.resize(nj);
		tweaks.resize(nj);

		MDataHandle tmpHandle;
		int nIters = data.inputValue(iterPg).asInt();
		int smooth = 1;
		int dim = 3;

		for (unsigned jntId = 0;jntId < nj;jntId++)
		{
			outputArrayHandle.jumpToElement(jntId);
			tmpHandle = outputArrayHandle.outputValue();
			

			inJointMatricesData.jumpToElement(jntId);
			MMatrix jntMat = inJointMatricesData.inputValue().asMatrix();
			MTransformationMatrix tmat(jntMat);
			MPoint inpnt = tmat.getTranslation(MSpace::kWorld);

			
			int nsc = 0;
			MPoint res = MPoint::origin;
			double totaldist = 0;

			
			int nsearch = nIters * dim * smooth + 10;
			MIntArray candIds = nn.getNearVertexIndicesOnMesh(inpnt, nsearch);


			for (int iterid = 0;iterid < nIters;iterid++)
			{
				MPoint _res;
				double dist;
				MStatus stat = calcACand(iterid, dim, smooth, candIds, inpnt, jntId, _res, dist);
				if (stat == MS::kSuccess)
				{
					nsc++;
					res += _res / dist;
					totaldist += 1.0 / dist;
				}
			}
			res = MPoint(res.x / totaldist, res.y / totaldist, res.z / totaldist);
			tmpHandle.set3Double(res.x, res.y, res.z);
		}
		outputArrayHandle.setAllClean();
		data.outputValue(outSrcmeshPg).setClean();
		data.outputValue(outDstmeshPg).setClean();

		
		
	} else if(plug == attachedOutMeshPg) {
		
		//sprintf(cmdstr, "progressWindow -title \"%s\" -progress 0", "Retarget");
		//MGlobal::executeCommand(cmdstr);

		sharedproc(plug, data);
		retargetMesh(plug, data);
		//MGlobal::executeCommand("progressWindow -endProgress");
	} else {
		return MS::kUnknownParameter;
	}

	
	apiutils::elapsedTime("Retarget Done.");
	
	return MS::kSuccess;
}










void* cyWldSkeletonTransferNode::creator()
{
	return new cyWldSkeletonTransferNode();
}

bool cyWldSkeletonTransferNode::existWithoutOutConnections(MStatus *stat) const
{
	return false;
}


MStatus cyWldSkeletonTransferNode::initialize()
{
	MStatus				stat;

	MFnNumericAttribute nAttr;
	MFnMatrixAttribute mAttr;
	MFnTypedAttribute tAttr;
	
	MFnEnumAttribute enAttr;
	MFnMessageAttribute msAttr;

	inJointMatrices = mAttr.create("inJointsPos", "injnts");
	mAttr.setStorable(true);
	mAttr.setKeyable(true);
	mAttr.setWritable(true);
	mAttr.setArray(true);
	mAttr.setIndexMatters(false);
	mAttr.setHidden(true);


	outJointsPos = nAttr.create("outJointsPos", "outjnts", MFnNumericData::k3Double);
	nAttr.setReadable(true);
	nAttr.setWritable(false);
	//nAttr.setStorable(false);
	nAttr.setArray(true);
	//nAttr.setUsesArrayDataBuilder(true);

	srcmeshPg = tAttr.create("srcMesh", "src", MFnData::kMesh);
	tAttr.setWritable(true);
	tAttr.setStorable(false);
	tAttr.setArray(true);
	tAttr.setIndexMatters(false);

	dstmeshPg = tAttr.create("dstMesh", "dst", MFnData::kMesh);
	tAttr.setWritable(true);
	tAttr.setStorable(false);
	tAttr.setArray(true);
	tAttr.setIndexMatters(false);

	enablePg = nAttr.create("enable", "en", MFnNumericData::kBoolean);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);

	verbouseLvPg = nAttr.create("verbousLevel", "vl", MFnNumericData::kInt, 0);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);



	matchModePg = enAttr.create("matchMode", "mm", 2);
	enAttr.addField("position", 0);
	enAttr.addField("vertexid", 1);
	enAttr.addField("uv", 2);
	enAttr.setWritable(true);
	enAttr.setStorable(true);
	enAttr.setKeyable(true);

	outSrcmeshPg = msAttr.create("outSrcmesh", "outsrc");
	outDstmeshPg = msAttr.create("outDstmesh", "outdst");
	outMatchModePg = msAttr.create("outMatchMode", "outmm");

	attachedInMeshPg = tAttr.create("attachedInMesh", "atchIn", MFnData::kMesh);
	tAttr.setWritable(true);
	tAttr.setStorable(false);
	tAttr.setArray(true);
	tAttr.setIndexMatters(false);

	attachedOutMeshPg = tAttr.create("attachedOutMesh", "atchOut", MFnData::kMesh);
	tAttr.setWritable(true);
	tAttr.setStorable(false);
	tAttr.setArray(true);
	tAttr.setIndexMatters(false);
	/*
	smoothnessPg = nAttr.create("smoothness", "sm", MFnNumericData::kInt, 1);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	nAttr.setMin(1);
	nAttr.setMax(4);

	averagingPg = nAttr.create("averaging", "av", MFnNumericData::kInt, 10);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	nAttr.setMin(0);
	*/
	//smoothPg = nAttr.create("smoothness", "sm", MFnNumericData::kInt, 1);
	//nAttr.setWritable(true);
	//nAttr.setStorable(true);
	//nAttr.setKeyable(true);
	//nAttr.setMin(1);

	iterPg = nAttr.create("iteration", "iter", MFnNumericData::kInt, 1);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	nAttr.setMin(1);


	stat = addAttribute( inJointMatrices );
	if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( outJointsPos );
	if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute(srcmeshPg);
	if (!stat) { stat.perror("addAttribute");return stat; }
	stat = addAttribute(dstmeshPg);
	if (!stat) { stat.perror("addAttribute");return stat; }
	stat == addAttribute(enablePg);
	if (!stat) { stat.perror("addAttribute");return stat; }
	stat == addAttribute(verbouseLvPg);
	if (!stat) { stat.perror("addAttribute");return stat; }
	stat == addAttribute(matchModePg);
	if (!stat) { stat.perror("addAttribute");return stat; }
	stat == addAttribute(outSrcmeshPg);
	if (!stat) { stat.perror("addAttribute");return stat; }
	stat == addAttribute(outDstmeshPg);
	if (!stat) { stat.perror("addAttribute");return stat; }
	stat == addAttribute(outMatchModePg);
	if (!stat) { stat.perror("addAttribute");return stat; }
	stat == addAttribute(attachedInMeshPg);
	if (!stat) { stat.perror("addAttribute");return stat; }
	stat == addAttribute(attachedOutMeshPg);
	if (!stat) { stat.perror("addAttribute");return stat; }
	//stat == addAttribute(smoothnessPg);
	//if (!stat) { stat.perror("addAttribute");return stat; }
	//stat == addAttribute(averagingPg);
	//if (!stat) { stat.perror("addAttribute");return stat; }
	//stat == addAttribute(smoothPg);
	//if (!stat) { stat.perror("addAttribute");return stat; }
	stat == addAttribute(iterPg);
	if (!stat) { stat.perror("addAttribute");return stat; }

	stat = attributeAffects( inJointMatrices, outJointsPos );
	if (!stat) { stat.perror("attributeAffects"); return stat;}
	stat = attributeAffects(srcmeshPg, outJointsPos);
	if (!stat) { stat.perror("attributeAffects"); return stat; }
	stat = attributeAffects(srcmeshPg, outSrcmeshPg);
	if (!stat) { stat.perror("attributeAffects"); return stat; }
	stat = attributeAffects(dstmeshPg, outJointsPos);
	if (!stat) { stat.perror("attributeAffects"); return stat; }
	stat = attributeAffects(dstmeshPg, outDstmeshPg);
	if (!stat) { stat.perror("attributeAffects"); return stat; }
	stat = attributeAffects(enablePg, outJointsPos);
	if (!stat) { stat.perror("attributeAffects"); return stat; }
	stat = attributeAffects(matchModePg, outJointsPos);
	if (!stat) { stat.perror("attributeAffects"); return stat; }
	stat = attributeAffects(matchModePg, outMatchModePg);
	if (!stat) { stat.perror("attributeAffects"); return stat; }

	stat = attributeAffects(attachedInMeshPg, attachedOutMeshPg);
	if (!stat) { stat.perror("attributeAffects"); return stat; }
	stat = attributeAffects(inJointMatrices, attachedOutMeshPg);
	if (!stat) { stat.perror("attributeAffects"); return stat; }
	stat = attributeAffects(srcmeshPg, attachedOutMeshPg);
	if (!stat) { stat.perror("attributeAffects"); return stat; }
	stat = attributeAffects(dstmeshPg, attachedOutMeshPg);
	if (!stat) { stat.perror("attributeAffects"); return stat; }
	stat = attributeAffects(enablePg, attachedOutMeshPg);
	if (!stat) { stat.perror("attributeAffects"); return stat; }
	stat = attributeAffects(matchModePg, attachedOutMeshPg);
	if (!stat) { stat.perror("attributeAffects"); return stat; }

	//stat = attributeAffects(smoothPg, outJointsPos);
	//stat = attributeAffects(smoothPg, attachedOutMeshPg);
	stat = attributeAffects(iterPg, outJointsPos);
	stat = attributeAffects(iterPg, attachedOutMeshPg);



	return MS::kSuccess;

}

