//
// Copyright (C) 
// 
// File: testCmd.cpp
//
// MEL Command: test
//
// Author: Maya Plug-in Wizard 2.0
//

#include <maya/MPoint.h>

#include <maya/MSimple.h>

#include "apiutils.h"

DeclareSimpleCommand( test, "", "2018");

MStatus test::doIt( const MArgList& args )
//
//	Description:
//		implements the MEL test command.
//
//	Arguments:
//		args - the argument list that was passes to the command from MEL
//
//	Return Value:
//		MS::kSuccess - command succeeded
//		MS::kFailure - command failed
//
{
	MStatus stat = MS::kSuccess;
	MPoint pnt;
	MObject mesh;
	int cnt = 1;

	MSelectionList slist = apiutils::NNSearch::getNearVerticesOnMesh(pnt, mesh, cnt);
	//apiutils::elapsedTime("test");

	setResult( "test command executed!\n" );

	return stat;
}
