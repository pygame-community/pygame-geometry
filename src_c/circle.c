#include "include/pygame.h"
#include "include/circle.h"
#include "include/base.h"

#include <limits.h>
#include <math.h>

static PyTypeObject pgCircle_Type;
#define pgCircle_Check(x) ((x)->ob_type == &pgCircle_Type)

static pgCircle *
pgCircle_FromObject(PyObject *obj, pgCircle *temp);

static int
pg_circle_init(pgCircleObject *, PyObject *, PyObject *);

static PyObject *
_pg_circle_subtype_new3(PyTypeObject *type, double x, double y, double r)
{
    pgCircleObject *circle_obj =
        (pgCircleObject *)pgCircle_Type.tp_new(type, NULL, NULL);

    if (circle_obj) {
        circle_obj->circle.x = x;
        circle_obj->circle.y = y;
        circle_obj->circle.r = r;
        circle_obj->circle.r_sqr = r * r;
    }
    return (PyObject *)circle_obj;
}

static PyObject *
pg_circle_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    pgCircleObject *self = (pgCircleObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->circle.x = self->circle.y = 0;
        self->circle.r = 0;
        self->circle.r_sqr = 0;
        self->weakreflist = NULL;
    }
    return (PyObject *)self;
}

static void
pg_circle_dealloc(pgCircleObject *self)
{
    if (self->weakreflist != NULL) {
        PyObject_ClearWeakRefs((PyObject *)self);
    }

    Py_TYPE(self)->tp_free((PyObject *)self);
}

static int
_pg_circle_set_radius(PyObject *value, pgCircle *circle)
{
    double tmp = 0;
    if (!pg_DoubleFromObj(value, &tmp))
        return 0;
    circle->r = tmp;
    circle->r_sqr = tmp * tmp;
    return 1;
}
static pgCircle *
pgCircle_FromObject(PyObject *obj, pgCircle *temp)
{
    Py_ssize_t length;

    if (pgCircle_Check(obj)) {
        return &((pgCircleObject *)obj)->circle;
    }

    if (PyList_Check(obj) || PyTuple_Check(obj)) {
        PyObject **f_arr = PySequence_Fast_ITEMS(obj);
        length = PySequence_Fast_GET_SIZE(obj);

        if (length == 3) {
            if (!pg_DoubleFromObj(f_arr[0], &(temp->x)) ||
                !pg_DoubleFromObj(f_arr[1], &(temp->y)) ||
                !_pg_circle_set_radius(f_arr[2], &temp)) {
                return NULL;
            }
            return temp;
        }
        else {
            /* Sequences of size other than 3 are not supported
            (don't wanna support infinite sequence nesting anymore)*/
            return NULL;
        }
    }
    else if (PySequence_Check(obj)) {
        /* Path for other sequences or Types that count as sequences*/
        PyObject *tmp = NULL;
        length = PySequence_Length(obj);
        if (length == 3) {
            /*These are to be substituted with better pg_DoubleFromSeqIndex()
             * implementations*/
            tmp = PySequence_ITEM(obj, 0);
            if (!pg_DoubleFromObj(tmp, &(temp->x))) {
                Py_DECREF(tmp);
                return NULL;
            }
            Py_DECREF(tmp);

            tmp = PySequence_ITEM(obj, 1);
            if (!pg_DoubleFromObj(tmp, &(temp->y))) {
                Py_DECREF(tmp);
                return NULL;
            }
            Py_DECREF(tmp);

            tmp = PySequence_ITEM(obj, 2);
            if (!_pg_circle_set_radius(tmp, &temp)) {
                Py_DECREF(tmp);
                return NULL;
            }
            Py_DECREF(tmp);

            return temp;
        }
        else {
            /* Sequences of size other than 3 are not supported
            (don't wanna support infinite sequence nesting anymore)*/
            return NULL;
        }
    }

    if (PyObject_HasAttrString(obj, "circle")) {
        PyObject *circleattr;
        pgCircle *retcircle;
        circleattr = PyObject_GetAttrString(obj, "circle");
        if (circleattr == NULL) {
            PyErr_Clear();
            return NULL;
        }
        if (PyCallable_Check(circleattr)) /*call if it's a method*/
        {
            PyObject *circleresult = PyObject_CallObject(circleattr, NULL);
            Py_DECREF(circleattr);
            if (circleresult == NULL) {
                PyErr_Clear();
                return NULL;
            }
            circleattr = circleresult;
        }
        retcircle = pgCircle_FromObject(circleattr, temp);
        Py_DECREF(circleattr);
        return retcircle;
    }
    return NULL;
}

static PyObject *
pgCircle_New(pgCircle *c)
{
    return _pg_circle_subtype_new3(&pgCircle_Type, c->x, c->y, c->r);
}

static PyObject *
pgCircle_New3(double x, double y, double r)
{
    return _pg_circle_subtype_new3(&pgCircle_Type, x, y, r);
}

static struct PyMethodDef pg_circle_methods[] = {{NULL, NULL, 0, NULL}};

/* numeric functions */
static int
pg_circle_bool(pgCircleObject *self)
{
    return self->circle.r != 0;
}

static PyNumberMethods pg_circle_as_number = {
    .nb_bool = (inquiry)pg_circle_bool,
};

static PyObject *
pg_circle_repr(pgCircleObject *self)
{
    // dont comments on it (-_-)
    return PyUnicode_FromFormat("pygame.Circle(%S, %S, %S)",
                                PyFloat_FromDouble(self->circle.x),
                                PyFloat_FromDouble(self->circle.y),
                                PyFloat_FromDouble(self->circle.r));
}

static PyObject *
pg_circle_str(pgCircleObject *self)
{
    return pg_circle_repr(self);
}

static PyObject *
pg_circle_richcompare(PyObject *o1, PyObject *o2, int opid)
{
    pgCircle *o1_circ, *o2_circ, temp1, temp2;
    double r1, r2;

    o1_circ = pgCircle_FromObject(o1, &temp1);
    o2_circ = pgCircle_FromObject(o2, &temp2);

    if (!o1_circ || !o2_circ) {
        goto Unimplemented;
    }

    r1 = o1_circ->r;
    r2 = o2_circ->r;

    switch (opid) {
        case Py_LT:
            return PyBool_FromLong(r1 < r2);
        case Py_LE:
            return PyBool_FromLong(r1 <= r2);
        case Py_EQ:
            return PyBool_FromLong(r1 == r2);
        case Py_NE:
            return PyBool_FromLong(r1 != r2);
        case Py_GT:
            return PyBool_FromLong(r1 > r2);
        case Py_GE:
            return PyBool_FromLong(r1 >= r2);
        default:
            break;
    }

Unimplemented:
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
}

#define GETSET_FOR_SIMPLE(name)                                               \
    static PyObject *pg_circle_get##name(pgCircleObject *self, void *closure) \
    {                                                                         \
        return PyFloat_FromDouble(self->circle.name);                         \
    }                                                                         \
    static int pg_circle_set##name(pgCircleObject *self, PyObject *value,     \
                                   void *closure)                             \
    {                                                                         \
        double val;                                                           \
        DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);                          \
        if (pg_DoubleFromObj(value, &val)) {                                  \
            self->circle.name = val;                                          \
            return 0;                                                         \
        }                                                                     \
        return -1;                                                            \
    }

// they are repetitive enough that we can abstract them like this
GETSET_FOR_SIMPLE(x)
GETSET_FOR_SIMPLE(y)

static PyObject *
pg_circle_getr(pgCircleObject *self, void *closure)
{
    return PyFloat_FromDouble(self->circle.r);
}
static int
pg_circle_setr(pgCircleObject *self, PyObject *value, void *closure)
{
    double val;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (pg_DoubleFromObj(value, &val)) {
        val = ABS(val);
        self->circle.r = val;
        self->circle.r_sqr = val * val;
        return 0;
    }
    return -1;
}

static PyObject *
pg_circle_getr_sqr(pgCircleObject *self, void *closure)
{
    return PyFloat_FromDouble(self->circle.r_sqr);
}

static PyObject *
pg_circle_getsafepickle(pgCircleObject *self, void *closure)
{
    Py_RETURN_TRUE;
}

static PyGetSetDef pg_circle_getsets[] = {
    {"x", (getter)pg_circle_getx, (setter)pg_circle_setx, NULL, NULL},
    {"y", (getter)pg_circle_gety, (setter)pg_circle_sety, NULL, NULL},
    {"r", (getter)pg_circle_getr, (setter)pg_circle_setr, NULL, NULL},
    {"r_sqr", (getter)pg_circle_getr_sqr, NULL, NULL, NULL},
    {"__safe_for_unpickling__", (getter)pg_circle_getsafepickle, NULL, NULL,
     NULL},
    {NULL, 0, NULL, NULL, NULL} /* Sentinel */
};

static PyTypeObject pgCircle_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame.Circle",
    .tp_basicsize = sizeof(pgCircleObject),
    .tp_dealloc = (destructor)pg_circle_dealloc,
    .tp_repr = (reprfunc)pg_circle_repr,
    .tp_as_number = &pg_circle_as_number,
    .tp_str = (reprfunc)pg_circle_str,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = NULL,
    .tp_richcompare = (richcmpfunc)pg_circle_richcompare,
    .tp_weaklistoffset = offsetof(pgCircleObject, weakreflist),
    .tp_methods = pg_circle_methods,
    .tp_getset = pg_circle_getsets,
    .tp_init = (initproc)pg_circle_init,
    .tp_new = pg_circle_new,
};

static int
pg_circle_init(pgCircleObject *self, PyObject *args, PyObject *kwds)
{
    pgCircle temp, s_circ = self->circle;
    pgCircle *argcirc = pgCircle_FromObject(args, &temp);

    if (!argcirc) {
        PyErr_SetString(PyExc_TypeError,
                        "Argument must be Circle style object");
        return -1;
    }
    s_circ.x = argcirc->x;
    s_circ.y = argcirc->y;
    s_circ.r = argcirc->r;
    s_circ.r_sqr = s_circ.r * s_circ.r;
    return 0;
}