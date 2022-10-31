#include "include/pygame.h"
#include "include/geometry.h"
#include "include/collisions.h"

#include <limits.h>
#include <float.h>
#include <stddef.h>
#include <math.h>

#ifndef PI
#define PI 3.14159265358979323846264
#endif

#ifndef RAD_TO_DEG
#define RAD_TO_DEG(x) (x * 180 / PI)
#endif

#define IS_LINE_VALID(line) (line->x1 != line->x2 || line->y1 != line->y2)

static double
pgLine_Length(pgLineBase *line)
{
    double dx = line->x2 - line->x1;
    double dy = line->y2 - line->y1;
    return sqrt(dx * dx + dy * dy);
}

static double
pgLine_LengthSquared(pgLineBase *line)
{
    double dx = line->x2 - line->x1;
    double dy = line->y2 - line->y1;
    return dx * dx + dy * dy;
}

static void
pgLine_At(pgLineBase *line, double t, double *X, double *Y)
{
    *X = line->x1 + t * (line->x2 - line->x1);
    *Y = line->y1 + t * (line->y2 - line->y1);
}

static PyObject *
_pg_line_subtype_new4(PyTypeObject *type, double x1, double y1, double x2,
                      double y2)
{
    pgLineObject *line = (pgLineObject *)pgLine_Type.tp_new(type, NULL, NULL);

    if (line) {
        line->line.x1 = x1;
        line->line.y1 = y1;
        line->line.x2 = x2;
        line->line.y2 = y2;
    }
    return (PyObject *)line;
}

static PyObject *
pg_line_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    pgLineObject *self = (pgLineObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->line.x1 = self->line.y1 = 0;
        self->line.x2 = self->line.y2 = 0;
        self->weakreflist = NULL;
    }
    return (PyObject *)self;
}

static void
pg_line_dealloc(pgLineObject *self)
{
    if (self->weakreflist != NULL) {
        PyObject_ClearWeakRefs((PyObject *)self);
    }

    Py_TYPE(self)->tp_free((PyObject *)self);
}

static int
pg_line_init(pgLineObject *self, PyObject *args, PyObject *kwds)
{
    if (!pgLine_FromObject(args, &(self->line))) {
        PyErr_SetString(PyExc_TypeError,
                        "Invalid line end points, expected 4 "
                        "numbers or 2 sequences of 2 numbers");
        return -1;
    }
    return 0;
}

static int
pgLine_FromObject(PyObject *obj, pgLineBase *out)
{
    Py_ssize_t length;

    if (pgLine_Check(obj)) {
        *out = ((pgLineObject *)obj)->line;
        return 1;
    }
    if (PyList_Check(obj) || PyTuple_Check(obj)) {
        length = PySequence_Fast_GET_SIZE(obj);
        PyObject **farray = PySequence_Fast_ITEMS(obj);

        if (length == 4) {
            if (!pg_DoubleFromObj(farray[0], &(out->x1)) ||
                !pg_DoubleFromObj(farray[1], &(out->y1)) ||
                !pg_DoubleFromObj(farray[2], &(out->x2)) ||
                !pg_DoubleFromObj(farray[3], &(out->y2))) {
                return 0;
            }
            return IS_LINE_VALID(out);
        }
        else if (length == 2) {
            if (!pg_TwoDoublesFromObj(farray[0], &(out->x1), &(out->y1)) ||
                !pg_TwoDoublesFromObj(farray[1], &(out->x2), &(out->y2))) {
                PyErr_Clear();
                return 0;
            }
            return IS_LINE_VALID(out);
        }
        else if (length == 1) /*looks like an arg?*/ {
            if (PyUnicode_Check(farray[0]) ||
                !pgLine_FromObject(farray[0], out)) {
                return 0;
            }
            return IS_LINE_VALID(out);
        }
    }
    if (PySequence_Check(obj)) {
        length = PySequence_Length(obj);
        if (length == 4) {
            PyObject *tmp;
            tmp = PySequence_GetItem(obj, 0);
            if (!pg_DoubleFromObj(tmp, &(out->x1))) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            tmp = PySequence_GetItem(obj, 1);
            if (!pg_DoubleFromObj(tmp, &(out->y1))) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            tmp = PySequence_GetItem(obj, 2);
            if (!pg_DoubleFromObj(tmp, &(out->x2))) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            tmp = PySequence_GetItem(obj, 3);
            if (!pg_DoubleFromObj(tmp, &(out->y2))) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            return IS_LINE_VALID(out);
        }
        else if (length == 2) {
            PyObject *tmp;
            tmp = PySequence_GetItem(obj, 0);
            if (!pg_TwoDoublesFromObj(tmp, &(out->x1), &(out->y1))) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            tmp = PySequence_GetItem(obj, 1);
            if (!pg_TwoDoublesFromObj(tmp, &(out->x2), &(out->y2))) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            return IS_LINE_VALID(out);
        }
        else if (PyTuple_Check(obj) && length == 1) /*looks like an arg?*/ {
            PyObject *sub = PySequence_GetItem(obj, 0);
            if (PyUnicode_Check(sub) || !pgLine_FromObject(sub, out)) {
                Py_DECREF(sub);
                return 0;
            }
            Py_DECREF(sub);
            return IS_LINE_VALID(out);
        }
    }
    if (PyObject_HasAttrString(obj, "line")) {
        PyObject *lineattr;
        lineattr = PyObject_GetAttrString(obj, "line");
        if (lineattr == NULL) {
            PyErr_Clear();
            return 0;
        }
        if (PyCallable_Check(lineattr)) /*call if it's a method*/
        {
            PyObject *lineresult = PyObject_CallObject(lineattr, NULL);
            Py_DECREF(lineattr);
            if (lineresult == NULL) {
                PyErr_Clear();
                return 0;
            }
            lineattr = lineresult;
        }
        Py_DECREF(lineattr);
        return pgLine_FromObject(lineattr, out);
    }
    return 0;
}

static int
pgLine_FromObjectFastcall(PyObject *const *args, Py_ssize_t nargs,
                          pgLineBase *out)
{
    if (nargs == 1) {
        return pgLine_FromObject(args[0], out);
    }
    else if (nargs == 2) {
        if (!pg_TwoDoublesFromObj(args[0], &(out->x1), &(out->y1)) ||
            !pg_TwoDoublesFromObj(args[1], &(out->x2), &(out->y2))) {
            return 0;
        }
        return IS_LINE_VALID(out);
    }
    else if (nargs == 4) {
        if (!pg_DoubleFromObj(args[0], &(out->x1)) ||
            !pg_DoubleFromObj(args[1], &(out->y1)) ||
            !pg_DoubleFromObj(args[2], &(out->x2)) ||
            !pg_DoubleFromObj(args[3], &(out->y2))) {
            return 0;
        }
        return IS_LINE_VALID(out);
    }
    return 0;
}

static PyObject *
pgLine_New(pgLineBase *l)
{
    return _pg_line_subtype_new4(&pgLine_Type, l->x1, l->y1, l->x2, l->y2);
}

static PyObject *
pgLine_New4(double x1, double y1, double x2, double y2)
{
    return _pg_line_subtype_new4(&pgLine_Type, x1, y1, x2, y2);
}

static PyObject *
pg_line_copy(pgLineObject *self, PyObject *_null)
{
    return _pg_line_subtype_new4(Py_TYPE(self), self->line.x1, self->line.y1,
                                 self->line.x2, self->line.y2);
}

static PyObject *
pg_line_is_parallel(pgLineObject *self, PyObject *const *args,
                    Py_ssize_t nargs)
{
    pgLineBase other_line;

    if (!pgLine_FromObjectFastcall(args, nargs, &other_line)) {
        return RAISE(PyExc_TypeError,
                     "Line.is_parallel requires a line or LineLike object");
    }

    double dx1 = self->line.x2 - self->line.x1;
    double dy1 = self->line.y2 - self->line.y1;
    double dx2 = other_line.x2 - other_line.x1;
    double dy2 = other_line.y2 - other_line.y1;

    double cross = dx1 * dy2 - dy1 * dx2;
    return PyBool_FromLong(cross == 0);
}

static PyObject *
pg_line_collideline(pgLineObject *self, PyObject *const *args,
                    Py_ssize_t nargs)
{
    pgLineBase B;

    if (!pgLine_FromObjectFastcall(args, nargs, &B)) {
        return RAISE(PyExc_TypeError,
                     "Line.collideline requires a line or LineLike object");
    }

    return PyBool_FromLong(pgCollision_LineLine(&self->line, &B));
}

static PyObject *
pg_line_collidepoint(pgLineObject *self, PyObject *const *args,
                     Py_ssize_t nargs)
{
    double px, py;

    if (!pg_TwoDoublesFromFastcallArgs(args, nargs, &px, &py)) {
        return RAISE(PyExc_TypeError,
                     "Line.collidepoint requires a point or PointLike object");
    }

    return PyBool_FromLong(pgCollision_LinePoint(&self->line, px, py));
}

static PyObject *
pg_line_collidecircle(pgLineObject *self, PyObject *const *args,
                      Py_ssize_t nargs)
{
    pgCircleBase circle;

    if (!pgCircle_FromObjectFastcall(args, nargs, &circle)) {
        return RAISE(
            PyExc_TypeError,
            "Line.collidecircle requires a circle or CircleLike object");
    }
    return PyBool_FromLong(pgCollision_LineCircle(&self->line, &circle));
}

static PyObject *
pg_line_as_rect(pgLineObject *self, PyObject *_null)
{
    double Ax = self->line.x1;
    double Ay = self->line.y1;
    double Bx = self->line.x2;
    double By = self->line.y2;

    int rect_x = (int)floor(MIN(Ax, Bx));
    int rect_y = (int)floor(MIN(Ay, By));

    int rect_width = (int)ceil(ABS(Ax - Bx));
    int rect_height = (int)ceil(ABS(Ay - By));

    return pgRect_New4(rect_x, rect_y, rect_width, rect_height);
}

static PyObject *
pg_line_update(pgLineObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    if (!pgLine_FromObjectFastcall(args, nargs, &(self->line))) {
        return RAISE(PyExc_TypeError,
                     "Line.update requires a line or LineLike object");
    }
    Py_RETURN_NONE;
}

static PyObject *
pg_line_colliderect(pgLineObject *self, PyObject *args)
{
    SDL_Rect *rect, temp;

    if (!(rect = pgRect_FromObject(args, &temp))) {
        return RAISE(PyExc_TypeError,
                     "Line.colliderect requires a Rect or a RectLike object");
    }
    return PyBool_FromLong(pgCollision_RectLine(rect, &self->line));
}

static PyObject *
pg_line_is_perpendicular(pgLineObject *self, PyObject *const *args,
                         Py_ssize_t nargs)
{
    pgLineBase other_line;

    if (!pgLine_FromObjectFastcall(args, nargs, &other_line)) {
        return RAISE(
            PyExc_TypeError,
            "Line.is_perpendicular requires a Line or LineLike object");
    }

    double dx1 = self->line.x2 - self->line.x1;
    double dy1 = self->line.y2 - self->line.y1;
    double dx2 = other_line.x2 - other_line.x1;
    double dy2 = other_line.y2 - other_line.y1;

    double dot = dx1 * dx2 + dy1 * dy2;

    return PyBool_FromLong(dot == 0);
}

static PyObject *
pg_line_collideswith(pgLineObject *self, PyObject *arg)
{
    int result = 0;
    if (pgLine_Check(arg)) {
        result = pgCollision_LineLine(&self->line, &pgLine_AsLine(arg));
    }
    else if (pgRect_Check(arg)) {
        result = pgCollision_RectLine(&pgRect_AsRect(arg), &self->line);
    }
    else if (pgCircle_Check(arg)) {
        result = pgCollision_LineCircle(&self->line, &pgCircle_AsCircle(arg));
    }
    else if (PySequence_Check(arg)) {
        double x, y;
        if (!pg_TwoDoublesFromObj(arg, &x, &y)) {
            return RAISE(
                PyExc_TypeError,
                "Invalid point argument, must be a sequence of 2 numbers");
        }
        result = pgCollision_LinePoint(&self->line, x, y);
    }
    else {
        return RAISE(PyExc_TypeError,
                     "Invalid shape argument, must be a CircleType, RectType, "
                     "LineType or a sequence of 2 numbers");
    }

    return PyBool_FromLong(result);
}

static PyObject *
pg_line_move(pgLineObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    double Dx, Dy;

    if (!pg_TwoDoublesFromFastcallArgs(args, nargs, &Dx, &Dy)) {
        return RAISE(PyExc_TypeError, "move requires a pair of numbers");
    }

    return _pg_line_subtype_new4(Py_TYPE(self), self->line.x1 + Dx,
                                 self->line.y1 + Dy, self->line.x2 + Dx,
                                 self->line.y2 + Dy);
}

static PyObject *
pg_line_move_ip(pgLineObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    double Dx, Dy;

    if (!pg_TwoDoublesFromFastcallArgs(args, nargs, &Dx, &Dy)) {
        return RAISE(PyExc_TypeError, "move_ip requires a pair of numbers");
    }

    self->line.x1 += Dx;
    self->line.y1 += Dy;
    self->line.x2 += Dx;
    self->line.y2 += Dy;

    Py_RETURN_NONE;
}

static PyObject *
pg_line_at(pgLineObject *self, PyObject *obj)
{
    double weight;
    double x, y;

    if (!pg_DoubleFromObj(obj, &weight)) {
        return RAISE(PyExc_TypeError,
                     "Expected a numeric value for the weight parameter");
    }

    pgLine_At(&self->line, weight, &x, &y);

    return pg_TupleFromDoublePair(x, y);
}

static struct PyMethodDef pg_line_methods[] = {
    {"__copy__", (PyCFunction)pg_line_copy, METH_NOARGS, NULL},
    {"copy", (PyCFunction)pg_line_copy, METH_NOARGS, NULL},
    {"is_parallel", (PyCFunction)pg_line_is_parallel, METH_FASTCALL, NULL},
    {"is_perpendicular", (PyCFunction)pg_line_is_perpendicular, METH_FASTCALL,
     NULL},
    {"collideline", (PyCFunction)pg_line_collideline, METH_FASTCALL, NULL},
    {"collidepoint", (PyCFunction)pg_line_collidepoint, METH_FASTCALL, NULL},
    {"collidecircle", (PyCFunction)pg_line_collidecircle, METH_FASTCALL, NULL},
    {"colliderect", (PyCFunction)pg_line_colliderect, METH_VARARGS, NULL},
    {"collideswith", (PyCFunction)pg_line_collideswith, METH_O, NULL},
    {"as_rect", (PyCFunction)pg_line_as_rect, METH_NOARGS, NULL},
    {"update", (PyCFunction)pg_line_update, METH_FASTCALL, NULL},
    {"move", (PyCFunction)pg_line_move, METH_FASTCALL, NULL},
    {"move_ip", (PyCFunction)pg_line_move_ip, METH_FASTCALL, NULL},
    {"at", (PyCFunction)pg_line_at, METH_O, NULL},
    {NULL, NULL, 0, NULL}};

/* sequence functions */

static Py_ssize_t
pg_line_seq_length(PyObject *_self)
{
    return 4;
}

static PyObject *
pg_line_item(pgLineObject *self, Py_ssize_t i)
{
    double *data = (double *)&self->line;

    if (i < 0 || i > 3) {
        if (i > -5 && i < 0) {
            i += 4;
        }
        else {
            return RAISE(PyExc_IndexError, "Invalid line Index");
        }
    }
    return PyFloat_FromDouble(data[i]);
}

static int
pg_line_ass_item(pgLineObject *self, Py_ssize_t i, PyObject *v)
{
    double val = 0;
    double *data = (double *)&self->line;

    if (i < 0 || i > 3) {
        if (i > -5 && i < 0) {
            i += 4;
        }
        else {
            PyErr_SetString(PyExc_IndexError, "Invalid line Index");
            return -1;
        }
    }
    if (!pg_DoubleFromObj(v, &val)) {
        PyErr_SetString(PyExc_TypeError, "Must assign numeric values");
        return -1;
    }
    data[i] = val;
    return 0;
}

static int
pg_line_contains_seq(pgLineObject *self, PyObject *arg)
{
    if (PyNumber_Check(arg)) {
        double coord = PyFloat_AsDouble(arg);
        return coord == self->line.x1 || coord == self->line.y1 ||
               coord == self->line.x2 || coord == self->line.y1;
    }

    pgLineBase B;
    if (!pgLine_FromObject(arg, &B)) {
        PyErr_SetString(PyExc_TypeError,
                        "'in <pygame.Line>' requires line style object"
                        " or int as left operand");
        return 0;
    }

    return pgCollision_LineLine(&(self->line), &B);
}

static PySequenceMethods pg_line_as_sequence = {
    .sq_length = pg_line_seq_length,
    .sq_item = (ssizeargfunc)pg_line_item,
    .sq_ass_item = (ssizeobjargproc)pg_line_ass_item,
    .sq_contains = (objobjproc)pg_line_contains_seq,
};

static PyObject *
pg_line_subscript(pgLineObject *self, PyObject *op)
{
    double *data = (double *)&self->line;

    if (PyIndex_Check(op)) {
        PyObject *index = PyNumber_Index(op);
        Py_ssize_t i;

        if (index == NULL) {
            return NULL;
        }
        i = PyNumber_AsSsize_t(index, NULL);
        Py_DECREF(index);
        return pg_line_item(self, i);
    }
    else if (op == Py_Ellipsis) {
        PyObject *lst = PyList_New(4);

        if (lst == NULL) {
            return NULL;
        }

        PyList_SET_ITEM(lst, 0, PyFloat_FromDouble(data[0]));
        PyList_SET_ITEM(lst, 1, PyFloat_FromDouble(data[1]));
        PyList_SET_ITEM(lst, 2, PyFloat_FromDouble(data[2]));
        PyList_SET_ITEM(lst, 3, PyFloat_FromDouble(data[3]));

        return lst;
    }
    else if (PySlice_Check(op)) {
        PyObject *slice;
        Py_ssize_t start;
        Py_ssize_t stop;
        Py_ssize_t step;
        Py_ssize_t slicelen;
        Py_ssize_t i;
        PyObject *n;

        if (PySlice_GetIndicesEx(op, 4, &start, &stop, &step, &slicelen)) {
            return NULL;
        }

        slice = PyList_New(slicelen);
        if (slice == NULL) {
            return NULL;
        }
        for (i = 0; i < slicelen; ++i) {
            n = PyFloat_FromDouble(data[start + (step * i)]);
            if (n == NULL) {
                Py_DECREF(slice);
                return NULL;
            }
            PyList_SET_ITEM(slice, i, n);
        }
        return slice;
    }

    return RAISE(PyExc_TypeError, "Invalid Line slice");
}

static int
pg_line_ass_subscript(pgLineObject *self, PyObject *op, PyObject *value)
{
    if (PyIndex_Check(op)) {
        PyObject *index;
        Py_ssize_t i;

        index = PyNumber_Index(op);
        if (index == NULL) {
            return -1;
        }
        i = PyNumber_AsSsize_t(index, NULL);
        Py_DECREF(index);
        return pg_line_ass_item(self, i, value);
    }
    else if (op == Py_Ellipsis) {
        double val = 0;

        if (pg_DoubleFromObj(value, &val)) {
            self->line.x1 = val;
            self->line.y1 = val;
            self->line.x2 = val;
            self->line.y2 = val;
        }
        else if (PyObject_IsInstance(value, (PyObject *)&pgLine_Type)) {
            pgLineObject *line = (pgLineObject *)value;

            self->line.x1 = line->line.x1;
            self->line.y1 = line->line.y1;
            self->line.x2 = line->line.x2;
            self->line.y2 = line->line.y2;
        }
        else if (PySequence_Check(value)) {
            PyObject *item;
            double values[4];
            Py_ssize_t i;

            if (PySequence_Size(value) != 4) {
                PyErr_SetString(PyExc_TypeError, "Expect a length 4 sequence");
                return -1;
            }
            for (i = 0; i < 4; ++i) {
                item = PySequence_ITEM(value, i);
                if (!pg_DoubleFromObj(item, values + i)) {
                    PyErr_Format(PyExc_TypeError,
                                 "Expected a number between %lf and %lf",
                                 DBL_MIN, DBL_MAX);
                }
            }
            self->line.x1 = values[0];
            self->line.y1 = values[1];
            self->line.x2 = values[2];
            self->line.y2 = values[3];
        }
        else {
            PyErr_SetString(PyExc_TypeError, "Expected a number or sequence");
            return -1;
        }
    }
    else if (PySlice_Check(op)) {
        double *data = (double *)&self->line;
        Py_ssize_t start;
        Py_ssize_t stop;
        Py_ssize_t step;
        Py_ssize_t slicelen;
        double val = 0;
        Py_ssize_t i;

        if (PySlice_GetIndicesEx(op, 4, &start, &stop, &step, &slicelen)) {
            return -1;
        }

        if (pg_DoubleFromObj(value, &val)) {
            for (i = 0; i < slicelen; ++i) {
                data[start + step * i] = val;
            }
        }
        else if (PySequence_Check(value)) {
            PyObject *item;
            double values[4];
            Py_ssize_t size = PySequence_Size(value);

            if (size != slicelen) {
                PyErr_Format(PyExc_TypeError, "Expected a length %zd sequence",
                             slicelen);
                return -1;
            }
            for (i = 0; i < slicelen; ++i) {
                item = PySequence_ITEM(value, i);
                if (!pg_DoubleFromObj(item, values + i)) {
                    PyErr_Format(PyExc_TypeError,
                                 "Expected a number between %lf and %lf",
                                 DBL_MIN, DBL_MAX);
                }
            }
            for (i = 0; i < slicelen; ++i) {
                data[start + step * i] = values[i];
            }
        }
        else {
            PyErr_SetString(PyExc_TypeError, "Expected a number or sequence");
            return -1;
        }
    }
    else {
        PyErr_SetString(PyExc_TypeError, "Invalid Line slice");
        return -1;
    }
    return 0;
}

static PyMappingMethods pg_line_as_mapping = {
    .mp_length = (lenfunc)pg_line_seq_length,
    .mp_subscript = (binaryfunc)pg_line_subscript,
    .mp_ass_subscript = (objobjargproc)pg_line_ass_subscript,
};

/* numeric functions */
static int
pg_line_bool(pgLineObject *self)
{
    return 1;
}

static PyNumberMethods pg_line_as_number = {
    .nb_bool = (inquiry)pg_line_bool,
};

static PyObject *
pg_line_repr(pgLineObject *self)
{
    PyObject *result, *x1, *y1, *x2, *y2;

    x1 = PyFloat_FromDouble(self->line.x1);
    if (!x1) {
        return NULL;
    }
    y1 = PyFloat_FromDouble(self->line.y1);
    if (!y1) {
        Py_DECREF(x1);
        return NULL;
    }
    x2 = PyFloat_FromDouble(self->line.x2);
    if (!x2) {
        Py_DECREF(x1);
        Py_DECREF(y1);
        return NULL;
    }
    y2 = PyFloat_FromDouble(self->line.y2);
    if (!y2) {
        Py_DECREF(x1);
        Py_DECREF(y1);
        Py_DECREF(x2);
        return NULL;
    }

    result =
        PyUnicode_FromFormat("<Line((%R, %R), (%R, %R))>", x1, y1, x2, y2);

    Py_DECREF(x1);
    Py_DECREF(y1);
    Py_DECREF(x2);
    Py_DECREF(y2);

    return result;
}

static PyObject *
pg_line_str(pgLineObject *self)
{
    return pg_line_repr(self);
}

static PyObject *
pg_line_richcompare(PyObject *o1, PyObject *o2, int opid)
{
    pgLineBase o1line, o2line;
    double length1, length2;

    if (!pgLine_FromObject(o1, &o1line) || !pgLine_FromObject(o2, &o2line)) {
        goto Unimplemented;
    }

    length1 = pgLine_Length(&o1line);
    length2 = pgLine_Length(&o2line);

    switch (opid) {
        case Py_LT:
            return PyBool_FromLong(length1 < length2);
        case Py_LE:
            return PyBool_FromLong(length1 <= length2);
        case Py_EQ:
            return PyBool_FromLong(length1 == length2);
        case Py_NE:
            return PyBool_FromLong(length1 != length2);
        case Py_GT:
            return PyBool_FromLong(length1 > length2);
        case Py_GE:
            return PyBool_FromLong(length1 >= length2);
        default:
            break;
    }

Unimplemented:
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
}

static PyObject *
pg_line_iterator(pgLineObject *self)
{
    Py_ssize_t i;
    double *data = (double *)&self->line;
    PyObject *iter, *tup = PyTuple_New(4);
    if (!tup) {
        return NULL;
    }
    for (i = 0; i < 4; i++) {
        PyObject *val = PyFloat_FromDouble(data[i]);
        if (!val) {
            Py_DECREF(tup);
            return NULL;
        }

        PyTuple_SET_ITEM(tup, i, val);
    }
    iter = PyTuple_Type.tp_iter(tup);
    Py_DECREF(tup);
    return iter;
}

#define __LINE_GETSET_NAME(name)                                          \
    static PyObject *pg_line_get##name(pgLineObject *self, void *closure) \
    {                                                                     \
        return PyFloat_FromDouble(self->line.name);                       \
    }                                                                     \
    static int pg_line_set##name(pgLineObject *self, PyObject *value,     \
                                 void *closure)                           \
    {                                                                     \
        double val;                                                       \
        DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);                      \
        if (pg_DoubleFromObj(value, &val)) {                              \
            self->line.name = val;                                        \
            return 0;                                                     \
        }                                                                 \
        PyErr_SetString(PyExc_TypeError, "Expected a number");            \
        return -1;                                                        \
    }

// they are repetitive enough that we can abstract them like this
__LINE_GETSET_NAME(x1)
__LINE_GETSET_NAME(y1)
__LINE_GETSET_NAME(x2)
__LINE_GETSET_NAME(y2)
#undef __LINE_GETSET_NAME

static PyObject *
pg_line_geta(pgLineObject *self, void *closure)
{
    return pg_TupleFromDoublePair(self->line.x1, self->line.y1);
}

static int
pg_line_seta(pgLineObject *self, PyObject *value, void *closure)
{
    double x, y;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (pg_TwoDoublesFromObj(value, &x, &y)) {
        self->line.x1 = x;
        self->line.y1 = y;
        return 0;
    }
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
    return -1;
}

static PyObject *
pg_line_getb(pgLineObject *self, void *closure)
{
    return pg_TupleFromDoublePair(self->line.x2, self->line.y2);
}

static int
pg_line_setb(pgLineObject *self, PyObject *value, void *closure)
{
    double x, y;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (pg_TwoDoublesFromObj(value, &x, &y)) {
        self->line.x2 = x;
        self->line.y2 = y;
        return 0;
    }
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
    return -1;
}

static PyObject *
pg_line_getangle(pgLineObject *self, void *closure)
{
    double dx = self->line.x2 - self->line.x1;

    if (dx == 0.0)
        return (self->line.y2 > self->line.y1) ? PyFloat_FromDouble(-90.0)
                                               : PyFloat_FromDouble(90.0);

    double dy = self->line.y2 - self->line.y1;

    double gradient = (dy / dx);
    return PyFloat_FromDouble(-RAD_TO_DEG(atan(gradient)));
}

static PyObject *
pg_line_getlength(pgLineObject *self, void *closure)
{
    return PyFloat_FromDouble(pgLine_Length(&self->line));
}

static PyObject *
pg_line_getslope(pgLineObject *self, void *closure)
{
    double dem = self->line.x2 - self->line.x1;
    if (dem == 0) {
        return PyFloat_FromDouble(0);
    }

    double slope = (self->line.y2 - self->line.y1) / dem;
    return PyFloat_FromDouble(slope);
}

static PyObject *
pg_line_getsafepickle(pgLineObject *self, void *closure)
{
    Py_RETURN_TRUE;
}

static PyObject *
pg_line_get_midpoint(pgLineObject *self, void *closure)
{
    return pg_TupleFromDoublePair((self->line.x1 + self->line.x2) / 2,
                                  (self->line.y1 + self->line.y2) / 2);
}

static int
pg_line_set_midpoint(pgLineObject *self, PyObject *value, void *closure)
{
    double m_x, m_y;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (!pg_TwoDoublesFromObj(value, &m_x, &m_y)) {
        PyErr_SetString(
            PyExc_TypeError,
            "Invalid midpoint value, expected a sequence of 2 numbers");
        return -1;
    }

    double dx = m_x - (self->line.x1 + self->line.x2) / 2;
    double dy = m_y - (self->line.y1 + self->line.y2) / 2;

    self->line.x1 += dx;
    self->line.y1 += dy;
    self->line.x2 += dx;
    self->line.y2 += dy;

    return 0;
}

static PyObject *
pg_line_get_midpoint_x(pgLineObject *self, void *closure)
{
    return PyFloat_FromDouble((self->line.x1 + self->line.x2) / 2);
}

static int
pg_line_set_midpoint_x(pgLineObject *self, PyObject *value, void *closure)
{
    double m_x;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (!pg_DoubleFromObj(value, &m_x)) {
        PyErr_SetString(PyExc_TypeError,
                        "Invalid midpoint_x value, expected a numeric value");
        return -1;
    }

    double dx = m_x - (self->line.x1 + self->line.x2) / 2;
    self->line.x1 += dx;
    self->line.x2 += dx;
    return 0;
}

static PyObject *
pg_line_get_midpoint_y(pgLineObject *self, void *closure)
{
    return PyFloat_FromDouble((self->line.y1 + self->line.y2) / 2);
}

static int
pg_line_set_midpoint_y(pgLineObject *self, PyObject *value, void *closure)
{
    double m_y;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (!pg_DoubleFromObj(value, &m_y)) {
        PyErr_SetString(PyExc_TypeError,
                        "Invalid midpoint_y value, expected a numeric value");
        return -1;
    }

    double dy = m_y - (self->line.y1 + self->line.y2) / 2;
    self->line.y1 += dy;
    self->line.y2 += dy;
    return 0;
}

static PyGetSetDef pg_line_getsets[] = {
    {"x1", (getter)pg_line_getx1, (setter)pg_line_setx1, NULL, NULL},
    {"y1", (getter)pg_line_gety1, (setter)pg_line_sety1, NULL, NULL},
    {"x2", (getter)pg_line_getx2, (setter)pg_line_setx2, NULL, NULL},
    {"y2", (getter)pg_line_gety2, (setter)pg_line_sety2, NULL, NULL},
    {"a", (getter)pg_line_geta, (setter)pg_line_seta, NULL, NULL},
    {"b", (getter)pg_line_getb, (setter)pg_line_setb, NULL, NULL},
    {"length", (getter)pg_line_getlength, NULL, NULL, NULL},
    {"slope", (getter)pg_line_getslope, NULL, NULL, NULL},
    {"midpoint", (getter)pg_line_get_midpoint, (setter)pg_line_set_midpoint,
     NULL, NULL},
    {"midpoint_x", (getter)pg_line_get_midpoint_x,
     (setter)pg_line_set_midpoint_x, NULL, NULL},
    {"midpoint_y", (getter)pg_line_get_midpoint_y,
     (setter)pg_line_set_midpoint_y, NULL, NULL},
    {"angle", (getter)pg_line_getangle, NULL, NULL, NULL},
    {"__safe_for_unpickling__", (getter)pg_line_getsafepickle, NULL, NULL,
     NULL},
    {NULL, 0, NULL, NULL, NULL} /* Sentinel */
};

static PyTypeObject pgLine_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame.Line",
    .tp_basicsize = sizeof(pgLineObject),
    .tp_dealloc = (destructor)pg_line_dealloc,
    .tp_repr = (reprfunc)pg_line_repr,
    .tp_as_number = &pg_line_as_number,
    .tp_as_sequence = &pg_line_as_sequence,
    .tp_as_mapping = &pg_line_as_mapping,
    .tp_str = (reprfunc)pg_line_str,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = NULL,
    .tp_richcompare = (richcmpfunc)pg_line_richcompare,
    .tp_weaklistoffset = offsetof(pgLineObject, weakreflist),
    .tp_iter = (getiterfunc)pg_line_iterator,
    .tp_methods = pg_line_methods,
    .tp_getset = pg_line_getsets,
    .tp_init = (initproc)pg_line_init,
    .tp_new = pg_line_new,
};
