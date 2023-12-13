#include <maya/MFnTypedAttribute.h>

#include <maya/MString.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MVector.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MColor.h>
#include <maya/M3dView.h>

#include <maya/MDistance.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MEvaluationNode.h>
#include <maya/MFnNurbsCurveData.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnCamera.h>
#include <maya/MFloatMatrix.h>
#include <maya/MFnTransform.h>

#include "curveLocatorNode.h"


MBoundingBox getBoundingBox(const MDagPath& objPath)
{
	MStatus status;
	MObject curveLocatorNode = objPath.node(&status);
	MBoundingBox bbox;
	MPoint pntMin, pntMax;
	if (status)
	{
		MPlug plug(curveLocatorNode, curveLocator::inputCurves);
		if (!plug.isNull())
		{
			for (unsigned i = 0; i < plug.numElements(); i++)
			{
				MObject crv;
				status = plug[i].getValue(crv);
				if (status != MS::kSuccess)
				{
					continue;
				}
				MFnNurbsCurve fncrv(crv);
				MPointArray pnts;
				fncrv.getCVs(pnts, MSpace::kWorld);

				MPointArray lines;
				for (unsigned j = 0; j < (pnts.length() - 1); j++)
				{
					if (i == 0 && j == 0)
					{
						pntMin = pnts[j];
						pntMax = pnts[j];
					}
					else {
						for (unsigned k = 0; k < 3; k++) {
							if (pnts[j][k] < pntMin[k])
							{
								pntMin[k] = pnts[j][k];
							}
							else if (pnts[j][k] > pntMax[k])
							{
								pntMax[k] = pnts[j][k];
							}
						}
					}
					lines.append(pnts[j]);
					lines.append(pnts[j + 1]);
				}

			}

			bbox = MBoundingBox(pntMin, pntMax);
		}
	}


	return bbox;
}

MTypeId curveLocator::id(0x80007);
MString	curveLocator::drawDbClassification("drawdb/geometry/curveLocator");
MString	curveLocator::drawRegistrantId("CurveLocatorNodePlugin");
MObject curveLocator::output;
MObject curveLocator::inputCurves;
MObject curveLocator::locatorTypeName;
MObject curveLocator::labelText;
MObject curveLocator::labelFontSize;
MObject curveLocator::labelOffsetX;
MObject curveLocator::labelOffsetY;


curveLocator::curveLocator() {}
curveLocator::~curveLocator() {}

MStatus curveLocator::compute(const MPlug& plug/*plug*/, MDataBlock& dataBlock/*data*/)
{
	MStatus s;
	if (plug == output)
	{
		if (plug.isElement())
		{
			MArrayDataHandle outputArrayHandle = dataBlock.outputArrayValue(output);
			outputArrayHandle.setAllClean();
		}

		dataBlock.setClean(plug);

		return MS::kSuccess;
	}

	return MS::kUnknownParameter;;
}


bool curveLocator::isBounded() const
{
	return true;
}

MBoundingBox curveLocator::boundingBox() const
{
	MObject thisNode = thisMObject();
	MDagPath objPath = MDagPath::getAPathTo(thisNode);

	return getBoundingBox(objPath);

}

MStatus curveLocator::preEvaluation(
	const MDGContext& context,
	const MEvaluationNode& evaluationNode)
{
	if (context.isNormal())
	{
		MStatus status;
		if (evaluationNode.dirtyPlugExists(inputCurves, &status) && status)
		{
			MHWRender::MRenderer::setGeometryDrawDirty(thisMObject());
		}
	}

	return MStatus::kSuccess;
}

void* curveLocator::creator()
{
	return new curveLocator();
}


CurveLocatorData::CurveLocatorData() : MUserData(false) 
{
	curves = std::vector<MPointArray>();
}

CurveLocatorDrawOverride::CurveLocatorDrawOverride(const MObject& obj)
	: MHWRender::MPxDrawOverride(obj, NULL, false)
{
	fModelEditorChangedCbId = MEventMessage::addEventCallback(
		"modelEditorChanged", OnModelEditorChanged, this);

	MStatus status;
	MFnDependencyNode node(obj, &status);
	fCurveLocator = status ? dynamic_cast<curveLocator*>(node.userNode()) : NULL;
}

CurveLocatorDrawOverride::~CurveLocatorDrawOverride()
{
	fCurveLocator = NULL;

	if (fModelEditorChangedCbId != 0)
	{
		MMessage::removeCallback(fModelEditorChangedCbId);
		fModelEditorChangedCbId = 0;
	}
}

void CurveLocatorDrawOverride::OnModelEditorChanged(void *clientData)
{
	CurveLocatorDrawOverride *ovr = static_cast<CurveLocatorDrawOverride*>(clientData);
	if (ovr && ovr->fCurveLocator)
	{
		MHWRender::MRenderer::setGeometryDrawDirty(ovr->fCurveLocator->thisMObject());
	}
}

MHWRender::DrawAPI CurveLocatorDrawOverride::supportedDrawAPIs() const
{
	// this plugin supports both GL and DX
	return (MHWRender::kOpenGL | MHWRender::kDirectX11 | MHWRender::kOpenGLCoreProfile);
}

bool CurveLocatorDrawOverride::isBounded(const MDagPath& /*objPath*/,
	const MDagPath& /*cameraPath*/) const
{
	return true;
}



MBoundingBox CurveLocatorDrawOverride::boundingBox(
	const MDagPath& objPath,
	const MDagPath& cameraPath) const
{
	return getBoundingBox(objPath);
}

MUserData* CurveLocatorDrawOverride::prepareForDraw(
	const MDagPath& objPath,
	const MDagPath& cameraPath,
	const MHWRender::MFrameContext& frameContext,
	MUserData* oldData)
{
	CurveLocatorData* data = dynamic_cast<CurveLocatorData*>(oldData);
	if (!data)
	{
		data = new CurveLocatorData();
	}

	data->curves.clear();
	
	MStatus status;
	MObject curveLocatorNode = objPath.node(&status);

	if (status)
	{
		MPlug plug(curveLocatorNode, curveLocator::inputCurves);
		if (!plug.isNull())
		{
			for (unsigned i = 0; i < plug.numElements(); i++)
			{
				MObject crv;
				status = plug[i].getValue(crv);
				if (status != MS::kSuccess) 
				{
					continue;
				}
				MFnNurbsCurve fncrv(crv);
				MPointArray pnts;
				fncrv.getCVs(pnts, MSpace::kWorld);

				MPointArray lines;
				for (unsigned j = 0; j < (pnts.length()-1); j++)
				{
					if (i == 0 && j == 0)
					{
						data->pntMin = pnts[j];
						data->pntMax = pnts[j];
					}
					else {
						for (unsigned k = 0; k < 3; k++) {
							if (pnts[j][k] < data->pntMin[k])
							{
								data->pntMin[k] = pnts[j][k];
							}
							else if (pnts[j][k] > data->pntMax[k])
							{
								data->pntMax[k] = pnts[j][k];
							}
						}
					}
					lines.append(pnts[j]);
					lines.append(pnts[j + 1]);
				}

				data->curves.push_back(lines);
			}

			bbox = MBoundingBox(data->pntMin, data->pntMax);
		}

		plug.setAttribute(curveLocator::labelText);
		if (!plug.isNull())
		{
			MString label;
			plug.getValue(label);
			data->label = label;
		}

		plug.setAttribute(curveLocator::labelFontSize);
		if (!plug.isNull())
		{
			int size;
			plug.getValue(size);
			data->fontSize = size;
		}

		float offsetx, offsety;
		plug.setAttribute(curveLocator::labelOffsetX);
		plug.getValue(offsetx);
		plug.setAttribute(curveLocator::labelOffsetY);
		plug.getValue(offsety);
		
		MFnTransform fncamtr(cameraPath.transform());
		MPoint offset(offsetx, offsety, 0);
		data->wsoffset = fncamtr.transformationMatrix().inverse() * offset;

	}
	else {
		return NULL;
	}

	data->fColor = MHWRender::MGeometryUtilities::wireframeColor(objPath);
	switch (MHWRender::MGeometryUtilities::displayStatus(objPath))
	{
	case MHWRender::kLead:
	case MHWRender::kActive:
	case MHWRender::kHilite:
	case MHWRender::kActiveComponent:
		data->fDepthPriority = MHWRender::MRenderItem::sActiveWireDepthPriority;
		break;
	default:
		data->fDepthPriority = MHWRender::MRenderItem::sDormantFilledDepthPriority;
		break;
	}
	
	return data;
}

void CurveLocatorDrawOverride::addUIDrawables(
	const MDagPath& objPath,
	MHWRender::MUIDrawManager& drawManager,
	const MHWRender::MFrameContext& frameContext,
	const MUserData* data)
{
	CurveLocatorData* pLocatorData = (CurveLocatorData*)data;
	if (!pLocatorData)
	{
		return;
	}

	drawManager.beginDrawable();

	drawManager.setColor(pLocatorData->fColor);
	drawManager.setDepthPriority(pLocatorData->fDepthPriority);

	for (unsigned i = 0; i < pLocatorData->curves.size(); i++)
	{
		drawManager.mesh(MHWRender::MUIDrawManager::kLines, pLocatorData->curves[i]);
	}

	MColor textColor(pLocatorData->fColor);

	drawManager.setColor(textColor);
	drawManager.setFontSize(pLocatorData->fontSize);
	
	drawManager.text(pLocatorData->wsoffset, pLocatorData->label, MHWRender::MUIDrawManager::kCenter);

	drawManager.endDrawable();
}


MStatus curveLocator::initialize()
{
	MFnTypedAttribute   typedAttr;
	MFnUnitAttribute unitFn;
	MFnNumericAttribute numAttr;
	MStatus			 stat;

	output = unitFn.create("output", "out", MFnUnitAttribute::kDistance, 1.0);
	unitFn.setWritable(true);
	unitFn.setCached(false);
	unitFn.setArray(true);
	unitFn.setUsesArrayDataBuilder(true);
	unitFn.setWorldSpace(true);

	addAttribute(output);

	inputCurves = typedAttr.create("inputCurves", "crvs", MFnNurbsCurveData::kNurbsCurve, &stat);
	typedAttr.setArray(true);
	addAttribute(inputCurves);
	

	locatorTypeName = typedAttr.create("locatorTypeName", "typename", MFnData::kString, &stat);
	addAttribute(locatorTypeName);
	
	labelText = typedAttr.create("labelText", "label", MFnData::kString, &stat);
	typedAttr.setKeyable(true);
	addAttribute(labelText);

	labelFontSize = numAttr.create("labelFontSize", "fontsize", MFnNumericData::kInt, 13);
	numAttr.setKeyable(true);
	addAttribute(labelFontSize);

	labelOffsetX = numAttr.create("labelOffsetX", "lox", MFnNumericData::kFloat, 0.0);
	numAttr.setKeyable(false);
	addAttribute(labelOffsetX);

	labelOffsetY = numAttr.create("labelOffsetY", "loy", MFnNumericData::kFloat, 0.0);
	numAttr.setKeyable(false);
	addAttribute(labelOffsetY);


	attributeAffects(inputCurves, output);
	attributeAffects(labelText, output);
	attributeAffects(labelFontSize, output);
	attributeAffects(labelOffsetX, output);
	attributeAffects(labelOffsetY, output);


	return MS::kSuccess;
}
