#ifndef _apiutils_
#define _apiutils_

#include <memory>

#include <maya/MSelectionList.h>
#include <maya/MDagPath.h>

#include <sfcnn.hpp>

//template <typename Point, unsigned int Dim, typename NumType> class sfcnn;



namespace apiutils
{
	typedef reviver::dpoint<int, 2> IntPoint2d;
	typedef reviver::dpoint<int, 3> IntPoint3d;
	enum MatchMode { POSITION, VERTEXID, UV };
	struct Correspondance
	{
		int objid;
		int vid;
	};

	class NNSearch
	{
		//sfcnn< MPoint, 3, double> *nn = nullptr;
		sfcnn<IntPoint3d, 3, int> *nn = nullptr;

		MObject mesh;
		int		cnt;
		int		scaleFactor;

	public:
		NNSearch();
		~NNSearch();
		//NNSearch(MObject& _mesh);
		MSelectionList getNearVerticesOnMesh(MPoint pnt, MObject mesh, int cnt);
		MIntArray getNearVertexIndicesOnMesh(MPoint pnt, int cnt);
		void build(MPointArray& pnts);
	};
	
	MSelectionList getNearVerticesOnMesh(MPoint pnt, MObject mesh, int cnts);
	MIntArray getNearVertexIndicesOnMesh(MPoint pnt, MObject mesh, int cnts);
	void computeCorrespondance(MObject& src, MObject& dst, MatchMode matchMode, MIntArray& result);
	void elapsedTime(const char*);
	void resetElapsedTime(const char*);
}

#endif /* _apiutils_ */
