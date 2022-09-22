
#ifndef _GEOMETRY_H
#define _GEOMETRY_H

#include "pygame.h"

typedef struct {
    double x, y, r, r_sqr;
} pgCircleBase;

typedef struct {
    PyObject_HEAD pgCircleBase circle;
    PyObject *weakreflist;
} pgCircleObject;

#define pgCircle_CAST(o) ((pgCircleObject *)(o))
#define pgCircle_AsCircle(o) (pgCircle_CAST(o)->circle)
#define pgCircle_GETX(self) (pgCircle_CAST(self)->circle.x)
#define pgCircle_GETY(self) (pgCircle_CAST(self)->circle.y)
#define pgCircle_GETR(self) (pgCircle_CAST(self)->circle.r)
#define pgCircle_GETRSQR(self) (pgCircle_CAST(self)->circle.r_sqr)

typedef struct {
    double x1, y1;
    double x2, y2;
} pgLineBase;

typedef struct {
    PyObject_HEAD pgLineBase line;
    PyObject *weakreflist;
} pgLineObject;

#define pgLine_CAST(o) ((pgLineObject *)(o))

#define pgLine_GETLINE(o) (pgLine_CAST(o)->line)
#define pgLine_AsLine(o) (pgLine_CAST(o)->line)
#define pgLine_GETX1(self) (pgLine_CAST(self)->line.x1)
#define pgLine_GETY1(self) (pgLine_CAST(self)->line.y1)
#define pgLine_GETX2(self) (pgLine_CAST(self)->line.x2)
#define pgLine_GETY2(self) (pgLine_CAST(self)->line.y2)

// return 1 if success and 0 if failure
static int
pgLine_FromObject(PyObject *obj, pgLineBase *out);
// return 1 if success and 0 if failure
static int
pgLine_FromObjectFastcall(PyObject *const *args, Py_ssize_t nargs,
                          pgLineBase *out);
// return 1 if success and 0 if failure
static int
pgCircle_FromObject(PyObject *obj, pgCircleBase *out);
// return 1 if success and 0 if failure
static int
pgCircle_FromObjectFastcall(PyObject *const *args, Py_ssize_t nargs,
                            pgCircleBase *out);

static PyTypeObject pgCircle_Type;
static PyTypeObject pgLine_Type;
static PyTypeObject pgPolygon_Type;

typedef struct {
    Py_ssize_t verts_num;
    double *vertices;
    double c_x, c_y;
} pgPolygonBase;

typedef struct {
    PyObject_HEAD pgPolygonBase polygon;
    PyObject *weakreflist;
} pgPolygonObject;

#define pgPolygon_CAST(o) ((pgPolygonObject *)(o))
#define pgPolygon_AsPolygon(o) (pgPolygon_CAST(o)->polygon)
#define pgPolygon_GETVERTICES(o) (pgPolygon_AsPolygon(o).vertices)
#define pgPolygon_GETVERTSNUM(o) (pgPolygon_AsPolygon(o).verts_num)
#define pgPolygon_GETCENTER_X(o) (pgPolygon_AsPolygon(o).c_x)
#define pgPolygon_GETCENTER_Y(o) (pgPolygon_AsPolygon(o).c_y)

// return 1 if success and 0 if failure
static int
pgPolygon_FromObject(PyObject *obj, pgPolygonBase *out);

#define pgCircle_Check(o) ((o)->ob_type == &pgCircle_Type)
#define pgLine_Check(o) ((o)->ob_type == &pgLine_Type)
#define pgPolygon_Check(o) ((o)->ob_type == &pgPolygon_Type)

#endif /* ~_GEOMETRY_H */
