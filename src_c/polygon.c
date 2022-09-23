#include "include/pygame.h"
#include "include/geometry.h"
#include "include/collisions.h"

#include <limits.h>
#include <float.h>
#include <stddef.h>
#include <math.h>

static int
set_polygon_center_coords(pgPolygonBase *polygon)
{
    if (!polygon) {
        return 0;
    }
    double sum_x = 0;
    double sum_y = 0;
    Py_ssize_t i2; 
    for (i2 = 0; i2 < polygon->verts_num * 2; i2 += 2) {
        sum_x += polygon->vertices[i2];
        sum_y += polygon->vertices[i2 + 1];
    }
    polygon->c_x = sum_x / polygon->verts_num;
    polygon->c_y = sum_y / polygon->verts_num;
    return 1;
}

static int
move_polygon(pgPolygonBase *polygon, double dx, double dy)
{
    if (!polygon) {
        return 0;
    }
    Py_ssize_t i2;
    for (i2 = 0; i2 < polygon->verts_num * 2; i2 += 2) {
        polygon->vertices[i2] += dx;
        polygon->vertices[i2 + 1] += dy;
    }
    polygon->c_x += dx;
    polygon->c_y += dy;
    return 1;
}

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

static PyObject *
_pg_polygon_vertices_aslist(pgPolygonBase *poly)
{
    PyObject *list = PyList_New(poly->verts_num);
    if (!list) {
        return NULL;
    }
    Py_ssize_t i;
    Py_ssize_t i2;

    for (i = 0; i < poly->verts_num; i++) {
        i2 = i * 2;
        PyObject *tup = pg_tuple_from_values_double(poly->vertices[i2],
                                                    poly->vertices[i2 + 1]);
        if (!tup) {
            Py_DECREF(list);
            return NULL;
        }
        PyList_SET_ITEM(list, i, tup);
        tup = NULL;
    }
    return list;
}

static PyObject *
_pg_polygon_vertices_astuple(pgPolygonBase *poly)
{
    PyObject *vertices = PyTuple_New(poly->verts_num);
    if (!vertices) {
        return NULL;
    }
    Py_ssize_t i;
    Py_ssize_t i2;
    
    for (i = 0; i < poly->verts_num; i++) {
        i2 = i * 2;
        PyObject *tup = pg_tuple_from_values_double(poly->vertices[i2],
                                                    poly->vertices[i2 + 1]);
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
        pgPolygonBase *poly = &pgPolygon_AsPolygon(obj);

        out->verts_num = poly->verts_num;
        if (!out->vertices) {
            /* Only allocate new memory if the polygon vertices' memory is
             * not allocated, just copy the values otherwise*/
            out->vertices = PyMem_New(double, poly->verts_num * 2);
            if (!out->vertices) {
                return 0;
            }
        }

        memcpy(out->vertices, poly->vertices,
               poly->verts_num * 2 * sizeof(double));
        set_polygon_center_coords(out);
        return 1;
    }

    if (PySequence_FAST_CHECK(obj)) {
        PyObject **f_arr = PySequence_Fast_ITEMS(obj);
        length = PySequence_Fast_GET_SIZE(obj);

        if (length >= 3) {
            Py_ssize_t i;
            Py_ssize_t i2;
            out->verts_num = length;

            if (!out->vertices) {
                /* Only allocate new memory if the polygon vertices' memory is
                 * not allocated*/
                out->vertices = PyMem_New(double, length * 2);
                if (!out->vertices) {
                    return 0;
                }
            }

            double x_coord_sum = 0.0;
            double y_coord_sum = 0.0;
            for (i = 0; i < out->verts_num; i++) {
                i2 = i * 2;
                if (!pg_TwoDoublesFromObj(f_arr[i], &(out->vertices[i2]),
                                          &(out->vertices[i2 + 1]))) {
                    return 0;
                }
                x_coord_sum += out->vertices[i2];
                y_coord_sum += out->vertices[i2 + 1];
            }
            out->c_x = x_coord_sum / out->verts_num;
            out->c_y = y_coord_sum / out->verts_num;
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
            Py_ssize_t i2;
            
            out->verts_num = length;
            out->vertices = PyMem_New(double, length * 2);
            if (!out->vertices) {
                return 0;
            }

            double x_coord_sum = 0.0;
            double y_coord_sum = 0.0;
            for (i = 0; i < length; i++) {
                i2 = i * 2;
                tmp = PySequence_ITEM(obj, i);
                if (!pg_TwoDoublesFromObj(tmp, &(out->vertices[i2]),
                                          &(out->vertices[i2 + 1]))) {
                    Py_DECREF(tmp);
                    return 0;
                }
                x_coord_sum += out->vertices[i2];
                y_coord_sum += out->vertices[i2 + 1];
                Py_DECREF(tmp);
                tmp = NULL;
            }
            out->c_x = x_coord_sum / out->verts_num;
            out->c_y = y_coord_sum / out->verts_num;
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
pgPolygon_FromObjectFastcall(PyObject *const *args, Py_ssize_t nargs,
                             pgPolygonBase *out)
{
    if (nargs == 1) {
        return pgPolygon_FromObject(args[0], out);
    }
    else if (nargs >= 3) {
        Py_ssize_t i;
        Py_ssize_t i2;
        out->verts_num = nargs;

        if (!out->vertices) {
            /* Only allocate new memory if the polygon vertices' memory is
             * not allocated*/
            out->vertices = PyMem_New(double, nargs * 2);
            if (!out->vertices) {
                return 0;
            }
        }
        double x_coord_sum = 0.0;
        double y_coord_sum = 0.0;   
        for (i = 0; i < nargs; i++) {
            i2 = i * 2;
            if (!pg_TwoDoublesFromObj(args[i], &(out->vertices[i2]),
                                      &(out->vertices[i2 + 1]))) {
                return 0;
            }
            x_coord_sum += out->vertices[i2];
            y_coord_sum += out->vertices[i2 + 1];         
        }
        out->c_x = x_coord_sum / out->verts_num;
        out->c_y = y_coord_sum / out->verts_num;   
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
        polygon_obj->polygon.vertices = PyMem_New(double, verts_num * 2);
        if (!polygon_obj->polygon.vertices) {
            Py_DECREF(polygon_obj);
            return NULL;
        }

        memcpy(polygon_obj->polygon.vertices, vertices,
               verts_num * 2 * sizeof(double));

        polygon_obj->polygon.verts_num = verts_num;
        set_polygon_center_coords(&(polygon_obj->polygon));
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
        self->polygon.c_x = 0;
        self->polygon.c_y = 0;
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
    return PyUnicode_FromFormat("<Polygon(%S, %S)>",
                                PyLong_FromLong((int)self->polygon.verts_num),
                                _pg_polygon_vertices_aslist(&self->polygon));
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

static PyObject *
pg_polygon_copy(pgPolygonObject *self, PyObject *_null)
{
    return pgPolygon_New(&self->polygon);
}

static PyObject *
pg_polygon_move(pgPolygonObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    double Dx = 0.0, Dy = 0.0;

    if (nargs == 1) {
        if (!pg_TwoDoublesFromObj(args[0], &Dx, &Dy)) {
            goto error;
        }
    }
    else if (nargs == 2) {
        if (!pg_DoubleFromObj(args[0], &Dx) ||
            !pg_DoubleFromObj(args[1], &Dy)) {
            goto error;
        }
    }
    else {
        goto error;
    }

    move_polygon(&self->polygon, Dx, Dy);
    return _pg_polygon_subtype_new2(Py_TYPE(self), self->polygon.vertices,
                                    self->polygon.verts_num);
error:
    return RAISE(PyExc_TypeError, "move requires a pair of numbers");
}

static PyObject *
pg_polygon_move_ip(pgPolygonObject *self, PyObject *const *args,
                  Py_ssize_t nargs)
{
    double Dx = 0.0, Dy = 0.0;

    if (nargs == 1) {
        if (!pg_TwoDoublesFromObj(args[0], &Dx, &Dy)) {
            goto error;
        }
    }
    else if (nargs == 2) {
        if (!pg_DoubleFromObj(args[0], &Dx) ||
            !pg_DoubleFromObj(args[1], &Dy)) {
            goto error;
        }
    }
    else {
        goto error;
    }

    move_polygon(&(self->polygon), Dx, Dy);
    Py_RETURN_NONE;

error:
    return RAISE(PyExc_TypeError, "move requires a pair of numbers");
}

static struct PyMethodDef pg_polygon_methods[] = {
    {"move", (PyCFunction)pg_polygon_move, METH_FASTCALL, NULL},
    {"move_ip", (PyCFunction)pg_polygon_move_ip, METH_FASTCALL, NULL},
    {"__copy__", (PyCFunction)pg_polygon_copy, METH_NOARGS, NULL},
    {"copy", (PyCFunction)pg_polygon_copy, METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL}};

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

static PyObject *
pg_polygon_get_center_x(pgPolygonObject *self, void *closure)
{
    return PyFloat_FromDouble(self->polygon.c_x);
}

static int
pg_polygon_set_center_x(pgPolygonObject *self, PyObject *value, void *closure)
{
    double val;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (!pg_DoubleFromObj(value, &val)) {
        PyErr_SetString(PyExc_TypeError, "Expected a number");
        return -1;
    }
    move_polygon(&(self->polygon), (val - self->polygon.c_x), 0.0);
    return 0;
}

static PyObject *
pg_polygon_get_center_y(pgPolygonObject *self, void *closure)
{
    return PyFloat_FromDouble(self->polygon.c_y);
}

static int
pg_polygon_set_center_y(pgPolygonObject *self, PyObject *value, void *closure)
{
    double val;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (!pg_DoubleFromObj(value, &val)) {
        PyErr_SetString(PyExc_TypeError, "Expected a number");
        return -1;
    }
    move_polygon(&(self->polygon), 0.0, (val - self->polygon.c_y));
    return 0;
}

static PyObject *
pg_polygon_get_center(pgPolygonObject *self, void *closure)
{
    return pg_tuple_from_values_double(self->polygon.c_x, self->polygon.c_y);
}

static int
pg_polygon_set_center(pgPolygonObject *self, PyObject *value, void *closure)
{
    double new_c_x = 0, new_c_y = 0;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (!pg_TwoDoublesFromObj(value, &new_c_x, &new_c_y)) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
        return -1;
    }
    move_polygon(&(self->polygon), (new_c_x - self->polygon.c_x),
                 (new_c_y - self->polygon.c_y));
    return 0;
}

static PyGetSetDef pg_polygon_getsets[] = {
    {"c_x", (getter)pg_polygon_get_center_x, (setter)pg_polygon_set_center_x,
    NULL, NULL},
    {"c_y", (getter)pg_polygon_get_center_y, (setter)pg_polygon_set_center_y,
    NULL, NULL},
    {"center", (getter)pg_polygon_get_center, (setter)pg_polygon_set_center,
    NULL, NULL},
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
