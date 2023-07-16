
#ifndef _GEOMETRY_H
#define _GEOMETRY_H

#include "pygame.h"
#include <float.h>
#include <stddef.h>
#include <math.h>

typedef struct {
    double x, y, r;
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

typedef struct {
    double xa, ya;
    double xb, yb;
} pgLineBase;

typedef struct {
    PyObject_HEAD pgLineBase line;
    PyObject *weakreflist;
} pgLineObject;

#define pgLine_CAST(o) ((pgLineObject *)(o))

#define pgLine_GETLINE(o) (pgLine_CAST(o)->line)
#define pgLine_AsLine(o) (pgLine_CAST(o)->line)
#define pgLine_GETX1(self) (pgLine_CAST(self)->line.xa)
#define pgLine_GETY1(self) (pgLine_CAST(self)->line.ya)
#define pgLine_GETX2(self) (pgLine_CAST(self)->line.xb)
#define pgLine_GETY2(self) (pgLine_CAST(self)->line.yb)

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
    double centerx, centery;
} pgPolygonBase;

typedef struct {
    PyObject_HEAD pgPolygonBase polygon;
    PyObject *weakreflist;
} pgPolygonObject;

#define pgPolygon_CAST(o) ((pgPolygonObject *)(o))
#define pgPolygon_AsPolygon(o) (pgPolygon_CAST(o)->polygon)
#define pgPolygon_GETVERTICES(o) (pgPolygon_AsPolygon(o).vertices)
#define pgPolygon_GETVERTSNUM(o) (pgPolygon_AsPolygon(o).verts_num)
#define pgPolygon_GETCENTER_X(o) (pgPolygon_AsPolygon(o).centerx)
#define pgPolygon_GETCENTER_Y(o) (pgPolygon_AsPolygon(o).centery)

// return 1 if success and 0 if failure
static int
pgPolygon_FromObject(PyObject *obj, pgPolygonBase *out, int *was_sequence);

static int
pgPolygon_FromObjectFastcall(PyObject *const *args, Py_ssize_t nargs,
                             pgPolygonBase *out, int *was_sequence);

#define pgCircle_Check(o) ((o)->ob_type == &pgCircle_Type)
#define pgLine_Check(o) ((o)->ob_type == &pgLine_Type)
#define pgPolygon_Check(o) ((o)->ob_type == &pgPolygon_Type)

/* Constants */

/* PI */
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

/* 2PI */
#ifndef M_TWOPI
#define M_TWOPI 6.28318530717958647692
#endif

/* PI/2 */
#ifndef M_PI_QUO_2
#define M_PI_QUO_2 1.57079632679489661923
#endif

/* PI/4 */
#ifndef M_PI_QUO_4
#define M_PI_QUO_4 0.78539816339744830962
#endif

/* PI/180 */
#ifndef M_PI_QUO_180
#define M_PI_QUO_180 0.01745329251994329577
#endif

/* 180/PI */
#ifndef M_180_QUO_PI
#define M_180_QUO_PI 57.29577951308232087680
#endif

/* Functions */

/* Converts degrees to radians */
static PG_FORCE_INLINE double
DEG_TO_RAD(double deg)
{
    return deg * M_PI_QUO_180;
}

/* Converts radians to degrees */
static PG_FORCE_INLINE double
RAD_TO_DEG(double rad)
{
    return rad * M_180_QUO_PI;
}

/* Frees the polygon's vertices if they were allocated from a sequence. */
static PG_FORCE_INLINE void
PG_FREEPOLY_COND(pgPolygonBase *poly, int was_sequence)
{
    if (was_sequence) {
        PyMem_Free(poly->vertices);
    }
}

#endif /* ~_GEOMETRY_H */
