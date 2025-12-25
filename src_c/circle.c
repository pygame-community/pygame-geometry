#include "include/geometry.h"
#include "include/collisions.h"

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
    }
    return (PyObject *)circle_obj;
}

static PyObject *
_pg_circle_subtype_new(PyTypeObject *type, pgCircleBase *circle)
{
    pgCircleObject *circle_obj =
        (pgCircleObject *)pgCircle_Type.tp_new(type, NULL, NULL);

    if (circle_obj) {
        circle_obj->circle = *circle;
    }
    return (PyObject *)circle_obj;
}

static PyObject *
pg_circle_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    pgCircleObject *self = (pgCircleObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->circle.x = self->circle.y = 0;
        self->circle.r = DBL_MIN;
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
    double radius = 0;
    if (!pg_DoubleFromObj(value, &radius) || radius <= 0) {
        return 0;
    }
    circle->r = radius;

    return 1;
}

static int
pgCircle_FromObject(PyObject *obj, pgCircleBase *out)
{
    Py_ssize_t length;

    if (pgCircle_Check(obj)) {
        *out = pgCircle_AsCircle(obj);
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
        if (length == 3 && !pgPolygon_Check(obj)) {
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
        if (!circleattr) {
            PyErr_Clear();
            return 0;
        }
        if (PyCallable_Check(circleattr)) /*call if it's a method*/
        {
            PyObject *circleresult = PyObject_CallObject(circleattr, NULL);
            Py_DECREF(circleattr);
            if (!circleresult) {
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
        if (!pg_TwoDoublesFromObj(args[0], &out->x, &out->y) ||
            !_pg_circle_set_radius(args[1], out)) {
            return 0;
        }
        return 1;
    }
    else if (nargs == 3) {
        if (!pg_DoubleFromObj(args[0], &out->x) ||
            !pg_DoubleFromObj(args[1], &out->y) ||
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
    return _pg_circle_subtype_new(Py_TYPE(self), &self->circle);
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
        pgCollision_CircleCircle(&self->circle, &other_circle));
}

static PyObject *
pg_circle_collideline(pgCircleObject *self, PyObject *const *args,
                      Py_ssize_t nargs)
{
    pgLineBase line;
    if (!pgLine_FromObjectFastcall(args, nargs, &line)) {
        return RAISE(PyExc_TypeError, "A CircleType object was expected");
    }
    return PyBool_FromLong(pgCollision_LineCircle(&line, &self->circle));
}

static PyObject *
pg_circle_collidepoint(pgCircleObject *self, PyObject *const *args,
                       Py_ssize_t nargs)
{
    double px, py;

    if (!pg_TwoDoublesFromFastcallArgs(args, nargs, &px, &py)) {
        return RAISE(
            PyExc_TypeError,
            "Circle.collidepoint requires a point or PointLike object");
    }

    return PyBool_FromLong(pgCollision_CirclePoint(&self->circle, px, py));
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

    return PyBool_FromLong(pgCollision_RectCircle(&temp, &self->circle));
}

static PG_FORCEINLINE int
_pg_circle_collideswith(pgCircleBase *scirc, PyObject *arg)
{
    if (pgCircle_Check(arg)) {
        return pgCollision_CircleCircle(&pgCircle_AsCircle(arg), scirc);
    }
    else if (pgRect_Check(arg)) {
        return pgCollision_RectCircle(&pgRect_AsRect(arg), scirc);
    }
    else if (pgLine_Check(arg)) {
        return pgCollision_LineCircle(&pgLine_AsLine(arg), scirc);
    }
    else if (pgPolygon_Check(arg)) {
        return pgCollision_CirclePolygon(scirc, &pgPolygon_AsPolygon(arg), 0);
    }
    else if (PySequence_Check(arg)) {
        double x, y;
        if (!pg_TwoDoublesFromObj(arg, &x, &y)) {
            PyErr_SetString(
                PyExc_TypeError,
                "Invalid point argument, must be a sequence of 2 numbers");
            return -1;
        }
        return pgCollision_CirclePoint(scirc, x, y);
    }

    PyErr_SetString(PyExc_TypeError,
                    "Invalid shape argument, must be a CircleType, RectType, "
                    "LineType, PolygonType or a sequence of 2 numbers");
    return -1;
}

static PyObject *
pg_circle_collideswith(pgCircleObject *self, PyObject *arg)
{
    int result = _pg_circle_collideswith(&self->circle, arg);
    if (result == -1) {
        return NULL;
    }

    return PyBool_FromLong(result);
}

static PyObject *
pg_circle_as_rect(pgCircleObject *self, PyObject *_null)
{
    pgCircleBase *scirc = &self->circle;
    int diameter = (int)(scirc->r * 2.0);
    int x = (int)(scirc->x - scirc->r);
    int y = (int)(scirc->y - scirc->r);

    return pgRect_New4(x, y, diameter, diameter);
}

static PyObject *
pg_circle_update(pgCircleObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    if (!pgCircle_FromObjectFastcall(args, nargs, &self->circle)) {
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
    double Dx, Dy;

    if (!pg_TwoDoublesFromFastcallArgs(args, nargs, &Dx, &Dy)) {
        return RAISE(PyExc_TypeError, "move requires a pair of numbers");
    }

    return _pg_circle_subtype_new3(Py_TYPE(self), self->circle.x + Dx,
                                   self->circle.y + Dy, self->circle.r);
}

static PyObject *
pg_circle_move_ip(pgCircleObject *self, PyObject *const *args,
                  Py_ssize_t nargs)
{
    double Dx, Dy;

    if (!pg_TwoDoublesFromFastcallArgs(args, nargs, &Dx, &Dy)) {
        return RAISE(PyExc_TypeError, "move_ip requires a pair of numbers");
    }

    self->circle.x += Dx;
    self->circle.y += Dy;

    Py_RETURN_NONE;
}

static PyObject *
pg_circle_contains(pgCircleObject *self, PyObject *arg)
{
    int result = 0;
    pgCircleBase *scirc = &self->circle;
    double x, y;

    if (pgCircle_Check(arg)) {
        pgCircleBase *temp = &pgCircle_AsCircle(arg);
        if (temp == scirc) {
            /*a circle is always contained within itself*/
            Py_RETURN_TRUE;
        }
        double dx, dy, dr;

        dx = temp->x - scirc->x;
        dy = temp->y - scirc->y;
        dr = temp->r - scirc->r;

        result = (dx * dx + dy * dy) <= (dr * dr);
    }
    else if (pgLine_Check(arg)) {
        pgLineBase *temp = &pgLine_AsLine(arg);

        if (pgCollision_CirclePoint(scirc, temp->xa, temp->ya) &&
            pgCollision_CirclePoint(scirc, temp->xb, temp->yb)) {
            result = 1;
        }
    }
    else if (pgRect_Check(arg)) {
        SDL_Rect *temp = &pgRect_AsRect(arg);

        if (pgCollision_CirclePoint(scirc, temp->x, temp->y) &&
            pgCollision_CirclePoint(scirc, temp->x + temp->w, temp->y) &&
            pgCollision_CirclePoint(scirc, temp->x, temp->y + temp->h) &&
            pgCollision_CirclePoint(scirc, temp->x + temp->w,
                                    temp->y + temp->h)) {
            result = 1;
        }
    }
    else if (pgPolygon_Check(arg)) {
        pgPolygonBase *poly = &pgPolygon_AsPolygon(arg);
        double *vertices = poly->vertices;
        Py_ssize_t i2;
        for (i2 = 0; i2 < poly->verts_num * 2; i2 += 2) {
            if (!pgCollision_CirclePoint(scirc, vertices[i2],
                                         vertices[i2 + 1])) {
                Py_RETURN_FALSE;
            }
        }
        result = 1;
    }
    else if (pg_TwoDoublesFromObj(arg, &x, &y)) {
        result = pgCollision_CirclePoint(scirc, x, y);
    }
    else {
        return RAISE(PyExc_TypeError,
                     "Invalid shape argument, must be a CircleType, RectType, "
                     "LineType, PolygonType or a sequence of 2 numbers");
    }

    return PyBool_FromLong(result);
}

static PyObject *
pg_circle_collidepolygon(pgCircleObject *self, PyObject *const *args,
                         Py_ssize_t nargs)
{
    int was_sequence, result, only_edges = 0;
    pgPolygonBase poly;

    /* Check for the optional only_edges argument */
    if (PyBool_Check(args[nargs - 1])) {
        only_edges = args[nargs - 1] == Py_True;
        nargs--;
    }

    if (!pgPolygon_FromObjectFastcall(args, nargs, &poly, &was_sequence)) {
        return RAISE(
            PyExc_TypeError,
            "collidepolygon requires a PolygonType or PolygonLike object");
    }

    result = pgCollision_CirclePolygon(&self->circle, &poly, only_edges);

    PG_FREEPOLY_COND(&poly, was_sequence);

    return PyBool_FromLong(result);
}

static void
_pg_rotate_circle_helper(pgCircleBase *circle, double angle, double rx,
                         double ry)
{
    if (angle == 0.0 || fmod(angle, 360.0) == 0.0) {
        return;
    }

    double x = circle->x - rx;
    double y = circle->y - ry;

    const double angle_rad = DEG_TO_RAD(angle);

    double cos_theta = cos(angle_rad);
    double sin_theta = sin(angle_rad);

    circle->x = rx + x * cos_theta - y * sin_theta;
    circle->y = ry + x * sin_theta + y * cos_theta;
}

static PyObject *
pg_circle_rotate(pgCircleObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    if (!nargs || nargs > 2) {
        return RAISE(PyExc_TypeError, "rotate requires 1 or 2 arguments");
    }

    pgCircleBase *circle = &self->circle;
    double angle, rx, ry;

    rx = circle->x;
    ry = circle->y;

    if (!pg_DoubleFromObj(args[0], &angle)) {
        return RAISE(PyExc_TypeError,
                     "Invalid angle argument, must be numeric");
    }

    if (nargs != 2) {
        return _pg_circle_subtype_new(Py_TYPE(self), circle);
    }

    if (!pg_TwoDoublesFromObj(args[1], &rx, &ry)) {
        return RAISE(PyExc_TypeError,
                     "Invalid rotation point argument, must be a sequence of "
                     "2 numbers");
    }

    PyObject *circle_obj = _pg_circle_subtype_new(Py_TYPE(self), circle);
    if (!circle_obj) {
        return NULL;
    }

    _pg_rotate_circle_helper(&pgCircle_AsCircle(circle_obj), angle, rx, ry);

    return circle_obj;
}

static PyObject *
pg_circle_rotate_ip(pgCircleObject *self, PyObject *const *args,
                    Py_ssize_t nargs)
{
    if (!nargs || nargs > 2) {
        return RAISE(PyExc_TypeError, "rotate requires 1 or 2 arguments");
    }

    pgCircleBase *circle = &self->circle;
    double angle, rx, ry;

    rx = circle->x;
    ry = circle->y;

    if (!pg_DoubleFromObj(args[0], &angle)) {
        return RAISE(PyExc_TypeError,
                     "Invalid angle argument, must be numeric");
    }

    if (nargs != 2) {
        /* just return None */
        Py_RETURN_NONE;
    }

    if (!pg_TwoDoublesFromObj(args[1], &rx, &ry)) {
        return RAISE(PyExc_TypeError,
                     "Invalid rotation point argument, must be a sequence "
                     "of 2 numbers");
    }

    _pg_rotate_circle_helper(circle, angle, rx, ry);

    Py_RETURN_NONE;
}

static PyObject *
pg_circle_collidelist(pgCircleObject *self, PyObject *arg)
{
    Py_ssize_t i;
    pgCircleBase *scirc = &self->circle;
    int colliding;

    if (!PySequence_Check(arg)) {
        return RAISE(PyExc_TypeError, "Argument must be a sequence");
    }

    /* fast path */
    if (PySequence_FAST_CHECK(arg)) {
        PyObject **items = PySequence_Fast_ITEMS(arg);
        for (i = 0; i < PySequence_Fast_GET_SIZE(arg); i++) {
            if ((colliding = _pg_circle_collideswith(scirc, items[i])) == -1) {
                /*invalid shape*/
                return NULL;
            }
            if (colliding) {
                return PyLong_FromSsize_t(i);
            }
        }
        return PyLong_FromLong(-1);
    }

    /* general sequence path */
    for (i = 0; i < PySequence_Length(arg); i++) {
        PyObject *obj = PySequence_GetItem(arg, i);
        if (!obj) {
            return NULL;
        }

        if ((colliding = _pg_circle_collideswith(scirc, obj)) == -1) {
            /*invalid shape*/
            Py_DECREF(obj);
            return NULL;
        }
        Py_DECREF(obj);

        if (colliding) {
            return PyLong_FromSsize_t(i);
        }
    }

    return PyLong_FromLong(-1);
}

static PyObject *
pg_circle_collidelistall(pgCircleObject *self, PyObject *arg)
{
    PyObject *ret, **items;
    Py_ssize_t i;
    pgCircleBase *scirc = &self->circle;
    int colliding;

    if (!PySequence_Check(arg)) {
        return RAISE(PyExc_TypeError, "Argument must be a sequence");
    }

    ret = PyList_New(0);
    if (!ret) {
        return NULL;
    }

    /* fast path */
    if (PySequence_FAST_CHECK(arg)) {
        PyObject **items = PySequence_Fast_ITEMS(arg);

        for (i = 0; i < PySequence_Fast_GET_SIZE(arg); i++) {
            if ((colliding = _pg_circle_collideswith(scirc, items[i])) == -1) {
                /*invalid shape*/
                Py_DECREF(ret);
                return NULL;
            }

            if (!colliding) {
                continue;
            }

            PyObject *num = PyLong_FromSsize_t(i);
            if (!num) {
                Py_DECREF(ret);
                return NULL;
            }

            if (PyList_Append(ret, num)) {
                Py_DECREF(num);
                Py_DECREF(ret);
                return NULL;
            }
            Py_DECREF(num);
        }

        return ret;
    }

    /* general sequence path */
    for (i = 0; i < PySequence_Length(arg); i++) {
        PyObject *obj = PySequence_GetItem(arg, i);
        if (!obj) {
            Py_DECREF(ret);
            return NULL;
        }

        if ((colliding = _pg_circle_collideswith(scirc, obj)) == -1) {
            /*invalid shape*/
            Py_DECREF(ret);
            Py_DECREF(obj);
            return NULL;
        }
        Py_DECREF(obj);

        if (!colliding) {
            continue;
        }

        PyObject *num = PyLong_FromSsize_t(i);
        if (!num) {
            Py_DECREF(ret);
            return NULL;
        }

        if (PyList_Append(ret, num)) {
            Py_DECREF(num);
            Py_DECREF(ret);
            return NULL;
        }
        Py_DECREF(num);
    }

    return ret;
}

static PyObject *
pg_circle_intersect(pgCircleObject *self, PyObject *arg)
{
    pgCircleBase *scirc = &self->circle;

    /* max number of intersections when supporting: Circle (2), */
    double intersections[4];
    int num = 0;

    if (pgCircle_Check(arg)) {
        pgCircleBase *other = &pgCircle_AsCircle(arg);
        num = pgIntersection_CircleCircle(scirc, other, intersections);
    }
    else {
        PyErr_Format(PyExc_TypeError, "Argument must be a CircleType, got %s",
                     Py_TYPE(arg)->tp_name);
        return NULL;
    }

    return pg_PointList_FromArrayDouble(intersections, num * 2);
}

static struct PyMethodDef pg_circle_methods[] = {
    {"collidecircle", (PyCFunction)pg_circle_collidecircle, METH_FASTCALL,
     NULL},
    {"collideline", (PyCFunction)pg_circle_collideline, METH_FASTCALL, NULL},
    {"collidepoint", (PyCFunction)pg_circle_collidepoint, METH_FASTCALL, NULL},
    {"colliderect", (PyCFunction)pg_circle_colliderect, METH_FASTCALL, NULL},
    {"collide", (PyCFunction)pg_circle_collideswith, METH_O, NULL},
    {"collidepolygon", (PyCFunction)pg_circle_collidepolygon, METH_FASTCALL,
     NULL},
    {"collidelist", (PyCFunction)pg_circle_collidelist, METH_O, NULL},
    {"collidelistall", (PyCFunction)pg_circle_collidelistall, METH_O, NULL},
    {"as_rect", (PyCFunction)pg_circle_as_rect, METH_NOARGS, NULL},
    {"update", (PyCFunction)pg_circle_update, METH_FASTCALL, NULL},
    {"move", (PyCFunction)pg_circle_move, METH_FASTCALL, NULL},
    {"move_ip", (PyCFunction)pg_circle_move_ip, METH_FASTCALL, NULL},
    {"contains", (PyCFunction)pg_circle_contains, METH_O, NULL},
    {"__copy__", (PyCFunction)pg_circle_copy, METH_NOARGS, NULL},
    {"copy", (PyCFunction)pg_circle_copy, METH_NOARGS, NULL},
    {"rotate", (PyCFunction)pg_circle_rotate, METH_FASTCALL, NULL},
    {"rotate_ip", (PyCFunction)pg_circle_rotate_ip, METH_FASTCALL, NULL},
    {"intersect", (PyCFunction)pg_circle_intersect, METH_O, NULL},
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
    PyObject *x, *y, *r;

    x = PyFloat_FromDouble(self->circle.x);
    if (!x) {
        return NULL;
    }
    y = PyFloat_FromDouble(self->circle.y);
    if (!y) {
        Py_DECREF(x);
        return NULL;
    }
    r = PyFloat_FromDouble(self->circle.r);
    if (!r) {
        Py_DECREF(x);
        Py_DECREF(y);
        return NULL;
    }

    PyObject *result = PyUnicode_FromFormat("<Circle((%R, %R), %R)>", x, y, r);

    Py_DECREF(x);
    Py_DECREF(y);
    Py_DECREF(r);

    return result;
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
    double radius;

    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    if (!pg_DoubleFromObj(value, &radius)) {
        PyErr_SetString(PyExc_TypeError,
                        "Invalid type for radius, must be numeric");
        return -1;
    }

    if (radius <= 0) {
        PyErr_SetString(PyExc_ValueError, "Invalid radius value, must be > 0");
        return -1;
    }

    self->circle.r = radius;

    return 0;
}

static PyObject *
pg_circle_getr_sqr(pgCircleObject *self, void *closure)
{
    return PyFloat_FromDouble(self->circle.r * self->circle.r);
}

static int
pg_circle_setr_sqr(pgCircleObject *self, PyObject *value, void *closure)
{
    double radius_squared;

    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    if (!pg_DoubleFromObj(value, &radius_squared)) {
        PyErr_SetString(PyExc_TypeError,
                        "Invalid type for radius squared, must be numeric");
        return -1;
    }

    if (radius_squared <= 0) {
        PyErr_SetString(PyExc_ValueError,
                        "Invalid radius squared value, must be > 0");
        return -1;
    }

    self->circle.r = sqrt(radius_squared);

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
    if (!pg_TwoDoublesFromObj(value, &self->circle.x, &self->circle.y)) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
        return -1;
    }
    return 0;
}

static PyObject *
pg_circle_getarea(pgCircleObject *self, void *closure)
{
    return PyFloat_FromDouble(M_PI * self->circle.r * self->circle.r);
}

static int
pg_circle_setarea(pgCircleObject *self, PyObject *value, void *closure)
{
    double area;

    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    if (!pg_DoubleFromObj(value, &area)) {
        PyErr_SetString(PyExc_TypeError,
                        "Invalid type for area, must be numeric");
        return -1;
    }

    if (area <= 0) {
        PyErr_SetString(PyExc_ValueError, "Invalid area value, must be > 0");
        return -1;
    }

    self->circle.r = sqrt(area / M_PI);

    return 0;
}

static PyObject *
pg_circle_getcircumference(pgCircleObject *self, void *closure)
{
    return PyFloat_FromDouble(M_TWOPI * self->circle.r);
}

static int
pg_circle_setcircumference(pgCircleObject *self, PyObject *value,
                           void *closure)
{
    double circumference;

    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    if (!pg_DoubleFromObj(value, &circumference)) {
        PyErr_SetString(PyExc_TypeError,
                        "Invalid type for circumference, must be numeric");
        return -1;
    }

    if (circumference <= 0) {
        PyErr_SetString(PyExc_ValueError,
                        "Invalid circumference value, must be > 0");
        return -1;
    }

    self->circle.r = circumference / M_TWOPI;

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
    double diameter;

    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    if (!pg_DoubleFromObj(value, &diameter)) {
        PyErr_SetString(PyExc_TypeError,
                        "Invalid type for diameter, must be numeric");
        return -1;
    }

    if (diameter <= 0) {
        PyErr_SetString(PyExc_ValueError,
                        "Invalid diameter value, must be > 0");
        return -1;
    }

    self->circle.r = diameter / 2;

    return 0;
}

static PyObject *
pg_circle_gettop(pgCircleObject *self, void *closure)
{
    return pg_TupleFromDoublePair(self->circle.x,
                                  self->circle.y - self->circle.r);
}

static int
pg_circle_settop(pgCircleObject *self, PyObject *value, void *closure)
{
    double x, y;

    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    if (!pg_TwoDoublesFromObj(value, &x, &y)) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
        return -1;
    }

    self->circle.y = y + self->circle.r;
    self->circle.x = x;

    return 0;
}

static PyObject *
pg_circle_getleft(pgCircleObject *self, void *closure)
{
    return pg_TupleFromDoublePair(self->circle.x - self->circle.r,
                                  self->circle.y);
}

static int
pg_circle_setleft(pgCircleObject *self, PyObject *value, void *closure)
{
    double x, y;

    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    if (!pg_TwoDoublesFromObj(value, &x, &y)) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
        return -1;
    }

    self->circle.x = x + self->circle.r;
    self->circle.y = y;

    return 0;
}

static PyObject *
pg_circle_getbottom(pgCircleObject *self, void *closure)
{
    return pg_TupleFromDoublePair(self->circle.x,
                                  self->circle.y + self->circle.r);
}

static int
pg_circle_setbottom(pgCircleObject *self, PyObject *value, void *closure)
{
    double x, y;

    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    if (!pg_TwoDoublesFromObj(value, &x, &y)) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
        return -1;
    }

    self->circle.y = y - self->circle.r;
    self->circle.x = x;

    return 0;
}

static PyObject *
pg_circle_getright(pgCircleObject *self, void *closure)
{
    return pg_TupleFromDoublePair(self->circle.x + self->circle.r,
                                  self->circle.y);
}

static int
pg_circle_setright(pgCircleObject *self, PyObject *value, void *closure)
{
    double x, y;

    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    if (!pg_TwoDoublesFromObj(value, &x, &y)) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
        return -1;
    }

    self->circle.x = x - self->circle.r;
    self->circle.y = y;

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
    if (!pgCircle_FromObject(args, &self->circle)) {
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
    {"top", (getter)pg_circle_gettop, (setter)pg_circle_settop, NULL, NULL},
    {"left", (getter)pg_circle_getleft, (setter)pg_circle_setleft, NULL, NULL},
    {"bottom", (getter)pg_circle_getbottom, (setter)pg_circle_setbottom, NULL,
     NULL},
    {"right", (getter)pg_circle_getright, (setter)pg_circle_setright, NULL,
     NULL},
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