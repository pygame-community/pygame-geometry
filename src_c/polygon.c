#include "include/pygame.h"
#include "include/geometry.h"
#include "include/collisions.h"

#include <limits.h>
#include <float.h>
#include <stddef.h>
#include <math.h>

static PyObject *
pg_tuple_from_values_double(double val1, double val2)
{
    PyObject *tup = PyTuple_New(2);
    if (!tup) {
        return NULL;
    }

    PyObject *tmp = PyFloat_FromDouble(val1);
    if (!tmp) {
        Py_DECREF(tup);
        return NULL;
    }
    PyTuple_SET_ITEM(tup, 0, tmp);

    tmp = PyFloat_FromDouble(val2);
    if (!tmp) {
        Py_DECREF(tup);
        return NULL;
    }
    PyTuple_SET_ITEM(tup, 1, tmp);

    return tup;
}

inline static PyObject *
_pg_polygon_vertices_aslist(pgPolygonBase *poly)
{
    PyObject *vertices = PyList_New(poly->verts_num);
    if (!vertices) {
        return NULL;
    }
    Py_ssize_t i;
    for (i = 0; i < poly->verts_num; i++) {
        PyObject *tup = pg_tuple_from_values_double(poly->vertices[i],
                                                    poly->vertices[i + 1]);
        if (!tup) {
            Py_DECREF(vertices);
            return NULL;
        }
        PyList_SET_ITEM(vertices, i, tup);
    }
    return vertices;
}

inline static PyObject *
_pg_polygon_vertices_astuple(pgPolygonBase *poly)
{
    PyObject *vertices = PyTuple_New(poly->verts_num);
    if (!vertices) {
        return NULL;
    }
    Py_ssize_t i;
    for (i = 0; i < poly->verts_num; i++) {
        PyObject *tup = pg_tuple_from_values_double(poly->vertices[i],
                                                    poly->vertices[i + 1]);
        if (!tup) {
            Py_DECREF(vertices);
            return NULL;
        }
        PyTuple_SET_ITEM(vertices, i, tup);
    }
    return vertices;
}

static int
pgPolygon_FromObject(PyObject *obj, pgPolygonBase *out)
{
    Py_ssize_t length;

    if (pgPolygon_Check(obj)) {
        out->verts_num = pgPolygon_GETVERTSNUM(obj);
        out->vertices = PyMem_New(double, out->verts_num * 2);
        if (!out->vertices) {
            return 0;
        }

        memcpy(&(out->vertices), &pgPolygon_GETVERTICES(obj),
               sizeof(double) * out->verts_num * 2);

        return 1;
    }

    if (PySequence_FAST_CHECK(obj)) {
        PyObject **f_arr = PySequence_Fast_ITEMS(obj);
        length = PySequence_Fast_GET_SIZE(obj);

        if (length >= 3) {
            Py_ssize_t i;
            out->verts_num = length;
            out->vertices = PyMem_New(double, length * 2);

            if (!out->vertices) {
                return 0;
            }

            for (i = 0; i < length; i++) {
                if (!pg_TwoDoublesFromObj(f_arr[i], &(out->vertices[i]),
                                          &(out->vertices[i + 1]))) {
                    return 0;
                }
            }

            return 1;
        }
        else if (length == 1) {
            if (!pgPolygon_FromObject(f_arr[0], out)) {
                return 0;
            }
            return 1;
        }

        /* Sequences of size 0 or 2 are not supported*/
        return 0;
    }
    else if (PySequence_Check(obj)) {
        /* Path for other sequences or Types that count as sequences*/
        PyObject *tmp = NULL;
        length = PySequence_Length(obj);

        if (length >= 3) {
            Py_ssize_t i;
            out->verts_num = length;
            out->vertices = PyMem_New(double, length * 2);
            if (!out->vertices) {
                return 0;
            }

            for (i = 0; i < length; i++) {
                tmp = PySequence_ITEM(obj, i);
                if (!pg_TwoDoublesFromObj(tmp, &(out->vertices[i]),
                                          &(out->vertices[i + 1]))) {
                    Py_DECREF(tmp);
                    return 0;
                }
                Py_DECREF(tmp);
                tmp = NULL;
            }

            return 1;
        }
        else if (length == 1) {
            tmp = PySequence_ITEM(obj, 0);
            if (PyUnicode_Check(obj) || !pgPolygon_FromObject(tmp, out)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            return 1;
        }

        /* Sequences of size 0 or 2 are not supported*/
        return 0;
    }

    if (PyObject_HasAttrString(obj, "polygon")) {
        PyObject *polyattr;
        polyattr = PyObject_GetAttrString(obj, "polygon");
        if (polyattr == NULL) {
            PyErr_Clear();
            return 0;
        }
        if (PyCallable_Check(polyattr)) /*call if it's a method*/
        {
            PyObject *polyresult = PyObject_CallObject(polyattr, NULL);
            Py_DECREF(polyattr);
            if (polyresult == NULL) {
                PyErr_Clear();
                return 0;
            }
            polyattr = polyresult;
        }
        if (!pgPolygon_FromObject(polyattr, out)) {
            PyErr_Clear();
            Py_DECREF(polyattr);
            return 0;
        }
        Py_DECREF(polyattr);

        return 1;
    }

    return 0;
}

static int
pg_polygon_init(pgPolygonObject *self, PyObject *args, PyObject *kwds)
{
    if (!pgPolygon_FromObject(args, &(self->polygon))) {
        PyErr_SetString(PyExc_TypeError,
                        "Argument must be Polygon style object");
        return -1;
    }

    return 0;
}

static PyObject *
_pg_polygon_subtype_new2(PyTypeObject *type, double *vertices,
                         Py_ssize_t verts_num)
{
    pgPolygonObject *polygon_obj =
        (pgPolygonObject *)pgPolygon_Type.tp_new(type, NULL, NULL);

    if (verts_num < 3) {
        /*A polygon requires 3 or more vertices*/
        Py_DECREF(polygon_obj);
        return NULL;
    }
    if (polygon_obj) {
        double *vertices_2 = PyMem_New(double, verts_num * 2);
        if (!vertices_2) {
            Py_DECREF(polygon_obj);
            return NULL;
        }
        polygon_obj->polygon.vertices = vertices_2;
        memcpy(&(polygon_obj->polygon.vertices), vertices,
               verts_num * 2 * sizeof(double));
        polygon_obj->polygon.verts_num = verts_num;
    }
    return (PyObject *)polygon_obj;
}

static PyObject *
pg_polygon_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    pgPolygonObject *self = (pgPolygonObject *)type->tp_alloc(type, 0);

    if (self) {
        self->polygon.vertices = NULL;
        self->polygon.verts_num = 0;
        self->weakreflist = NULL;
    }

    return (PyObject *)self;
}

static PyObject *
pgPolygon_New(pgPolygonBase *p)
{
    return _pg_polygon_subtype_new2(&pgPolygon_Type, p->vertices,
                                    p->verts_num);
}

static PyObject *
pgPolygon_New2(double *vertices, Py_ssize_t verts_num)
{
    return _pg_polygon_subtype_new2(&pgPolygon_Type, vertices, verts_num);
}

static void
pg_polygon_dealloc(pgPolygonObject *self)
{
    if (self->weakreflist != NULL) {
        PyObject_ClearWeakRefs((PyObject *)self);
    }

    PyMem_Free(self->polygon.vertices);

    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
pg_polygon_repr(pgPolygonObject *self)
{
    return PyUnicode_FromFormat("pygame.Polygon(%S, %S)",
                                _pg_polygon_vertices_aslist(&self->polygon),
                                PyLong_FromLong((int)self->polygon.verts_num));
}

static PyObject *
pg_polygon_str(pgPolygonObject *self)
{
    return pg_polygon_repr(self);
}

static PyObject *
pg_polygon_getsafepickle(pgPolygonObject *self, void *closure)
{
    Py_RETURN_TRUE;
}

static struct PyMethodDef pg_polygon_methods[] = {{NULL, NULL, 0, NULL}};

static PyObject *
pg_polygon_get_verts_num(pgPolygonObject *self, void *closure)
{
    return PyLong_FromLong((int)self->polygon.verts_num);
}

static PyObject *
pg_polygon_get_vertices(pgPolygonObject *self, void *closure)
{
    return _pg_polygon_vertices_aslist(&self->polygon);
}

static PyGetSetDef pg_polygon_getsets[] = {
    {"verts_num", (getter)pg_polygon_get_verts_num, NULL,
     "Number of vertices of the polygon", NULL},
    {"vertices", (getter)pg_polygon_get_vertices, NULL,
     "Vertices of the polygon", NULL},
    {"__safe_for_unpickling__", (getter)pg_polygon_getsafepickle, NULL, NULL,
     NULL},
    {NULL, 0, NULL, NULL, NULL} /* Sentinel */
};

static PyTypeObject pgPolygon_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame.Polygon",
    .tp_basicsize = sizeof(pgPolygonObject),
    .tp_dealloc = (destructor)pg_polygon_dealloc,
    .tp_repr = (reprfunc)pg_polygon_repr,
    .tp_str = (reprfunc)pg_polygon_str,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = NULL,
    .tp_weaklistoffset = offsetof(pgPolygonObject, weakreflist),
    .tp_methods = pg_polygon_methods,
    .tp_getset = pg_polygon_getsets,
    .tp_init = (initproc)pg_polygon_init,
    .tp_new = pg_polygon_new,
};