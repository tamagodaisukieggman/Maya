#pragma once

#include <maya/MPxCommand.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MFloatArray.h>

class selectNearVertices : public MPxCommand
{
public:
	selectNearVertices();
	~selectNearVertices() override;

	MStatus     doIt(const MArgList& args) override;
	MStatus     redoIt() override;
	MStatus     undoIt() override;
	MSyntax		syntax();
	bool        isUndoable() const override;

	static      void* creator();

};

class findCloseUVsOnHardEdge : public MPxCommand
{
public:
	findCloseUVsOnHardEdge();
	~findCloseUVsOnHardEdge() override;

	MStatus     doIt(const MArgList& args) override;
	MStatus     redoIt() override;
	MStatus     undoIt() override;
	MSyntax		syntax();
	bool        isUndoable() const override;

	static      void* creator();
private:
	float		texsize;
	float		npixels;
	MStatus		execute(MObjectArray &meshes);
	MStatus		procMesh(MObject mesh);
};

class findUvOverlappedFaces : public MPxCommand
{
public:
	struct Ray
	{
	public:
		MPoint origin;
		MVector dir;
	};

	struct Face
	{
	public:
		MPoint center;
		float radius=0;
		bool hasUV=false;
		std::vector<Ray> rays;

	};

public:
	findUvOverlappedFaces();
	~findUvOverlappedFaces() override;

	MStatus     doIt(const MArgList& args) override;
	MStatus     redoIt() override;
	MStatus     undoIt() override;
	MSyntax		syntax();
	bool        isUndoable() const override;

	static      void* creator();
private:
	std::vector<Face> faces;
	MStatus		execute(MObjectArray &meshes);
	MStatus		procMesh(MObject mesh);
};


std::ostream& operator<<(std::ostream& stream, const findUvOverlappedFaces::Face& face);
