#include <Python.h>

#ifndef PySequence_FAST_CHECK
#define PySequence_FAST_CHECK(o) (PyList_Check(o) || PyTuple_Check(o))
#endif /* ~PySequence_FAST_CHECK */

static PyObject *
pg_geometry_raycast(PyObject *self, PyObject *const *args, Py_ssize_t nargs);
