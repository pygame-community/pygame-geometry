#include "include/geometry.h"
#include "include/collisions.h"

#define IS_LINE_VALID(line) (line->xa != line->xb || line->ya != line->yb)

static double
pgLine_Length(pgLineBase *line)
{
    double dx = line->xb - line->xa;
    double dy = line->yb - line->ya;
    return sqrt(dx * dx + dy * dy);
}

static double
pgLine_LengthSquared(pgLineBase *line)
{
    double dx = line->xb - line->xa;
    double dy = line->yb - line->ya;
    return dx * dx + dy * dy;
}

static void
pgLine_At(pgLineBase *line, double t, double *X, double *Y)
{
    *X = line->xa + t * (line->xb - line->xa);
    *Y = line->ya + t * (line->yb - line->ya);
}

static PyObject *
_pg_line_subtype_new4(PyTypeObject *type, double xa, double ya, double xb,
                      double yb)
{
    pgLineObject *line = (pgLineObject *)pgLine_Type.tp_new(type, NULL, NULL);

    if (line) {
        line->line.xa = xa;
        line->line.ya = ya;
        line->line.xb = xb;
        line->line.yb = yb;
    }
    return (PyObject *)line;
}

static PyObject *
pg_line_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    pgLineObject *self = (pgLineObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->line.xa = self->line.ya = 0;
        self->line.xb = self->line.yb = 0;
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
            if (!pg_DoubleFromObj(farray[0], &(out->xa)) ||
                !pg_DoubleFromObj(farray[1], &(out->ya)) ||
                !pg_DoubleFromObj(farray[2], &(out->xb)) ||
                !pg_DoubleFromObj(farray[3], &(out->yb))) {
                return 0;
            }
            return IS_LINE_VALID(out);
        }
        else if (length == 2) {
            if (!pg_TwoDoublesFromObj(farray[0], &(out->xa), &(out->ya)) ||
                !pg_TwoDoublesFromObj(farray[1], &(out->xb), &(out->yb))) {
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
        if (length == 4 && !pgPolygon_Check(obj)) {
            PyObject *tmp;
            tmp = PySequence_GetItem(obj, 0);
            if (!pg_DoubleFromObj(tmp, &(out->xa))) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            tmp = PySequence_GetItem(obj, 1);
            if (!pg_DoubleFromObj(tmp, &(out->ya))) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            tmp = PySequence_GetItem(obj, 2);
            if (!pg_DoubleFromObj(tmp, &(out->xb))) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            tmp = PySequence_GetItem(obj, 3);
            if (!pg_DoubleFromObj(tmp, &(out->yb))) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            return IS_LINE_VALID(out);
        }
        else if (length == 2) {
            PyObject *tmp;
            tmp = PySequence_GetItem(obj, 0);
            if (!pg_TwoDoublesFromObj(tmp, &(out->xa), &(out->ya))) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            tmp = PySequence_GetItem(obj, 1);
            if (!pg_TwoDoublesFromObj(tmp, &(out->xb), &(out->yb))) {
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
        else {
            return 0;
        }
    }
    if (PyObject_HasAttrString(obj, "line")) {
        PyObject *lineattr;
        lineattr = PyObject_GetAttrString(obj, "line");
        if (!lineattr) {
            PyErr_Clear();
            return 0;
        }
        if (PyCallable_Check(lineattr)) /*call if it's a method*/
        {
            PyObject *lineresult = PyObject_CallObject(lineattr, NULL);
            Py_DECREF(lineattr);
            if (!lineresult) {
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
        if (!pg_TwoDoublesFromObj(args[0], &(out->xa), &(out->ya)) ||
            !pg_TwoDoublesFromObj(args[1], &(out->xb), &(out->yb))) {
            return 0;
        }
        return IS_LINE_VALID(out);
    }
    else if (nargs == 4) {
        if (!pg_DoubleFromObj(args[0], &(out->xa)) ||
            !pg_DoubleFromObj(args[1], &(out->ya)) ||
            !pg_DoubleFromObj(args[2], &(out->xb)) ||
            !pg_DoubleFromObj(args[3], &(out->yb))) {
            return 0;
        }
        return IS_LINE_VALID(out);
    }
    return 0;
}

static PyObject *
pgLine_New(pgLineBase *l)
{
    return _pg_line_subtype_new4(&pgLine_Type, l->xa, l->ya, l->xb, l->yb);
}

static PyObject *
pgLine_New4(double xa, double ya, double xb, double yb)
{
    return _pg_line_subtype_new4(&pgLine_Type, xa, ya, xb, yb);
}

static PyObject *
pg_line_copy(pgLineObject *self, PyObject *_null)
{
    return _pg_line_subtype_new4(Py_TYPE(self), self->line.xa, self->line.ya,
                                 self->line.xb, self->line.yb);
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

    double dx1 = self->line.xb - self->line.xa;
    double dy1 = self->line.yb - self->line.ya;
    double dx2 = other_line.xb - other_line.xa;
    double dy2 = other_line.yb - other_line.ya;

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
    double Ax = self->line.xa;
    double Ay = self->line.ya;
    double Bx = self->line.xb;
    double By = self->line.yb;

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
pg_line_colliderect(pgLineObject *self, PyObject *const *args,
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
        return PyBool_FromLong(pgCollision_RectLine(tmp, &self->line));
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

    return PyBool_FromLong(pgCollision_RectLine(&temp, &self->line));
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

    double dx1 = self->line.xb - self->line.xa;
    double dy1 = self->line.yb - self->line.ya;
    double dx2 = other_line.xb - other_line.xa;
    double dy2 = other_line.yb - other_line.ya;

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
    else if (pgPolygon_Check(arg)) {
        result =
            pgCollision_PolygonLine(&pgPolygon_AsPolygon(arg), &self->line, 0);
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
                     "LineType, PolygonType or a sequence of 2 numbers");
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

    return _pg_line_subtype_new4(Py_TYPE(self), self->line.xa + Dx,
                                 self->line.ya + Dy, self->line.xb + Dx,
                                 self->line.yb + Dy);
}

static PyObject *
pg_line_move_ip(pgLineObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    double Dx, Dy;

    if (!pg_TwoDoublesFromFastcallArgs(args, nargs, &Dx, &Dy)) {
        return RAISE(PyExc_TypeError, "move_ip requires a pair of numbers");
    }

    self->line.xa += Dx;
    self->line.ya += Dy;
    self->line.xb += Dx;
    self->line.yb += Dy;

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

static PyObject *
pg_line_flip(pgLineObject *self, PyObject *_null)
{
    return _pg_line_subtype_new4(Py_TYPE(self), self->line.xb, self->line.yb,
                                 self->line.xa, self->line.ya);
}

static PyObject *
pg_line_flip_ab_ip(pgLineObject *self, PyObject *_null)
{
    double tx = self->line.xb;
    double ty = self->line.yb;

    self->line.xb = self->line.xa;
    self->line.yb = self->line.ya;

    self->line.xa = tx;
    self->line.ya = ty;

    Py_RETURN_NONE;
}

static PyObject *
pg_line_as_points(pgLineObject *self, PyObject *arg)
{
    int N = 0;
    if (!pg_IntFromObj(arg, &N)) {
        return RAISE(PyExc_TypeError, "as_points requires an integer");
    }
    if (N < 0) {
        return RAISE(PyExc_ValueError,
                     "as_points requires a positive integer");
    }

    PyObject *point = NULL;
    PyObject *list = PyList_New(2 + N);
    if (!list) {
        return NULL;
    }

    pgLineBase *line = &self->line;

    // Add the start and end points to the list
    point = pg_TupleFromDoublePair(line->xa, line->ya);
    if (!point) {
        Py_DECREF(list);
        return NULL;
    }
    PyList_SET_ITEM(list, 0, point);
    point = pg_TupleFromDoublePair(line->xb, line->yb);
    if (!point) {
        Py_DECREF(list);
        return NULL;
    }
    PyList_SET_ITEM(list, N + 1, point);

    if (!N) {
        return list;
    }
    else if (N == 1) {
        point = pg_TupleFromDoublePair((line->xa + line->xb) / 2,
                                       (line->ya + line->yb) / 2);
        if (!point) {
            Py_DECREF(list);
            return NULL;
        }
        PyList_SET_ITEM(list, 1, point);
        return list;
    }

    double step_x = (line->xb - line->xa) / (N + 1);
    double step_y = (line->yb - line->ya) / (N + 1);
    double x = line->xa + step_x;
    double y = line->ya + step_y;

    Py_ssize_t i;
    for (i = 1; i < N + 1; i++) {
        point = pg_TupleFromDoublePair(x, y);
        if (!point) {
            Py_DECREF(list);
            return NULL;
        }
        PyList_SET_ITEM(list, i, point);
        x += step_x;
        y += step_y;
    }

    return list;
}

static PyObject *
pg_line_as_segments(pgLineObject *self, PyObject *arg)
{
    /* Segments the line into N Lines of equal length and returns a list of
     * them. */

    int N = 1;
    if (!pg_IntFromObj(arg, &N)) {
        return RAISE(PyExc_TypeError, "as_segments requires an integer");
    }
    if (N < 1) {
        return RAISE(PyExc_ValueError,
                     "as_segments requires a positive integer");
    }

    PyObject *line_obj = NULL;
    PyObject *list = PyList_New(N);
    if (!list) {
        return NULL;
    }

    if (N == 1) {
        line_obj = pg_line_copy(self, NULL);
        if (!line_obj) {
            Py_DECREF(list);
            return NULL;
        }
        PyList_SET_ITEM(list, 0, line_obj);
        return list;
    }

    pgLineBase *line = &self->line;

    double step_x = (line->xb - line->xa) / N;
    double step_y = (line->yb - line->ya) / N;
    double xa = line->xa, ya = line->ya;
    double xb = xa + step_x, yb = ya + step_y;

    Py_ssize_t i;
    for (i = 0; i < N; i++) {
        line_obj = _pg_line_subtype_new4(Py_TYPE(self), xa, ya, xb, yb);
        if (!line_obj) {
            Py_DECREF(list);
            return NULL;
        }
        PyList_SET_ITEM(list, i, line_obj);
        xa = xb;
        ya = yb;
        xb += step_x;
        yb += step_y;
    }

    return list;
}

static PG_FORCE_INLINE double
_lerp_helper(double start, double end, double amount)
{
    return start + (end - start) * amount;
}

static int
_line_scale_helper(pgLineBase *line, double factor, double origin)
{
    if (factor == 1.0) {
        return 1;
    }
    else if (factor <= 0.0) {
        PyErr_SetString(PyExc_ValueError,
                        "Can only scale by a positive non zero number");
        return 0;
    }

    if (origin < 0.0 || origin > 1.0) {
        PyErr_SetString(PyExc_ValueError, "Origin must be between 0 and 1");
        return 0;
    }

    double xa = line->xa;
    double ya = line->ya;
    double xb = line->xb;
    double yb = line->yb;

    double x1_factor = xa * factor;
    double y1_factor = ya * factor;
    double x2_factor = xb * factor;
    double y2_factor = yb * factor;

    double fac_m_one = factor - 1;
    double dx = _lerp_helper(fac_m_one * xa, fac_m_one * xb, origin);
    double dy = _lerp_helper(fac_m_one * ya, fac_m_one * yb, origin);

    line->xa = x1_factor - dx;
    line->ya = y1_factor - dy;
    line->xb = x2_factor - dx;
    line->yb = y2_factor - dy;

    return 1;
}

static PyObject *
pg_line_scale(pgLineObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    double factor, origin;

    if (!pg_TwoDoublesFromFastcallArgs(args, nargs, &factor, &origin)) {
        return RAISE(PyExc_TypeError,
                     "scale requires a sequence of two numbers");
    }

    PyObject *line;
    if (!(line = pgLine_New(&self->line))) {
        return NULL;
    }

    if (!_line_scale_helper(&pgLine_AsLine(line), factor, origin)) {
        return NULL;
    }

    return line;
}

static PyObject *
pg_line_scale_ip(pgLineObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    double factor, origin;

    if (!pg_TwoDoublesFromFastcallArgs(args, nargs, &factor, &origin)) {
        return RAISE(PyExc_TypeError,
                     "scale_ip requires a sequence of two numbers");
    }

    if (!_line_scale_helper(&pgLine_AsLine(self), factor, origin)) {
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_line_collidepolygon(pgLineObject *self, PyObject *const *args,
                       Py_ssize_t nargs)
{
    pgPolygonBase poly;
    int was_sequence, result, only_edges = 0;

    /* Check for the optional only_edges argument */
    if (PyBool_Check(args[nargs - 1])) {
        only_edges = args[nargs - 1] == Py_True;
        nargs--;
    }

    if (!pgPolygon_FromObjectFastcall(args, nargs, &poly, &was_sequence)) {
        return RAISE(
            PyExc_TypeError,
            "collidepolygon requires a Polygon or PolygonLike object");
    }

    result = pgCollision_PolygonLine(&poly, &self->line, only_edges);

    PG_FREEPOLY_COND(&poly, was_sequence);

    return PyBool_FromLong(result);
}

static PyObject *
pg_line_as_circle(pgLineObject *self, PyObject *_null)
{
    pgCircleObject *circle_obj =
        (pgCircleObject *)pgCircle_Type.tp_new(&pgCircle_Type, NULL, NULL);

    if (circle_obj) {
        circle_obj->circle.x = (self->line.xa + self->line.xb) / 2;
        circle_obj->circle.y = (self->line.ya + self->line.yb) / 2;
        circle_obj->circle.r = pgLine_Length(&self->line) / 2;
    }

    return (PyObject *)circle_obj;
}

static void
_pg_rotate_line_helper(pgLineBase *line, double angle, double rx, double ry)
{
    if (angle == 0.0 || fmod(angle, 360.0) == 0.0) {
        return;
    }

    double angle_rad = DEG_TO_RAD(angle);

    double x1 = line->xa, y1 = line->ya;
    double x2 = line->xb, y2 = line->yb;

    double cos_a = cos(angle_rad);
    double sin_a = sin(angle_rad);

    x1 -= rx;
    y1 -= ry;
    x2 -= rx;
    y2 -= ry;

    double x1_new = x1 * cos_a - y1 * sin_a;
    double y1_new = x1 * sin_a + y1 * cos_a;
    double x2_new = x2 * cos_a - y2 * sin_a;
    double y2_new = x2 * sin_a + y2 * cos_a;

    line->xa = x1_new + rx;
    line->ya = y1_new + ry;

    line->xb = x2_new + rx;
    line->yb = y2_new + ry;
}

static PyObject *
pg_line_rotate(pgLineObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    if (!nargs || nargs > 2) {
        return RAISE(PyExc_TypeError, "rotate requires 1 or 2 arguments");
    }

    pgLineBase *line = &self->line;
    double angle, rx, ry;

    rx = (line->xa + line->xb) / 2;
    ry = (line->ya + line->yb) / 2;

    if (!pg_DoubleFromObj(args[0], &angle)) {
        return RAISE(PyExc_TypeError,
                     "Invalid angle argument, must be numeric");
    }

    if (nargs == 2 && !pg_TwoDoublesFromObj(args[1], &rx, &ry)) {
        return RAISE(PyExc_TypeError,
                     "Invalid rotation_point argument, must be a sequence of "
                     "two numbers");
    }

    PyObject *line_obj;
    if (!(line_obj = pgLine_New(line))) {
        return NULL;
    }

    _pg_rotate_line_helper(&pgLine_AsLine(line_obj), angle, rx, ry);

    return line_obj;
}

static PyObject *
pg_line_rotate_ip(pgLineObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    if (!nargs || nargs > 2) {
        return RAISE(PyExc_TypeError, "rotate requires 1 or 2 arguments");
    }

    pgLineBase *line = &self->line;
    double angle, rx, ry;

    rx = (line->xa + line->xb) / 2;
    ry = (line->ya + line->yb) / 2;

    if (!pg_DoubleFromObj(args[0], &angle)) {
        return RAISE(PyExc_TypeError,
                     "Invalid angle argument, must be numeric");
    }

    if (nargs == 2 && !pg_TwoDoublesFromObj(args[1], &rx, &ry)) {
        return RAISE(PyExc_TypeError,
                     "Invalid rotation_point argument, must be a sequence of "
                     "two numbers");
    }

    _pg_rotate_line_helper(line, angle, rx, ry);

    Py_RETURN_NONE;
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
    {"colliderect", (PyCFunction)pg_line_colliderect, METH_FASTCALL, NULL},
    {"collide", (PyCFunction)pg_line_collideswith, METH_O, NULL},
    {"collidepolygon", (PyCFunction)pg_line_collidepolygon, METH_FASTCALL,
     NULL},
    {"as_rect", (PyCFunction)pg_line_as_rect, METH_NOARGS, NULL},
    {"update", (PyCFunction)pg_line_update, METH_FASTCALL, NULL},
    {"move", (PyCFunction)pg_line_move, METH_FASTCALL, NULL},
    {"move_ip", (PyCFunction)pg_line_move_ip, METH_FASTCALL, NULL},
    {"at", (PyCFunction)pg_line_at, METH_O, NULL},
    {"flip_ab", (PyCFunction)pg_line_flip, METH_NOARGS, NULL},
    {"flip_ab_ip", (PyCFunction)pg_line_flip_ab_ip, METH_NOARGS, NULL},
    {"as_points", (PyCFunction)pg_line_as_points, METH_O, NULL},
    {"as_segments", (PyCFunction)pg_line_as_segments, METH_O, NULL},
    {"scale", (PyCFunction)pg_line_scale, METH_FASTCALL, NULL},
    {"scale_ip", (PyCFunction)pg_line_scale_ip, METH_FASTCALL, NULL},
    {"as_circle", (PyCFunction)pg_line_as_circle, METH_NOARGS, NULL},
    {"rotate", (PyCFunction)pg_line_rotate, METH_FASTCALL, NULL},
    {"rotate_ip", (PyCFunction)pg_line_rotate_ip, METH_FASTCALL, NULL},
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
        return coord == self->line.xa || coord == self->line.ya ||
               coord == self->line.xb || coord == self->line.ya;
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
    Py_ssize_t i;
    if (PyIndex_Check(op)) {
        PyObject *index = PyNumber_Index(op);

        if (!index) {
            return NULL;
        }
        i = PyNumber_AsSsize_t(index, NULL);
        Py_DECREF(index);
        return pg_line_item(self, i);
    }
    else if (op == Py_Ellipsis) {
        PyObject *lst = PyList_New(4);
        if (!lst) {
            return NULL;
        }

        for (i = 0; i < 4; i++) {
            PyObject *val = PyFloat_FromDouble(data[i]);
            if (!val) {
                Py_DECREF(lst);
                return NULL;
            }

            PyList_SET_ITEM(lst, i, val);
        }

        return lst;
    }
    else if (PySlice_Check(op)) {
        PyObject *slice;
        Py_ssize_t start;
        Py_ssize_t stop;
        Py_ssize_t step;
        Py_ssize_t slicelen;
        PyObject *n;

        if (PySlice_GetIndicesEx(op, 4, &start, &stop, &step, &slicelen)) {
            return NULL;
        }

        slice = PyList_New(slicelen);
        if (!slice) {
            return NULL;
        }
        for (i = 0; i < slicelen; ++i) {
            n = PyFloat_FromDouble(data[start + (step * i)]);
            if (!n) {
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
        if (!index) {
            return -1;
        }
        i = PyNumber_AsSsize_t(index, NULL);
        Py_DECREF(index);
        return pg_line_ass_item(self, i, value);
    }
    else if (op == Py_Ellipsis) {
        double val = 0;

        if (pg_DoubleFromObj(value, &val)) {
            self->line.xa = val;
            self->line.ya = val;
            self->line.xb = val;
            self->line.yb = val;
        }
        else if (PyObject_IsInstance(value, (PyObject *)&pgLine_Type)) {
            pgLineObject *line = (pgLineObject *)value;

            self->line.xa = line->line.xa;
            self->line.ya = line->line.ya;
            self->line.xb = line->line.xb;
            self->line.yb = line->line.yb;
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
            self->line.xa = values[0];
            self->line.ya = values[1];
            self->line.xb = values[2];
            self->line.yb = values[3];
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
    PyObject *result, *xa, *ya, *xb, *yb;

    xa = PyFloat_FromDouble(self->line.xa);
    if (!xa) {
        return NULL;
    }
    ya = PyFloat_FromDouble(self->line.ya);
    if (!ya) {
        Py_DECREF(xa);
        return NULL;
    }
    xb = PyFloat_FromDouble(self->line.xb);
    if (!xb) {
        Py_DECREF(xa);
        Py_DECREF(ya);
        return NULL;
    }
    yb = PyFloat_FromDouble(self->line.yb);
    if (!yb) {
        Py_DECREF(xa);
        Py_DECREF(ya);
        Py_DECREF(xb);
        return NULL;
    }

    result =
        PyUnicode_FromFormat("<Line((%R, %R), (%R, %R))>", xa, ya, xb, yb);

    Py_DECREF(xa);
    Py_DECREF(ya);
    Py_DECREF(xb);
    Py_DECREF(yb);

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
__LINE_GETSET_NAME(xa)
__LINE_GETSET_NAME(ya)
__LINE_GETSET_NAME(xb)
__LINE_GETSET_NAME(yb)
#undef __LINE_GETSET_NAME

static PyObject *
pg_line_geta(pgLineObject *self, void *closure)
{
    return pg_TupleFromDoublePair(self->line.xa, self->line.ya);
}

static int
pg_line_seta(pgLineObject *self, PyObject *value, void *closure)
{
    double x, y;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (pg_TwoDoublesFromObj(value, &x, &y)) {
        self->line.xa = x;
        self->line.ya = y;
        return 0;
    }
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
    return -1;
}

static PyObject *
pg_line_getb(pgLineObject *self, void *closure)
{
    return pg_TupleFromDoublePair(self->line.xb, self->line.yb);
}

static int
pg_line_setb(pgLineObject *self, PyObject *value, void *closure)
{
    double x, y;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (pg_TwoDoublesFromObj(value, &x, &y)) {
        self->line.xb = x;
        self->line.yb = y;
        return 0;
    }
    PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
    return -1;
}

static PyObject *
pg_line_getangle(pgLineObject *self, void *closure)
{
    double dx = self->line.xb - self->line.xa;

    if (dx == 0.0)
        return (self->line.yb > self->line.ya) ? PyFloat_FromDouble(-90.0)
                                               : PyFloat_FromDouble(90.0);

    double dy = self->line.yb - self->line.ya;

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
    double dem = self->line.xb - self->line.xa;
    if (dem == 0) {
        return PyFloat_FromDouble(0);
    }

    double slope = (self->line.yb - self->line.ya) / dem;
    return PyFloat_FromDouble(slope);
}

static PyObject *
pg_line_getsafepickle(pgLineObject *self, void *closure)
{
    Py_RETURN_TRUE;
}

static PyObject *
pg_line_get_center(pgLineObject *self, void *closure)
{
    return pg_TupleFromDoublePair((self->line.xa + self->line.xb) / 2,
                                  (self->line.ya + self->line.yb) / 2);
}

static int
pg_line_set_center(pgLineObject *self, PyObject *value, void *closure)
{
    double m_x, m_y;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (!pg_TwoDoublesFromObj(value, &m_x, &m_y)) {
        PyErr_SetString(
            PyExc_TypeError,
            "Invalid center value, expected a sequence of 2 numbers");
        return -1;
    }

    double dx = m_x - (self->line.xa + self->line.xb) / 2;
    double dy = m_y - (self->line.ya + self->line.yb) / 2;

    self->line.xa += dx;
    self->line.ya += dy;
    self->line.xb += dx;
    self->line.yb += dy;

    return 0;
}

static PyObject *
pg_line_get_centerx(pgLineObject *self, void *closure)
{
    return PyFloat_FromDouble((self->line.xa + self->line.xb) / 2);
}

static int
pg_line_set_centerx(pgLineObject *self, PyObject *value, void *closure)
{
    double m_x;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (!pg_DoubleFromObj(value, &m_x)) {
        PyErr_SetString(PyExc_TypeError,
                        "Invalid centerx value, expected a numeric value");
        return -1;
    }

    double dx = m_x - (self->line.xa + self->line.xb) / 2;
    self->line.xa += dx;
    self->line.xb += dx;
    return 0;
}

static PyObject *
pg_line_get_centery(pgLineObject *self, void *closure)
{
    return PyFloat_FromDouble((self->line.ya + self->line.yb) / 2);
}

static int
pg_line_set_centery(pgLineObject *self, PyObject *value, void *closure)
{
    double m_y;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (!pg_DoubleFromObj(value, &m_y)) {
        PyErr_SetString(PyExc_TypeError,
                        "Invalid centery value, expected a numeric value");
        return -1;
    }

    double dy = m_y - (self->line.ya + self->line.yb) / 2;
    self->line.ya += dy;
    self->line.yb += dy;
    return 0;
}

static PyGetSetDef pg_line_getsets[] = {
    {"xa", (getter)pg_line_getxa, (setter)pg_line_setxa, NULL, NULL},
    {"ya", (getter)pg_line_getya, (setter)pg_line_setya, NULL, NULL},
    {"xb", (getter)pg_line_getxb, (setter)pg_line_setxb, NULL, NULL},
    {"yb", (getter)pg_line_getyb, (setter)pg_line_setyb, NULL, NULL},
    {"a", (getter)pg_line_geta, (setter)pg_line_seta, NULL, NULL},
    {"b", (getter)pg_line_getb, (setter)pg_line_setb, NULL, NULL},
    {"length", (getter)pg_line_getlength, NULL, NULL, NULL},
    {"slope", (getter)pg_line_getslope, NULL, NULL, NULL},
    {"center", (getter)pg_line_get_center, (setter)pg_line_set_center, NULL,
     NULL},
    {"centerx", (getter)pg_line_get_centerx, (setter)pg_line_set_centerx, NULL,
     NULL},
    {"centery", (getter)pg_line_get_centery, (setter)pg_line_set_centery, NULL,
     NULL},
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
