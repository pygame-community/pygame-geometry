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
    if (!obj)
        return 0;
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
pg_DoubleFromObj(PyObject *obj, double *val)
{
    if (PyFloat_Check(obj)) {
        *val = PyFloat_AS_DOUBLE(obj);
        return 1;
    }

    *val = (double)PyLong_AsLong(obj);
    if (PyErr_Occurred()) {
        PyErr_Clear();
        return 0;
    }

    return 1;
}

/*Assumes obj is a Sequence, internal or conscious use only*/
static PG_FORCE_INLINE int
_pg_DoubleFromObjIndex(PyObject *obj, int index, double *val)
{
    int result = 0;

    PyObject *item = PySequence_ITEM(obj, index);
    if (!item) {
        PyErr_Clear();
        return 0;
    }
    result = pg_DoubleFromObj(item, val);
    Py_DECREF(item);

    return result;
}

static PG_FORCE_INLINE int
pg_DoubleFromObjIndex(PyObject *obj, int index, double *val)
{
    int result = 0;

    if ((PyTuple_Check(obj) || PyList_Check(obj)) &&
        index < PySequence_Fast_GET_SIZE(obj)) {
        result = pg_DoubleFromObj(PySequence_Fast_GET_ITEM(obj, index), val);
    }
    else {
        PyObject *item = PySequence_GetItem(obj, index);

        if (!item) {
            PyErr_Clear();
            return 0;
        }
        result = pg_DoubleFromObj(item, val);
        Py_DECREF(item);
    }

    return result;
}

static PG_FORCE_INLINE int
pg_TwoDoublesFromObj(PyObject *obj, double *val1, double *val2)
{
    Py_ssize_t length;
    /*Faster path for tuples and lists*/
    if (PyTuple_Check(obj) || PyList_Check(obj)) {
        length = PySequence_Fast_GET_SIZE(obj);
        PyObject **f_arr = PySequence_Fast_ITEMS(obj);
        if (length == 2) {
            if (!pg_DoubleFromObj(f_arr[0], val1) ||
                !pg_DoubleFromObj(f_arr[1], val2)) {
                return 0;
            }
        }
        else if (length == 1) {
            /* Handle case of ((x, y), ) 'nested sequence' */
            return pg_TwoDoublesFromObj(f_arr[0], val1, val2);
        }
        else {
            return 0;
        }
    }
    else if (PySequence_Check(obj)) {
        length = PySequence_Length(obj);
        if (length == 2) {
            if (!_pg_DoubleFromObjIndex(obj, 0, val1)) {
                return 0;
            }
            if (!_pg_DoubleFromObjIndex(obj, 1, val2)) {
                return 0;
            }
        }
        else if (length == 1 && !PyUnicode_Check(obj)) {
            /* Handle case of ((x, y), ) 'nested sequence' */
            PyObject *tmp = PySequence_ITEM(obj, 0);
            int ret = pg_TwoDoublesFromObj(tmp, val1, val2);
            Py_DECREF(tmp);
            return ret;
        }
        else {
            PyErr_Clear();
            return 0;
        }
    }
    else {
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

static PG_FORCE_INLINE int
pg_TwoDoublesFromFastcallArgs(PyObject *const *args, Py_ssize_t nargs,
                              double *val1, double *val2)
{
    if (nargs == 1 && pg_TwoDoublesFromObj(args[0], val1, val2)) {
        return 1;
    }
    else if (nargs == 2 && pg_DoubleFromObj(args[0], val1) &&
             pg_DoubleFromObj(args[1], val2)) {
        return 1;
    }
    return 0;
}

// these return PyObject * on success and NULL on failure.

static PG_FORCE_INLINE PyObject *
pg_TupleFromDoublePair(double val1, double val2)
{
    /*this is demonstrated to be faster than Py_BuildValue*/
    PyObject *tuple = PyTuple_New(2);
    if (!tuple)
        return NULL;

    PyObject *tmp = PyFloat_FromDouble(val1);
    if (!tmp) {
        Py_DECREF(tuple);
        return NULL;
    }
    PyTuple_SET_ITEM(tuple, 0, tmp);

    tmp = PyFloat_FromDouble(val2);
    if (!tmp) {
        Py_DECREF(tuple);
        return NULL;
    }
    PyTuple_SET_ITEM(tuple, 1, tmp);

    return tuple;
}

static PG_FORCE_INLINE PyObject *
pg_TupleFromIntPair(int val1, int val2)
{
    /*this is demonstrated to be faster than Py_BuildValue*/
    PyObject *tuple = PyTuple_New(2);
    if (!tuple)
        return NULL;

    PyObject *tmp = PyLong_FromLong(val1);
    if (!tmp) {
        Py_DECREF(tuple);
        return NULL;
    }
    PyTuple_SET_ITEM(tuple, 0, tmp);

    tmp = PyLong_FromLong(val2);
    if (!tmp) {
        Py_DECREF(tuple);
        return NULL;
    }
    PyTuple_SET_ITEM(tuple, 1, tmp);

    return tuple;
}

static PG_FORCE_INLINE PyObject *
pg_PointList_FromArrayDouble(double *array, int arr_length)
{
    /*Takes an even length double array [1, 2, 3, 4, 5, 6, 7, 8] and returns
     * a list of points:
     * C_arr[1, 2, 3, 4, 5, 6, 7, 8] -> List((1, 2), (3, 4), (5, 6), (7, 8))*/

    if (arr_length % 2) {
        return RAISE(PyExc_ValueError, "array length must be even");
    }

    int num_points = arr_length / 2;
    PyObject *sequence = PyList_New(num_points);
    if (!sequence) {
        return NULL;
    }

    int i;
    PyObject *point = NULL;
    for (i = 0; i < num_points; i++) {
        point = pg_TupleFromDoublePair(array[i * 2], array[i * 2 + 1]);
        if (!point) {
            Py_DECREF(sequence);
            return NULL;
        }
        PyList_SET_ITEM(sequence, i, point);
    }

    return sequence;
}

static PG_FORCE_INLINE PyObject *
pg_PointTuple_FromArrayDouble(double *array, int arr_length)
{
    /*Takes an even length double array [1, 2, 3, 4, 5, 6, 7, 8] and returns
     * a tuple of points:
     * C_arr[1, 2, 3, 4, 5, 6, 7, 8] -> Tuple((1, 2), (3, 4), (5, 6), (7, 8))*/

    if (arr_length % 2) {
        return RAISE(PyExc_ValueError, "array length must be even");
    }

    int num_points = arr_length / 2;
    PyObject *sequence = PyTuple_New(num_points);
    if (!sequence) {
        return NULL;
    }

    int i;
    PyObject *point = NULL;
    for (i = 0; i < num_points; i++) {
        point = pg_TupleFromDoublePair(array[i * 2], array[i * 2 + 1]);
        if (!point) {
            Py_DECREF(sequence);
            return NULL;
        }
        PyTuple_SET_ITEM(sequence, i, point);
    }

    return sequence;
}

#endif /* ~_BASE_H */
