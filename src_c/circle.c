#include "include/pygame.h"
#include "include/geometry.h"
#include "include/collisions.h"

#include <limits.h>
#include <float.h>
#include <stddef.h>
#include <math.h>

#define PI 3.14159265358979323846264
#define TAU 6.28318530717958647692528

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
_pg_circle_set_radius(PyObject *value, pgCircleBase *circle)
{
    double tmp = 0;
    if (!pg_DoubleFromObj(value, &tmp) || tmp < 0)
        return 0;
    circle->r = tmp;
    circle->r_sqr = tmp * tmp;
    return 1;
}

static int
pgCircle_FromObject(PyObject *obj, pgCircleBase *out)
{
    Py_ssize_t length;

    if (pgCircle_Check(obj)) {
        memcpy(out, &((pgCircleObject *)obj)->circle, sizeof(pgCircleBase));
        return 1;
    }

    if (PySequence_FAST_CHECK(obj)) {
        PyObject **f_arr = PySequence_Fast_ITEMS(obj);
        length = PySequence_Fast_GET_SIZE(obj);

        if (length == 3) {
            if (!pg_DoubleFromObj(f_arr[0], &(out->x)) ||
                !pg_DoubleFromObj(f_arr[1], &(out->y)) ||
                !_pg_circle_set_radius(f_arr[2], out)) {
                return 0;
            }
            return 1;
        }
        else if (length == 1) {
            if (!pgCircle_FromObject(f_arr[0], out)) {
                return 0;
            }
            return 1;
        }
        else if (length == 2) {
            if (!pg_TwoDoublesFromObj(f_arr[0], &(out->x), &(out->y)) ||
                !_pg_circle_set_radius(f_arr[1], out)) {
                return 0;
            }
            return 1;
        }
        else {
            /* Sequences of size other than 3 or 1 are not supported
            (don't wanna support infinite sequence nesting anymore)*/
            return 0;
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
            if (!pg_DoubleFromObj(tmp, &(out->x))) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);

            tmp = PySequence_ITEM(obj, 1);
            if (!pg_DoubleFromObj(tmp, &(out->y))) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);

            tmp = PySequence_ITEM(obj, 2);
            if (!_pg_circle_set_radius(tmp, out)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);

            return 1;
        }
        else if (length == 2) {
            tmp = PySequence_ITEM(obj, 0);
            if (!pg_TwoDoublesFromObj(tmp, &(out->x), &(out->y))) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);

            tmp = PySequence_ITEM(obj, 1);
            if (!_pg_circle_set_radius(tmp, out)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);

            return 1;
        }
        else if (length == 1) {
            tmp = PySequence_ITEM(obj, 0);
            if (PyUnicode_Check(obj) || !pgCircle_FromObject(tmp, out)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            return 1;
        }
        else {
            /* Sequences of size other than 3 or 1 are not supported
            (don't wanna support infinite sequence nesting anymore)*/
            return 0;
        }
    }

    if (PyObject_HasAttrString(obj, "circle")) {
        PyObject *circleattr;
        circleattr = PyObject_GetAttrString(obj, "circle");
        if (circleattr == NULL) {
            PyErr_Clear();
            return 0;
        }
        if (PyCallable_Check(circleattr)) /*call if it's a method*/
        {
            PyObject *circleresult = PyObject_CallObject(circleattr, NULL);
            Py_DECREF(circleattr);
            if (circleresult == NULL) {
                PyErr_Clear();
                return 0;
            }
            circleattr = circleresult;
        }
        if (!pgCircle_FromObject(circleattr, out)) {
            PyErr_Clear();
            Py_DECREF(circleattr);
            return 0;
        }
        Py_DECREF(circleattr);

        return 1;
    }
    return 0;
}

static int
pgCircle_FromObjectFastcall(PyObject *const *args, Py_ssize_t nargs,
                            pgCircleBase *out)
{
    if (nargs == 1) {
        return pgCircle_FromObject(args[0], out);
    }
    else if (nargs == 2) {
        if (!pg_TwoDoublesFromObj(args[0], &(out->x), &(out->y)) ||
            !_pg_circle_set_radius(args[1], out)) {
            return 0;
        }
        return 1;
    }
    else if (nargs == 3) {
        if (!pg_DoubleFromObj(args[0], &(out->x)) ||
            !pg_DoubleFromObj(args[1], &(out->y)) ||
            !_pg_circle_set_radius(args[2], out)) {
            return 0;
        }
        return 1;
    }

    return 0;
}

static PyObject *
pgCircle_New(pgCircleBase *c)
{
    return _pg_circle_subtype_new3(&pgCircle_Type, c->x, c->y, c->r);
}

static PyObject *
pgCircle_New3(double x, double y, double r)
{
    return _pg_circle_subtype_new3(&pgCircle_Type, x, y, r);
}

static PyObject *
pg_circle_copy(pgCircleObject *self, PyObject *_null)
{
    return _pg_circle_subtype_new3(Py_TYPE(self), self->circle.x,
                                   self->circle.y, self->circle.r);
}

static PyObject *
pg_circle_collidecircle(pgCircleObject *self, PyObject *const *args,
                        Py_ssize_t nargs)
{
    pgCircleBase other_circle;
    if (!pgCircle_FromObjectFastcall(args, nargs, &other_circle)) {
        return RAISE(PyExc_TypeError, "A CircleType object was expected");
    }
    return PyBool_FromLong(
        pgCollision_CircleCircle(&(self->circle), &other_circle));
}

static PyObject *
pg_circle_collideline(pgCircleObject *self, PyObject *const *args,
                      Py_ssize_t nargs)
{
    pgLineBase line;
    if (!pgLine_FromObjectFastcall(args, nargs, &line)) {
        return RAISE(PyExc_TypeError, "A CircleType object was expected");
    }
    return PyBool_FromLong(pgCollision_LineCircle(&line, &(self->circle)));
}

static PyObject *
pg_circle_collidepoint(pgCircleObject *self, PyObject *const *args,
                       Py_ssize_t nargs)
{
    double px = 0, py = 0;

    if (nargs == 1) {
        if (!pg_TwoDoublesFromObj(args[0], &px, &py)) {
            goto error;
        }
    }
    else if (nargs == 2) {
        if (!pg_DoubleFromObj(args[0], &px) ||
            !pg_DoubleFromObj(args[1], &py)) {
            goto error;
        }
    }
    else {
        return RAISE(PyExc_TypeError,
                     "Invalid arguments number, can be at most 2");
    }

    return PyBool_FromLong(pgCollision_CirclePoint(&(self->circle), px, py));

error:
    return RAISE(PyExc_TypeError,
                 "collidepoint requires a point or PointLike object");
}
static PyObject *
pg_circle_colliderect(pgCircleObject *self, PyObject *const *args,
                      Py_ssize_t nargs)
{
    SDL_Rect temp;

    if (nargs == 1) {
        SDL_Rect *tmp;
        if (!(tmp = pgRect_FromObject(args[0], &temp))) {
            if (PyErr_Occurred())
                return NULL;
            else
                return RAISE(PyExc_TypeError,
                             "Invalid rect, all 4 fields must be numeric");
        }
        return PyBool_FromLong(pgCollision_RectCircle(tmp, &(self->circle)));
    }
    else if (nargs == 2) {
        if (!pg_TwoIntsFromObj(args[0], &temp.x, &temp.y) ||
            !pg_TwoIntsFromObj(args[1], &temp.w, &temp.h)) {
            return RAISE(PyExc_TypeError,
                         "Invalid rect, all 4 fields must be numeric");
        }
    }
    else if (nargs == 4) {
        if (!pg_IntFromObj(args[0], &temp.x) ||
            !pg_IntFromObj(args[1], &temp.y) ||
            !pg_IntFromObj(args[2], &temp.w) ||
            !pg_IntFromObj(args[3], &temp.h)) {
            return RAISE(PyExc_TypeError,
                         "Invalid rect, all 4 fields must be numeric");
        }
    }
    else {
        return RAISE(PyExc_TypeError,
                     "Invalid arguments number, must be 1, 2 or 4");
    }

    return PyBool_FromLong(pgCollision_RectCircle(&temp, &(self->circle)));
}

static PyObject *
pg_circle_collideswith(pgCircleObject *self, PyObject *arg)
{
    int result = 0;
    if (pgCircle_Check(arg)) {
        result =
            pgCollision_CircleCircle(&self->circle, &pgCircle_AsCircle(arg));
    }
    else if (pgRect_Check(arg)) {
        result = pgCollision_RectCircle(&pgRect_AsRect(arg), &self->circle);
    }
    else if (pgLine_Check(arg)) {
        result = pgCollision_LineCircle(&pgLine_AsLine(arg), &self->circle);
    }
    else if (PySequence_Check(arg)) {
        double x, y;
        if (!pg_TwoDoublesFromObj(arg, &x, &y)) {
            return RAISE(
                PyExc_TypeError,
                "Invalid point argument, must be a sequence of 2 numbers");
        }
        result = pgCollision_CirclePoint(&self->circle, x, y);
    }
    else {
        return RAISE(PyExc_TypeError,
                     "Invalid shape argument, must be a CircleType, RectType, "
                     "LineType or a sequence of 2 numbers");
    }

    return PyBool_FromLong(result);
}

static PyObject *
pg_circle_as_rect(pgCircleObject *self, PyObject *_null)
{
    pgCircleBase scirc = self->circle;
    int diameter = (int)(2 * scirc.r);
    int x = (int)(scirc.x - scirc.r);
    int y = (int)(scirc.y - scirc.r);

    return pgRect_New4(x, y, diameter, diameter);
}

static PyObject *
pg_circle_update(pgCircleObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    if (!pgCircle_FromObjectFastcall(args, nargs, &(self->circle))) {
        PyErr_SetString(
            PyExc_TypeError,
            "Circle.update requires a circle or CircleLike object");
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyObject *
pg_circle_move(pgCircleObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    double Dx = 0, Dy = 0;

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

    return _pg_circle_subtype_new3(Py_TYPE(self), self->circle.x + Dx,
                                   self->circle.y + Dy, self->circle.r);
error:
    return RAISE(PyExc_TypeError, "move requires a pair of numbers");
}

static PyObject *
pg_circle_move_ip(pgCircleObject *self, PyObject *const *args,
                  Py_ssize_t nargs)
{
    double Dx = 0, Dy = 0;

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

    self->circle.x += Dx;
    self->circle.y += Dy;

    Py_RETURN_NONE;

error:
    return RAISE(PyExc_TypeError, "move_ip requires a pair of numbers");
}

static struct PyMethodDef pg_circle_methods[] = {
    {"collidecircle", (PyCFunction)pg_circle_collidecircle, METH_FASTCALL,
     NULL},
    {"collideline", (PyCFunction)pg_circle_collideline, METH_FASTCALL, NULL},
    {"collidepoint", (PyCFunction)pg_circle_collidepoint, METH_FASTCALL, NULL},
    {"colliderect", (PyCFunction)pg_circle_colliderect, METH_FASTCALL, NULL},
    {"collideswith", (PyCFunction)pg_circle_collideswith, METH_O, NULL},
    {"as_rect", (PyCFunction)pg_circle_as_rect, METH_NOARGS, NULL},
    {"update", (PyCFunction)pg_circle_update, METH_FASTCALL, NULL},
    {"move", (PyCFunction)pg_circle_move, METH_FASTCALL, NULL},
    {"move_ip", (PyCFunction)pg_circle_move_ip, METH_FASTCALL, NULL},
    {"__copy__", (PyCFunction)pg_circle_copy, METH_NOARGS, NULL},
    {"copy", (PyCFunction)pg_circle_copy, METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL}};

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
    pgCircleBase o1_circ, o2_circ;
    double r1, r2;

    if (!pgCircle_FromObject(o1, &o1_circ) ||
        !pgCircle_FromObject(o1, &o2_circ)) {
        PyErr_SetString(PyExc_TypeError,
                        "Argument must be Circle style object");
        return NULL;
    }

    r1 = o1_circ.r;
    r2 = o2_circ.r;

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
    return NULL;
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
        PyErr_SetString(PyExc_TypeError, "Expected a number");                \
        return -1;                                                            \
    }

// they are repetitive enough that we can abstract them like this
GETSET_FOR_SIMPLE(x)
GETSET_FOR_SIMPLE(y)

#undef GETSET_FOR_SIMPLE

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

    if (!pg_DoubleFromObj(value, &val) || val < 0) {
        PyErr_SetString(PyExc_TypeError, "Expected a positive number");
        return -1;
    }

    self->circle.r = val;
    self->circle.r_sqr = val * val;
    return 0;
}

static PyObject *
pg_circle_getr_sqr(pgCircleObject *self, void *closure)
{
    return PyFloat_FromDouble(self->circle.r_sqr);
}

static int
pg_circle_setr_sqr(pgCircleObject *self, PyObject *value, void *closure)
{
    double val;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    if (!pg_DoubleFromObj(value, &val) || val < 0) {
        PyErr_SetString(PyExc_TypeError, "Expected a positive number");
        return -1;
    }

    self->circle.r_sqr = val;
    self->circle.r = sqrt(val);
    return 0;
}

static PyObject *
pg_circle_getcenter(pgCircleObject *self, void *closure)
{
    return pg_TupleFromDoublePair(self->circle.x, self->circle.y);
}

static int
pg_circle_setcenter(pgCircleObject *self, PyObject *value, void *closure)
{
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (!pg_TwoDoublesFromObj(value, &(self->circle.x), &(self->circle.y))) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
        return -1;
    }
    return 0;
}

static PyObject *
pg_circle_getarea(pgCircleObject *self, void *closure)
{
    return PyFloat_FromDouble(PI * self->circle.r_sqr);
}

static int
pg_circle_setarea(pgCircleObject *self, PyObject *value, void *closure)
{
    double val;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (!pg_DoubleFromObj(value, &val) || val <= 0) {
        PyErr_SetString(PyExc_TypeError, "Expected a positive number");
        return -1;
    }
    self->circle.r_sqr = val / PI;
    self->circle.r = sqrt(self->circle.r_sqr);
    return 0;
}

static PyObject *
pg_circle_getcircumference(pgCircleObject *self, void *closure)
{
    return PyFloat_FromDouble(TAU * self->circle.r);
}

static int
pg_circle_setcircumference(pgCircleObject *self, PyObject *value,
                           void *closure)
{
    double val;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (!pg_DoubleFromObj(value, &val) || val <= 0) {
        PyErr_SetString(PyExc_TypeError, "Expected a positive number");
        return -1;
    }
    self->circle.r = val / TAU;
    self->circle.r_sqr = self->circle.r * self->circle.r;

    return 0;
}

static PyObject *
pg_circle_getdiameter(pgCircleObject *self, void *closure)
{
    return PyFloat_FromDouble(2 * self->circle.r);
}

static int
pg_circle_setdiameter(pgCircleObject *self, PyObject *value, void *closure)
{
    double val;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (!pg_DoubleFromObj(value, &val) || val <= 0) {
        PyErr_SetString(PyExc_TypeError, "Expected a positive number");
        return -1;
    }
    self->circle.r = val / 2;
    self->circle.r_sqr = self->circle.r * self->circle.r;
    return 0;
}

static PyObject *
pg_circle_getsafepickle(pgCircleObject *self, void *closure)
{
    Py_RETURN_TRUE;
}

static int
pg_circle_init(pgCircleObject *self, PyObject *args, PyObject *kwds)
{
    if (!pgCircle_FromObject(args, &(self->circle))) {
        PyErr_SetString(PyExc_TypeError,
                        "Argument must be Circle style object");
        return -1;
    }

    return 0;
}

static PyGetSetDef pg_circle_getsets[] = {
    {"x", (getter)pg_circle_getx, (setter)pg_circle_setx, NULL, NULL},
    {"y", (getter)pg_circle_gety, (setter)pg_circle_sety, NULL, NULL},
    {"r", (getter)pg_circle_getr, (setter)pg_circle_setr, NULL, NULL},
    {"r_sqr", (getter)pg_circle_getr_sqr, (setter)pg_circle_setr_sqr, NULL,
     NULL},
    {"d", (getter)pg_circle_getdiameter, (setter)pg_circle_setdiameter, NULL,
     NULL},
    {"diameter", (getter)pg_circle_getdiameter, (setter)pg_circle_setdiameter,
     NULL, NULL},
    {"center", (getter)pg_circle_getcenter, (setter)pg_circle_setcenter, NULL,
     NULL},
    {"area", (getter)pg_circle_getarea, (setter)pg_circle_setarea, NULL, NULL},
    {"circumference", (getter)pg_circle_getcircumference,
     (setter)pg_circle_setcircumference, NULL, NULL},
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