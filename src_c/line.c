#include "include/pygame.h"
#include "include/line.h"
#include "include/base.h"

#include <limits.h>
#include <math.h>

static PyTypeObject pgLine_Type;
#define pgLine_Check(x) ((x)->ob_type == &pgLine_Type)


static pgLineBase*
pgLine_FromObject(PyObject *obj, pgLineBase* temp);

// return 1 if they intersect, 0 if not
int pgLine_GetIntersectionPoint(
    double x1, double y1, double x2, double y2,
    double x3, double y3, double x4, double y4,
    double *X, double *Y
) { 
    double x1_m_x2 = x1 - x2;
    double y3_m_y4 = y3 - y4;
    double y1_m_y2 = y1 - y2;
    double x3_m_x4 = x3 - x4;
    
    double den = x1_m_x2 * y3_m_y4 - y1_m_y2 * x3_m_x4;

    if (!den) {
        return 0;
    }

    double x1_m_x3 = x1 - x3;
    double y1_m_y3 = y1 - y3;

    double t1 = x1_m_x3 * y3_m_y4 - y1_m_y3 * x3_m_x4;
    double t = t1 / den;

    double u1 = x1_m_x2 * y1_m_y3 - y1_m_y2 * x1_m_x3;
    double u = -(u1 / den);

    if (t >= 0 && t <= 1 && u >= 0 && u <= 1) {
        *X = x1 + t * (x2 - x1);
        *Y = y1 + t * (y2 - y1);
        return 1;
    }
    return 0;
}

static int
_pg_line_contains(pgLineObject *self, PyObject *arg) {
    pgLineBase *argline, temp_line;
    if (!(argline = pgLine_FromObject(arg, &temp_line))) {
        return -1;
    }
    
    double x1_m_x2 = self->line.x1 - self->line.x2;
    double y3_m_y4 = argline->y1 - argline->y2;
    double y1_m_y2 = self->line.y1 - self->line.y2;
    double x3_m_x4 = argline->x1 - argline->x2;
    
    double den = x1_m_x2 * y3_m_y4 - y1_m_y2 * x3_m_x4;

    if (!den) {
        return 0;
    }

    double x1_m_x3 = self->line.x1 - argline->x1;
    double y1_m_y3 = self->line.y1 - argline->y1;

    double t1 = x1_m_x3 * y3_m_y4 - y1_m_y3 * x3_m_x4;
    double t = t1 / den;

    double u1 = x1_m_x2 * y1_m_y3 - y1_m_y2 * x1_m_x3;
    double u = -(u1 / den);

    return t >= 0 && t <= 1 && u >= 0 && u <= 1;
}

static double
_pg_line_length(pgLineBase line) {
    return sqrt(
        (line.x2 - line.x1) * (line.x2 - line.x1) +
        (line.y2 - line.y1) * (line.y2 - line.y1)
    );
}

static int
pg_line_init(pgLineObject *, PyObject *, PyObject *);

static PyObject *
_pg_line_subtype_new4(PyTypeObject *type, double x1, double y1, double x2, double y2) {
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
pg_line_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    pgLineObject *self = (pgLineObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->line.x1 = self->line.y1 = 0;
        self->line.x2 = self->line.y2 = 0;
        self->weakreflist = NULL;
    }
    return (PyObject *)self;
}

static void
pg_line_dealloc(pgLineObject *self) {
    if (self->weakreflist != NULL) {
        PyObject_ClearWeakRefs((PyObject *)self);
    }

    Py_TYPE(self)->tp_free((PyObject *)self);
}

static pgLineBase*
pgLine_FromObject(PyObject *obj, pgLineBase* temp) {
    Py_ssize_t length;

    if (pgLine_Check(obj)) {
        return &((pgLineObject *)obj)->line;
    }
    if (PyList_Check(obj) || PyTuple_Check(obj)) {
        PyObject **f_arr = PySequence_Fast_ITEMS(obj);
        length = PySequence_Fast_GET_SIZE(obj);

        if (length == 4) {
            if (!pg_DoubleFromObj(f_arr[0], &(temp->x1)) ||
                !pg_DoubleFromObj(f_arr[1], &(temp->y1)) ||
                !pg_DoubleFromObj(f_arr[2], &(temp->x2)) ||
                !pg_DoubleFromObj(f_arr[3], &(temp->y2))) {
                return NULL;
            }
            return temp;
        }
        else if (length == 2) {
            if (!pg_TwoDoublesFromObj(f_arr[0], &(temp->x1), &(temp->y1)) ||
                !pg_TwoDoublesFromObj(f_arr[1], &(temp->x2), &(temp->y2))) {
                return NULL;
            }
            return temp;
        }
        else {
            /* Sequences of size other than 2 or 4 are not supported 
            (don't wanna support infinite sequence nesting anymore)*/
            return NULL;
        }
    }
    else if (PySequence_Check(obj)) {
        /* Path for other sequences or Types that count as sequences*/
        PyObject *tmp = NULL;
        length = PySequence_Length(obj);
        if (length == 4) {
            /*These are to be substituted with better pg_DoubleFromSeqIndex() implementations*/
            tmp = PySequence_ITEM(obj, 0);
            if (!pg_DoubleFromObj(tmp, &(temp->x1))) {
                Py_DECREF(tmp);
                return NULL;
            }
            Py_DECREF(tmp);

            tmp = PySequence_ITEM(obj, 1);
            if (!pg_DoubleFromObj(tmp, &(temp->y1))) {
                Py_DECREF(tmp);
                return NULL;
            }
            Py_DECREF(tmp);

            tmp = PySequence_ITEM(obj, 2);
            if (!pg_DoubleFromObj(tmp, &(temp->x2))) {
                Py_DECREF(tmp);
                return NULL;
            }
            Py_DECREF(tmp);

            tmp = PySequence_ITEM(obj, 3);
            if (!pg_DoubleFromObj(tmp, &(temp->y2))) {
                Py_DECREF(tmp);
                return NULL;
            }
            Py_DECREF(tmp);

            return temp;
        }
        else if (length == 2) {

            tmp = PySequence_ITEM(obj, 0);
            if (!pg_TwoDoublesFromObj(tmp, &(temp->x1), &(temp->y1))) {
                Py_DECREF(tmp);
                return NULL;
            }
            Py_DECREF(tmp);

            tmp = PySequence_ITEM(obj, 1);
            if (!pg_TwoDoublesFromObj(tmp, &(temp->x2), &(temp->y2))) {
                Py_DECREF(tmp);
                return NULL;
            }
            Py_DECREF(tmp);

            return temp;

        }
        else {
            /* Sequences of size other than 2 or 4 are not supported 
            (don't wanna support infinite sequence nesting anymore)*/
            return NULL;
        }

    }

    if (PyObject_HasAttrString(obj, "line")) {
        PyObject *lineattr;
        pgLineBase *retline;
        lineattr = PyObject_GetAttrString(obj, "line");
        if (lineattr == NULL) {
            PyErr_Clear();
            return NULL;
        }
        if (PyCallable_Check(lineattr)) /*call if it's a method*/
        {
            PyObject *lineresult = PyObject_CallObject(lineattr, NULL);
            Py_DECREF(lineattr);
            if (lineresult == NULL) {
                PyErr_Clear();
                return NULL;
            }
            lineattr = lineresult;
        }
        retline = pgLine_FromObject(lineattr, temp);
        Py_DECREF(lineattr);
        return retline;
    }
    return NULL;
}

static PyObject *
pgLine_New(pgLineBase *l) {
    return _pg_line_subtype_new4(&pgLine_Type, l->x1, l->y1, l->x2, l->y2);
}

static PyObject *
pgLine_New4(double x1, double y1, double x2, double y2) {
    return _pg_line_subtype_new4(&pgLine_Type, x1, y1, x2, y2);
}

static PyObject *
pg_line_copy(pgLineObject *self) {
    return _pg_line_subtype_new4(
        Py_TYPE(self),
        self->line.x1, self->line.y1,
        self->line.x2, self->line.y2
    );
}

static PyObject *
pg_line_raycast(pgLineObject *self, PyObject* args) {
    pgLineObject *temp = NULL, *B = NULL;
    double x, y;

    if (PyTuple_GET_SIZE(args) == 1 && (B = pgLine_FromObject(PyTuple_GET_ITEM(args, 0), temp)) != NULL);
    else (B = pgLine_FromObject(args, temp));

    if (pgLine_GetIntersectionPoint(
        self->line.x1, self->line.y1, self->line.x2, self->line.y2,
        B->line.x1, B->line.y1, B->line.x2, B->line.y2,
        &x, &y)) {
        return Py_BuildValue("(dd)", x, y);
    }
    Py_RETURN_NONE;
}

static struct PyMethodDef pg_line_methods[] = {
    {"copy", (PyCFunction)pg_line_copy, METH_VARARGS, NULL},
    {"raycast", (PyCFunction)pg_line_raycast, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

/* sequence functions */

static Py_ssize_t
pg_line_seq_length(PyObject *_self) { return 4; }

static PyObject *
pg_line_item(pgLineObject *self, Py_ssize_t i) {
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
pg_line_ass_item(pgLineObject *self, Py_ssize_t i, PyObject *v) {
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
pg_line_contains_seq(pgLineObject *self, PyObject *arg) {
    if (PyNumber_Check(arg)) {
        double coord = PyFloat_AsDouble(arg);
        return coord == self->line.x1 || coord == self->line.y1 ||
               coord == self->line.x2 || coord == self->line.y1;
    }
    int ret = _pg_line_contains(self, arg);
    if (ret < 0) {
        PyErr_SetString(PyExc_TypeError,
                        "'in <pygame.Line>' requires line style object"
                        " or int as left operand");
    }
    return ret;
}

static PySequenceMethods pg_line_as_sequence = {
    .sq_length = pg_line_seq_length,
    .sq_item = (ssizeargfunc)pg_line_item,
    .sq_ass_item = (ssizeobjargproc)pg_line_ass_item,
    .sq_contains = (objobjproc)pg_line_contains_seq,
};

static PyObject *
pg_line_subscript(pgLineObject *self, PyObject *op) {
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
        PyObject* lst = PyList_New(4);
        
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
pg_line_ass_subscript(pgLineObject *self, PyObject *op, PyObject *value) {
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
                                 DBL_TRUE_MIN, DBL_MAX);
                }
            }
            self->line.x1 = values[0];
            self->line.y1 = values[1];
            self->line.x2 = values[2];
            self->line.y2 = values[3];
        }
        else {
            PyErr_SetString(PyExc_TypeError,
                            "Expected a number or sequence");
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
                                 DBL_TRUE_MIN, DBL_MAX);
                }
            }
            for (i = 0; i < slicelen; ++i) {
                data[start + step * i] = values[i];
            }
        }
        else {
            PyErr_SetString(PyExc_TypeError,
                            "Expected a number or sequence");
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
pg_line_bool(pgLineObject *self) {
    return self->line.x1 != 0 || self->line.y1 != 0 ||
           self->line.x2 != 0 || self->line.y2 != 0;
}

static PyNumberMethods pg_line_as_number = {
    .nb_bool = (inquiry)pg_line_bool,
};

static PyObject *
pg_line_repr(pgLineObject *self) {
    // dont comments on it (-_-)
    return PyUnicode_FromFormat("pygame.Line(%S, %S, %S, %S)",
                                PyFloat_FromDouble(self->line.x1),
                                PyFloat_FromDouble(self->line.y1),
                                PyFloat_FromDouble(self->line.x2),
                                PyFloat_FromDouble(self->line.y2));
}

static PyObject *
pg_line_str(pgLineObject *self) { return pg_line_repr(self); }

static PyObject *
pg_line_richcompare(PyObject *o1, PyObject *o2, int opid) {
    pgLineBase *o1line, *o2line, temp1, temp2;
    double length1, length2;

    o1line = pgLine_FromObject(o1, &temp1);
    o2line = pgLine_FromObject(o2, &temp2);

    if (!o1line || !o2line) {
        goto Unimplemented;
    }

    length1 = _pg_line_length(*o1line);
    length2 = _pg_line_length(*o2line);

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
pg_line_iterator(pgLineObject *self) {
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

#define __LINE_GETSET_NAME(name) \
    static PyObject* \
    pg_line_get##name(pgLineObject *self, void *closure) { return PyFloat_FromDouble(self->line.name); } \
    static int \
    pg_line_set##name(pgLineObject *self, PyObject *value, void *closure) { \
        double val; \
        DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value); \
        if (pg_DoubleFromObj(value, &val)) { \
            self->line.name = val; \
            return 0; \
        } \
        return -1; \
    }

// they are repetitive enough that we can abstract them like this
__LINE_GETSET_NAME(x1)
__LINE_GETSET_NAME(y1)
__LINE_GETSET_NAME(x2)
__LINE_GETSET_NAME(y2)

static PyObject *
pg_line_getsafepickle(pgLineObject *self, void *closure) { Py_RETURN_TRUE; }

static PyGetSetDef pg_line_getsets[] = {
    {"x1", (getter)pg_line_getx1, (setter)pg_line_setx1, NULL, NULL},
    {"y1", (getter)pg_line_gety1, (setter)pg_line_sety1, NULL, NULL},
    {"x2", (getter)pg_line_getx2, (setter)pg_line_setx2, NULL, NULL},
    {"y2", (getter)pg_line_gety2, (setter)pg_line_sety2, NULL, NULL},
    {"__safe_for_unpickling__", (getter)pg_line_getsafepickle, NULL, NULL, NULL},
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

static int
pg_line_init(pgLineObject *self, PyObject *args, PyObject *kwds) {
    pgLineBase temp;
    pgLineBase *argrect = pgLine_FromObject(args, &temp);

    if (argrect == NULL) {
        PyErr_SetString(PyExc_TypeError, "Argument must be rect style object");
        return -1;
    }
    self->line.x1 = argrect->x1;
    self->line.y1 = argrect->y1;
    self->line.x2 = argrect->x2;
    self->line.y2 = argrect->y2;
    return 0;
}
