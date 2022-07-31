#ifndef _BASE_H
#define _BASE_H

#include "pygame.h"

// all of this functions return 1 on success and 0 on failure.


static PG_FORCE_INLINE int
pg_IntFromObj(PyObject *obj, int *val)
{
    int tmp_val;

    if (PyFloat_Check(obj)) {
        /* Python3.8 complains with deprecation warnings if we pass
         * floats to PyLong_AsLong.
         */
        double dv = PyFloat_AsDouble(obj);
        tmp_val = (int)dv;
    }
    else {
        tmp_val = PyLong_AsLong(obj);
    }

    if (tmp_val == -1 && PyErr_Occurred()) {
        PyErr_Clear();
        return 0;
    }
    *val = tmp_val;
    return 1;
}

static PG_FORCE_INLINE int
pg_IntFromObjIndex(PyObject *obj, int _index, int *val)
{
    int result = 0;
    PyObject *item = PySequence_GetItem(obj, _index);

    if (!item) {
        PyErr_Clear();
        return 0;
    }
    result = pg_IntFromObj(item, val);
    Py_DECREF(item);
    return result;
}

static PG_FORCE_INLINE int
pg_TwoIntsFromObj(PyObject *obj, int *val1, int *val2)
{
    if (!obj) return 0;
    if (PyTuple_Check(obj) && PyTuple_Size(obj) == 1) {
        return pg_TwoIntsFromObj(PyTuple_GET_ITEM(obj, 0), val1, val2);
    }
    if (!PySequence_Check(obj) || PySequence_Length(obj) != 2) {
        return 0;
    }
    if (!pg_IntFromObjIndex(obj, 0, val1) ||
        !pg_IntFromObjIndex(obj, 1, val2)) {
        return 0;
    }
    return 1;
}

static PG_FORCE_INLINE int
pg_FloatFromObj(PyObject *obj, float *val)
{
    float f = (float)PyFloat_AsDouble(obj);

    if (f == -1 && PyErr_Occurred()) {
        PyErr_Clear();
        return 0;
    }

    *val = f;
    return 1;
}

static PG_FORCE_INLINE int
pg_FloatFromObjIndex(PyObject *obj, int _index, float *val)
{
    int result = 0;
    PyObject *item = PySequence_GetItem(obj, _index);

    if (!item) {
        PyErr_Clear();
        return 0;
    }
    result = pg_FloatFromObj(item, val);
    Py_DECREF(item);
    return result;
}

static PG_FORCE_INLINE int
pg_TwoFloatsFromObj(PyObject *obj, float *val1, float *val2)
{
    if (PyTuple_Check(obj) && PyTuple_Size(obj) == 1) {
        return pg_TwoFloatsFromObj(PyTuple_GET_ITEM(obj, 0), val1, val2);
    }
    if (!PySequence_Check(obj) || PySequence_Length(obj) != 2) {
        return 0;
    }
    if (!pg_FloatFromObjIndex(obj, 0, val1) ||
        !pg_FloatFromObjIndex(obj, 1, val2)) {
        return 0;
    }
    return 1;
}

static PG_FORCE_INLINE int
pg_DoubleFromObj(PyObject *obj, double *val) {
    double f = PyFloat_AsDouble(obj);

    if (f == -1 && PyErr_Occurred()) {
        PyErr_Clear();
        return 0;
    }

    *val = f;
    return 1;
}

static PG_FORCE_INLINE int
pg_DoubleFromObjIndex(PyObject *obj, int _index, double *val) {
    int result = 0;
    PyObject *item = PySequence_GetItem(obj, _index);

    if (!item) {
        PyErr_Clear();
        return 0;
    }
    result = pg_DoubleFromObj(item, val);
    Py_DECREF(item);
    return result;
}

static PG_FORCE_INLINE int
pg_TwoDoublesFromObj(PyObject *obj, double *val1, double *val2) {
    if (PyTuple_Check(obj) && PyTuple_Size(obj) == 1) {
        return pg_TwoDoublesFromObj(PyTuple_GET_ITEM(obj, 0), val1, val2);
    }
    if (!PySequence_Check(obj) || PySequence_Length(obj) != 2) {
        return 0;
    }
    if (!pg_DoubleFromObjIndex(obj, 0, val1) ||
        !pg_DoubleFromObjIndex(obj, 1, val2)) {
        return 0;
    }
    return 1;
}

static PG_FORCE_INLINE int
pg_UintFromObj(PyObject *obj, Uint32 *val)
{
    if (PyNumber_Check(obj)) {
        PyObject *longobj;

        if (!(longobj = PyNumber_Long(obj))) {
            PyErr_Clear();
            return 0;
        }
        *val = (Uint32)PyLong_AsUnsignedLong(longobj);
        Py_DECREF(longobj);
        if (PyErr_Occurred()) {
            PyErr_Clear();
            return 0;
        }
        return 1;
    }
    return 0;
}

static PG_FORCE_INLINE int
pg_UintFromObjIndex(PyObject *obj, int _index, Uint32 *val)
{
    int result = 0;
    PyObject *item = PySequence_GetItem(obj, _index);

    if (!item) {
        PyErr_Clear();
        return 0;
    }
    result = pg_UintFromObj(item, val);
    Py_DECREF(item);
    return result;
}

#endif /* ~_BASE_H */
