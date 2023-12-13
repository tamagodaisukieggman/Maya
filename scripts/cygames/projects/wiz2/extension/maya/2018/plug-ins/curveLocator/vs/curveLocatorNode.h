#ifndef _curveLocatorNode
#define _curveLocatorNode

#include <vector>

#include <maya/MPxLocatorNode.h>

#include <maya/MDrawRegistry.h>
#include <maya/MPxDrawOverride.h>
#include <maya/MUserData.h>
#include <maya/MDrawContext.h>
#include <maya/MHWGeometryUtilities.h>
#include <maya/MPointArray.h>
#include <maya/MGlobal.h>
#include <maya/MEventMessage.h>
#include <maya/MFnDependencyNode.h>

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h> 


#include <assert.h>

class curveLocator : public MPxLocatorNode
{
public:
	curveLocator();
	~curveLocator() override;

	MStatus   		compute(const MPlug& plug, MDataBlock& data) override;

	void            draw(M3dView & view, const MDagPath & path,
		M3dView::DisplayStyle style,
		M3dView::DisplayStatus status) override {};

	bool            isBounded() const override;
	MBoundingBox    boundingBox() const override;

	MStatus preEvaluation(const MDGContext& context, const MEvaluationNode& evaluationNode) override;

	static  void *          creator();
	static  MStatus         initialize();

	static	MObject			inputCurves;
	static	MObject			locatorTypeName;
	static	MObject			labelText;
	static	MObject			labelFontSize;
	static	MObject			labelOffsetX;
	static	MObject			labelOffsetY;

public:
	static	MTypeId		id;
	static	MString		drawDbClassification;
	static	MString		drawRegistrantId;

	static MObject      output;
};

class CurveLocatorData : public MUserData
{
public:
	CurveLocatorData(); // don't delete after draw
	~CurveLocatorData() override {}

	MColor fColor;
	unsigned int fDepthPriority;
	MPointArray fLineList;
	MPointArray fTriangleList;

	std::vector<MPointArray> curves;
	MPoint	pntMin;
	MPoint	pntMax;
	MString	label;
	unsigned fontSize;
	float labelOffsetX;
	float labelOffsetY;
	MFloatPoint wsoffset;
};

class CurveLocatorDrawOverride : public MHWRender::MPxDrawOverride
{
public:
	static MHWRender::MPxDrawOverride* Creator(const MObject& obj)
	{
		return new CurveLocatorDrawOverride(obj);
	}

	~CurveLocatorDrawOverride() override;

	MHWRender::DrawAPI supportedDrawAPIs() const override;

	bool isBounded(
		const MDagPath& objPath,
		const MDagPath& cameraPath) const override;

	MBoundingBox boundingBox(
		const MDagPath& objPath,
		const MDagPath& cameraPath) const override;

	MUserData* prepareForDraw(
		const MDagPath& objPath,
		const MDagPath& cameraPath,
		const MHWRender::MFrameContext& frameContext,
		MUserData* oldData) override;

	bool hasUIDrawables() const override { return true; }

	void addUIDrawables(
		const MDagPath& objPath,
		MHWRender::MUIDrawManager& drawManager,
		const MHWRender::MFrameContext& frameContext,
		const MUserData* data) override;

	MMatrix transform(const MDagPath &objPath, const MDagPath &cameraPath) const override
	{
		return MPxDrawOverride::transform(objPath, cameraPath);
	}

	bool  excludedFromPostEffects() const override
	{
		return true;
	}

	bool traceCallSequence() const override
	{
		return false;
	}
	void handleTraceMessage(const MString &message) const override
	{
		MGlobal::displayInfo("CurveLocatorDrawOverride: " + message);

		fputs("CurveLocatorDrawOverride: ", stderr);
		fputs(message.asChar(), stderr);
		fputs("\n", stderr);
	}


private:
	CurveLocatorDrawOverride(const MObject& obj);

	static void OnModelEditorChanged(void *clientData);

	curveLocator*  fCurveLocator;
	MCallbackId fModelEditorChangedCbId;

	MBoundingBox bbox;
};

#endif
