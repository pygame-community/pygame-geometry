#include "include/pygame.h"
#include "include/geometry.h"
#include "include/collisions.h"
#include "include/methods.h"

#include <limits.h>
#include <float.h>
#include <math.h>

#ifndef PySequence_FAST_CHECK
#define PySequence_FAST_CHECK(o) (PyList_Check(o) || PyTuple_Check(o))
#endif /* ~PySequence_FAST_CHECK */

static PyObject *
pg_geometry_raycast(PyObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    PyObject **A_farr;
    PyObject **B_farr;
    Py_ssize_t A_len;
    Py_ssize_t B_len;
    Py_ssize_t i;
    Py_ssize_t j;

    if (nargs != 2) {
        return RAISE(PyExc_TypeError, "raycast() takes exactly 2 arguments");
    }
    if (!PySequence_FAST_CHECK(args[0])) {
        return RAISE(PyExc_TypeError,
                     "raycast() first argument must be a sequence");
    }
    if (!PySequence_FAST_CHECK(args[1])) {
        return RAISE(PyExc_TypeError,
                     "raycast() second argument must be a sequence");
    }

    A_len = PySequence_Fast_GET_SIZE(args[0]);
    B_len = PySequence_Fast_GET_SIZE(args[1]);

    if (A_len == 0) {
        return PyList_New(0);
    }
    if (B_len == 0) {
        PyObject *ret = PyList_New(A_len);
        for (i = 0; i < A_len; i++) {
            PyList_SET_ITEM(ret, i, Py_None);
        }
        return ret;
    }

    A_farr = PySequence_Fast_ITEMS(args[0]);
    B_farr = PySequence_Fast_ITEMS(args[1]);

    PyObject *ret = PyList_New(A_len);

    if (!ret) {
        return NULL;
    }

    pgLineBase A_line;
    pgLineBase B_line;

    for (i = 0; i < A_len; i++) {
        if (!pgLine_FromObject(A_farr[i], &A_line)) {
            Py_DECREF(ret);
            return RAISE(
                PyExc_TypeError,
                "raycast() first argument must be a sequence of Line or "
                "LineLike objects");
        }

        double record = DBL_MAX;
        double closest_x = 0, closest_y = 0;
        double x = 0, y = 0;

        for (j = 0; j < B_len; j++) {
            if (!pgLine_FromObject(B_farr[j], &B_line)) {
                Py_DECREF(ret);
                return RAISE(
                    PyExc_TypeError,
                    "raycast() second argument must be a sequence of Line or "
                    "LineLike objects");
            }

            if (pgIntersection_LineLine(&A_line, &B_line, &x, &y)) {
                if (x * x + y * y < record) {
                    record = x * x + y * y;
                    closest_x = x;
                    closest_y = y;
                }
            }
        }

        if (record == DBL_MAX) {
            PyList_SET_ITEM(ret, i, Py_None);
        }
        else {
            PyList_SET_ITEM(ret, i,
                            Py_BuildValue("(dd)", closest_x, closest_y));
        }
    }
    return ret;
}
