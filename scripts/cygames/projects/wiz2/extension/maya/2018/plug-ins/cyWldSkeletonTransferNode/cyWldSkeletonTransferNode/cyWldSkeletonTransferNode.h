#ifndef _cyWldSkeletonTransferNodeNode
#define _cyWldSkeletonTransferNodeNode

#include <vector>
#include <sstream>
#include <time.h>



#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h>
#include <maya/MPointArray.h>
#include <maya/MIntArray.h>
#include <maya/MObjectArray.h>
#include <maya/MVectorArray.h>

#include <apiutils.h>

#include <Windows.h>

class cyWldSkeletonTransferNode : public MPxNode
{
public:
	static	MTypeId		id;
	
						cyWldSkeletonTransferNode();
	virtual				~cyWldSkeletonTransferNode(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );
	virtual bool		existWithoutOutConnections(MStatus *stat) const;
	

	static  void*		creator();
	static  MStatus		initialize();
	
	

private:
	static	int			progress;

	static  MObject		inJointMatrices;		
	static  MObject		outJointsPos;
	static	MObject		srcmeshPg;
	static	MObject		dstmeshPg;
	static	MObject		enablePg;
	static	MObject		matchModePg;
	static	MObject		verbouseLvPg;
	static	MObject		outSrcmeshPg;
	static	MObject		outDstmeshPg;
	static	MObject		outMatchModePg;

	static	MObject		attachedInMeshPg;
	static	MObject		attachedOutMeshPg;
	//static	MObject		smoothnessPg;
	//static	MObject		averagingPg;
	static	MObject		smoothPg;
	static	MObject		iterPg;

	char	buf[1024];

	std::stringstream	ss;
	apiutils::NNSearch	nn;
	std::vector<MVectorArray>	srcCoords;
	std::vector<MVectorArray>	dstCoords;
	std::vector<MDoubleArray>	tweaks;
	std::vector<MVectorArray>	inverseBases;
	std::vector<std::vector<double> > comps;
	
	std::vector<MIntArray>		corresponds;
	MPointArray					srcAllPnts;
	MPointArray					dstAllPnts;
	MObjectArray				srcmeshes;
	MObjectArray				dstmeshes;
	MIntArray					srcPntToObj;
	MIntArray					srcPntLocalId;
	MIntArray					dstPntLocalId;
	MIntArray					dstPntToObj;
	//MVectorArray				usedDirections;
	//MIntArray					numUsedDirections;

	int							verbouse;
	MPoint						getPolygonalOrigin(const MPointArray& mesh, const MIntArray& ids);
	MStatus						calcACand(int tryid, int dim, int smooth, MIntArray& neighbourIds, const MPoint& inpnt, int jntId, MPoint& output, double& dist);
	MStatus						retargetMesh(const MPlug& plug, MDataBlock& data);
	MStatus						sharedproc(const MPlug& plug, MDataBlock& data);
	MPoint						calcOriginForTarget(const std::vector<MIntArray>& actualIds);
	MPoint						getAverage(const MIntArray& ids);
	static DWORD WINAPI			ThreadFunc(LPVOID lpParam);
	
};







#endif
