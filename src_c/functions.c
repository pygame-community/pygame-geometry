#include "include/geometry.h"
#include "include/functions.h"

#ifndef PI
#define PI 3.14159265358979323846
#endif /* ~PI */

static PyObject *
pgPolygon_New2(double *vertices, Py_ssize_t verts_num);

static PyObject *
geometry_regular_polygon(PyObject *_null, PyObject *const *args,
                         Py_ssize_t nargs)
{
    int sides;
    double radius;
    double angle = 0;
    double Cx, Cy;

    if (nargs < 3 || nargs > 4) {
        return RAISE(PyExc_TypeError,
                     "invalid number of arguments, expected 3 or 4 arguments");
    }
    if (!PyLong_Check(args[0])) {
        return RAISE(PyExc_TypeError,
                     "the first parameter must be an integer");
    }
    sides = PyLong_AsLong(args[0]);
    if (sides == -1 && PyErr_Occurred()) {
        return NULL;
    }

    if (!pg_TwoDoublesFromObj(args[1], &Cx, &Cy)) {
        return RAISE(PyExc_TypeError,
                     "the second parameter must be a sequence of 2 numbers");
    }

    if (!pg_DoubleFromObj(args[2], &radius)) {
        return RAISE(PyExc_TypeError, "the third parameter must be a number");
    }
    if (nargs == 4) {
        if (!pg_DoubleFromObj(args[3], &angle)) {
            return RAISE(PyExc_TypeError,
                         "the forth parameter must be a number");
        }
        angle *= PI / 180.0;
    }

    if (sides < 3) {
        if (sides < 0) {
            return RAISE(PyExc_ValueError,
                         "the sides can not be a negative number");
        }
        return RAISE(PyExc_ValueError, "polygons need at least 3 sides");
    }

    double *vertices = PyMem_New(double, sides * 2);
    if (!vertices) {
        return RAISE(PyExc_MemoryError,
                     "cannot allocate memory for the polygon vertices");
    }

    int loop;
    double fac = PI * 2 / sides;
    for (loop = 0; loop < sides; loop++) {
        double ang = angle + fac * loop;
        vertices[loop * 2] = Cx + radius * cos(ang);
        vertices[loop * 2 + 1] = Cy + radius * sin(ang);
    }

    PyObject *ret = pgPolygon_New2(vertices, sides);
    PyMem_Free(vertices);

    return ret;
}
