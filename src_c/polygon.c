#include "include/pygame.h"
#include "include/geometry.h"
#include "include/collisions.h"

#include <limits.h>
#include <float.h>
#include <stddef.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#ifndef M_PI_QUO_2
#define M_PI_QUO_2 1.57079632679489661923
#endif

#ifndef M_TWOPI
#define M_TWOPI 6.28318530717958647692
#endif

static PG_FORCE_INLINE void
PgFreePolygon(pgPolygonBase *poly)
{
    PyMem_Free(poly->vertices);
}

static PG_FORCE_INLINE double *
_pg_new_vertices_from_polygon(pgPolygonBase *polygon)
{
    double *vertices = PyMem_New(double, polygon->verts_num * 2);
    if (!vertices) {
        return NULL;
    }
    memcpy(vertices, polygon->vertices,
           polygon->verts_num * 2 * sizeof(double));

    return vertices;
}

static PG_FORCE_INLINE double *
_pg_new_vertices_from_vertices(double *vertices_to_copy, Py_ssize_t verts_num)
{
    double *vertices = PyMem_New(double, verts_num * 2);
    if (!vertices) {
        return NULL;
    }
    memcpy(vertices, vertices_to_copy, verts_num * 2 * sizeof(double));

    return vertices;
}

static int
_set_polygon_center_coords(pgPolygonBase *polygon)
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
_pg_move_polygon_helper(pgPolygonBase *polygon, double dx, double dy)
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
_pg_polygon_vertices_aslist(pgPolygonBase *poly)
{
    return pg_PointList_FromArrayDouble(poly->vertices,
                                        (int)poly->verts_num * 2);
}

static PyObject *
_pg_polygon_vertices_astuple(pgPolygonBase *poly)
{
    return pg_PointTuple_FromArrayDouble(poly->vertices,
                                         (int)poly->verts_num * 2);
}

static int
_pgPolygon_InitFromObject(PyObject *obj, pgPolygonBase *init_poly)
{
    /* This function always allocates new memory for the vertices, and
     * therefore it should be used only when the polygon is not yet
     * initialized. */
    Py_ssize_t length;

    /*If the Python object is already a pgPolygonBase object, copy the
     relevant information from that object to the init_poly object into
        the new memory. */
    if (pgPolygon_Check(obj)) {
        pgPolygonBase *poly = &pgPolygon_AsPolygon(obj);

        if (!(init_poly->vertices = _pg_new_vertices_from_polygon(poly))) {
            PyErr_Clear();
            return 0;
        }

        init_poly->verts_num = poly->verts_num;
        init_poly->c_x = poly->c_x;
        init_poly->c_y = poly->c_y;

        return 1;
    }

    /*If the Python object is a Fast sequence, extract the vertices of the
     polygon from the sequence*/
    if (PySequence_FAST_CHECK(obj)) {
        PyObject **f_arr = PySequence_Fast_ITEMS(obj);
        length = PySequence_Fast_GET_SIZE(obj);

        /*Make sure the sequence has at least 3 items (a polygon needs at
        least 3 vertices)*/
        if (length >= 3) {
            Py_ssize_t i;

            /*Allocate memory for the vertices of the polygon*/
            init_poly->vertices = PyMem_New(double, length * 2);
            if (!init_poly->vertices) {
                return 0;
            }

            /*Extract the x and y coordinates of each vertex and store them in
            the init_poly object's vertices array*/
            for (i = 0; i < length; i++) {
                double x, y;
                if (!pg_TwoDoublesFromObj(f_arr[i], &x, &y)) {
                    /* Note: not using PyMem_Free on polygon vertices on
                       failure because the pgPolygonBase is part of a Python
                       object, which will handle freeing the memory on
                       destruction. If we free the memory here, we will get a
                       double free error. */
                    return 0;
                }
                init_poly->vertices[i * 2] = x;
                init_poly->vertices[i * 2 + 1] = y;
                init_poly->c_x += x;
                init_poly->c_y += y;
            }

            init_poly->verts_num = length;
            /*Calculate the centroid of the polygon*/
            init_poly->c_x /= length;
            init_poly->c_y /= length;

            return 1;
        }
        /*If the sequence only has one item, attempt to initialize the
        init_poly object using that item*/
        else if (length == 1) {
            if (!_pgPolygon_InitFromObject(f_arr[0], init_poly)) {
                return 0;
            }
            return 1;
        }

        return 0;
    }

    /*If the Python object is not a Fast sequence but is still
     considered a sequence by PySequence_Check, extract the vertices of
     the polygon from the Sequence object*/
    else if (PySequence_Check(obj)) {
        /*Create an item variable to store the vertices of the polygon
         as they are extracted from the object*/
        PyObject *item = NULL;
        length = PySequence_Length(obj);

        /*Make sure the object has at least 3 items (a polygon needs at
         least 3 vertices)*/
        if (length >= 3) {
            Py_ssize_t i;

            /*Allocate memory for the vertices of the polygon*/
            init_poly->vertices = PyMem_New(double, length * 2);
            if (!init_poly->vertices) {
                return 0;
            }

            /*Extract the x and y coordinates of each vertex and store
            them in the init_poly object*/
            for (i = 0; i < length; i++) {
                double x, y;
                item = PySequence_ITEM(obj, i);
                if (!pg_TwoDoublesFromObj(item, &x, &y)) {
                    Py_DECREF(item);
                    /* Note: not using PyMem_Free on polygon vertices on
                       failure because the pgPolygonBase is part of a Python
                       object, which will handle freeing the memory on
                       destruction. If we free the memory here, we will get a
                       double free error. */
                    return 0;
                }
                Py_DECREF(item);

                init_poly->vertices[i * 2] = x;
                init_poly->vertices[i * 2 + 1] = y;
                init_poly->c_x += x;
                init_poly->c_y += y;
            }

            init_poly->verts_num = length;
            /*Calculate the centroid of the polygon*/
            init_poly->c_x /= length;
            init_poly->c_y /= length;

            return 1;
        }
        /*If the object only has one item, attempt to initialize the
        init_poly object using that item*/
        else if (length == 1) {
            item = PySequence_ITEM(obj, 0);
            /*If the item is a Unicode string or if the
            _pgPolygon_InitFromObject function fails, return 0
            indicating that the init_poly object could not be
            initialized*/
            if (PyUnicode_Check(obj) ||
                !_pgPolygon_InitFromObject(item, init_poly)) {
                Py_DECREF(item);
                return 0;
            }
            Py_DECREF(item);
            return 1;
        }

        return 0;
    }

    /*If the Python object has an attribute called "polygon", attempt
    to extract the vertices of the polygon from that attribute*/
    PyObject *polyattr;
    if (!(polyattr = PyObject_GetAttrString(obj, "polygon"))) {
        PyErr_Clear();
        return 0;
    }

    /*call if it's a method*/
    if (PyCallable_Check(polyattr)) {
        PyObject *polyresult = PyObject_CallObject(polyattr, NULL);
        Py_DECREF(polyattr);
        if (!polyresult) {
            PyErr_Clear();
            return 0;
        }
        polyattr = polyresult;
    }

    if (!_pgPolygon_InitFromObject(polyattr, init_poly)) {
        Py_DECREF(polyattr);
        return 0;
    }

    Py_DECREF(polyattr);

    return 1;
}

static int
pgPolygon_FromObject(PyObject *obj, pgPolygonBase *out, int *was_sequence)
{
    /* This function must only be utilized to try and convert a Polygon
     * compatible object to a pgPolygonBase object for use in the C
     * code. Once the object has been finalized, if its vertices came
     * from a sequence, the pgPolygonBase object's vertices must be
     * freed using the PyMem_Free function. The out_code variable is
     * used to store the type of object that was used to initialize the
     * pgPolygonBase object. The was_sequence variable should therefore
     * be used to determine whether the pgPolygonBase object's vertices
     * should be freed or not. The was_sequence variable can be one of
     * the following values:
     *
     * 0 - The object was already a pgPolygonBase object, so no
     * vertices will be allocated, you MUST NOT free the vertices after
     * use. 1 - The object was a sequence (i.e. a list, tuple, etc.) so
     * vertices were allocated, you MUST free the vertices after use.
     *
     * All of this is because you can't free memory from an actual
     * pgPolygonObject because it is using allocated memory already
     * whereas with sequences, you need to recreate the pgPolygonBase
     * object from the sequence, therefore you need to free the
     * vertices after use.
     */

    Py_ssize_t length;

    if (pgPolygon_Check(obj)) {
        /*Do a shallow copy of the pgPolygonBase object*/
        memcpy(out, &pgPolygon_AsPolygon(obj), sizeof(pgPolygonBase));
        *was_sequence = 0;
        return 1;
    }

    if (PySequence_FAST_CHECK(obj)) {
        PyObject **f_arr = PySequence_Fast_ITEMS(obj);
        length = PySequence_Fast_GET_SIZE(obj);

        if (length >= 3) {
            Py_ssize_t i;

            /*Allocate memory for the vertices of the polygon*/
            out->vertices = PyMem_New(double, length * 2);
            if (!out->vertices) {
                return 0;
            }

            for (i = 0; i < out->verts_num; i++) {
                double x, y;
                if (!pg_TwoDoublesFromObj(f_arr[i], &x, &y)) {
                    PgFreePolygon(out);
                    return 0;
                }
                out->vertices[i * 2] = x;
                out->vertices[i * 2 + 1] = y;
                out->c_x += x;
                out->c_y += y;
            }

            out->verts_num = length;
            /*Calculate the centroid of the polygon*/
            out->c_x /= length;
            out->c_y /= length;

            *was_sequence = 1;
            return 1;
        }
        else if (length == 1) {
            if (!pgPolygon_FromObject(f_arr[0], out, was_sequence)) {
                return 0;
            }
            *was_sequence = 1;
            return 1;
        }

        return 0;
    }

    else if (PySequence_Check(obj)) {
        /* Path for other sequences or Types that count as sequences*/
        PyObject *tmp = NULL;
        length = PySequence_Length(obj);

        if (length >= 3) {
            Py_ssize_t i;

            out->vertices = PyMem_New(double, length * 2);
            if (!out->vertices) {
                return 0;
            }

            for (i = 0; i < length; i++) {
                double x, y;
                tmp = PySequence_ITEM(obj, i);
                if (!pg_TwoDoublesFromObj(tmp, &x, &y)) {
                    Py_DECREF(tmp);
                    PgFreePolygon(out);
                    return 0;
                }
                Py_DECREF(tmp);
                out->vertices[i * 2] = x;
                out->vertices[i * 2 + 1] = y;
                out->c_x += x;
                out->c_y += y;
            }

            out->verts_num = length;
            out->c_x /= length;
            out->c_y /= length;

            *was_sequence = 1;
            return 1;
        }
        else if (length == 1) {
            tmp = PySequence_ITEM(obj, 0);
            if (PyUnicode_Check(obj) ||
                !pgPolygon_FromObject(tmp, out, was_sequence)) {
                Py_DECREF(tmp);
                return 0;
            }
            Py_DECREF(tmp);
            *was_sequence = 1;
            return 1;
        }

        return 0;
    }

    PyObject *polyattr;
    if (!(polyattr = PyObject_GetAttrString(obj, "polygon"))) {
        PyErr_Clear();
        return 0;
    }

    if (PyCallable_Check(polyattr)) /*call if it's a method*/
    {
        PyObject *polyresult = PyObject_CallObject(polyattr, NULL);
        Py_DECREF(polyattr);
        if (!polyresult) {
            PyErr_Clear();
            return 0;
        }
        polyattr = polyresult;
    }

    if (!pgPolygon_FromObject(polyattr, out, was_sequence)) {
        PyErr_Clear();
        Py_DECREF(polyattr);
        return 0;
    }

    Py_DECREF(polyattr);

    return 1;
}

static int
pgPolygon_FromObjectFastcall(PyObject *const *args, Py_ssize_t nargs,
                             pgPolygonBase *out, int *was_sequence)
{
    /* This function must only be utilized to try and convert a Polygon
     * compatible object to a pgPolygonBase object for use in the C
     * code ( in the case of a FASTCALL method). Once the object has
     * been finalized, if its vertices came from a sequence, the
     * pgPolygonBase object's vertices must be freed using the
     * PyMem_Free function. The out_code variable is used to store the
     * type of object that was used to initialize the pgPolygonBase
     * object. The was_sequence variable should therefore be used to
     * determine whether the pgPolygonBase object's vertices should be
     * freed or not. The was_sequence variable can be one of the
     * following values:
     *
     * 0 - The object was already a pgPolygonBase object, so no
     * vertices will be allocated, you MUST NOT free the vertices after
     * use. 1 - The object was a sequence (i.e. a list, tuple, etc.) so
     * vertices were allocated, you MUST free the vertices after use.
     * All of this is because you can't free memory from an actual
     * pgPolygonObject because it is using allocated memory already
     * whereas with sequences, you need to recreate the pgPolygonBase
     * object from the sequence, therefore you need to free the
     * vertices after use.
     */

    if (nargs == 1) {
        return pgPolygon_FromObject(args[0], out, was_sequence);
    }
    /* Make sure the object has at least 3 items (a polygon needs at
       least 3 vertices)*/
    else if (nargs >= 3) {
        Py_ssize_t i;

        out->vertices = PyMem_New(double, nargs * 2);
        if (!out->vertices) {
            return 0;
        }

        for (i = 0; i < nargs; i++) {
            double x, y;
            if (!pg_TwoDoublesFromObj(args[i], &x, &y)) {
                PgFreePolygon(out);
                return 0;
            }
            out->vertices[i * 2] = x;
            out->vertices[i * 2 + 1] = y;
            out->c_x += x;
            out->c_y += y;
        }

        out->verts_num = nargs;
        out->c_x /= nargs;
        out->c_y /= nargs;

        *was_sequence = 1;
        return 1;
    }

    return 0;
}

static int
pg_polygon_init(pgPolygonObject *self, PyObject *args, PyObject *kwds)
{
    if (!_pgPolygon_InitFromObject(args, &self->polygon)) {
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

    if (!polygon_obj) {
        return NULL;
    }

    if (!(polygon_obj->polygon.vertices =
              _pg_new_vertices_from_vertices(vertices, verts_num))) {
        Py_DECREF(polygon_obj);
        return NULL;
    }

    polygon_obj->polygon.verts_num = verts_num;
    _set_polygon_center_coords(&(polygon_obj->polygon));

    return (PyObject *)polygon_obj;
}

static PyObject *
_pg_polygon_subtype_new2_copy(PyTypeObject *type, pgPolygonBase *polygon)
{
    /* Copies an existing polygon type. Specifically it allocates new memory
     * for the vertices, but it doesn't recalculate the center of the polygon,
     * therefore saving performance */
    pgPolygonObject *polygon_obj =
        (pgPolygonObject *)pgPolygon_Type.tp_new(type, NULL, NULL);

    if (polygon->verts_num < 3) {
        /*A polygon requires 3 or more vertices*/
        Py_DECREF(polygon_obj);
        return NULL;
    }

    if (!polygon_obj) {
        return NULL;
    }

    if (!(polygon_obj->polygon.vertices =
              _pg_new_vertices_from_polygon(polygon))) {
        Py_DECREF(polygon_obj);
        return NULL;
    }

    polygon_obj->polygon.verts_num = polygon->verts_num;
    polygon_obj->polygon.c_x = polygon->c_x;
    polygon_obj->polygon.c_y = polygon->c_y;

    return (PyObject *)polygon_obj;
}

static PyObject *
_pg_polygon_subtype_new2_transfer(PyTypeObject *type, double *vertices,
                                  Py_ssize_t verts_num)
{
    pgPolygonObject *polygon_obj =
        (pgPolygonObject *)pgPolygon_Type.tp_new(type, NULL, NULL);

    if (!polygon_obj) {
        return NULL;
    }

    if (verts_num < 3 || !vertices) {
        /*A polygon requires 3 or more vertices*/
        Py_DECREF(polygon_obj);
        return NULL;
    }

    polygon_obj->polygon.vertices = vertices;
    polygon_obj->polygon.verts_num = verts_num;

    _set_polygon_center_coords(&(polygon_obj->polygon));

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
    PyObject *result, *verts, *verts_num;

    verts = _pg_polygon_vertices_aslist(&self->polygon);
    if (!verts) {
        return NULL;
    }
    verts_num = PyLong_FromLong((long)self->polygon.verts_num);
    if (!verts_num) {
        Py_DECREF(verts);
        return NULL;
    }

    result = PyUnicode_FromFormat("<Polygon(%R, %R)>", verts_num, verts);

    Py_DECREF(verts);
    Py_DECREF(verts_num);

    return result;
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
    double Dx, Dy;

    if (!pg_TwoDoublesFromFastcallArgs(args, nargs, &Dx, &Dy)) {
        return RAISE(PyExc_TypeError, "move requires a pair of numbers");
    }

    double *verts = PyMem_New(double, self->polygon.verts_num * 2);
    if (!verts) {
        return NULL;
    }
    memcpy(verts, self->polygon.vertices,
           self->polygon.verts_num * 2 * sizeof(double));

    Py_ssize_t i2;
    for (i2 = 0; i2 < self->polygon.verts_num * 2; i2 += 2) {
        verts[i2] += Dx;
        verts[i2 + 1] += Dy;
    }

    PyObject *tmp = _pg_polygon_subtype_new2_transfer(Py_TYPE(self), verts,
                                                      self->polygon.verts_num);
    if (!tmp) {
        PyMem_Free(verts);
        return NULL;
    }

    return tmp;
}

static PyObject *
pg_polygon_move_ip(pgPolygonObject *self, PyObject *const *args,
                   Py_ssize_t nargs)
{
    double Dx, Dy;

    if (!pg_TwoDoublesFromFastcallArgs(args, nargs, &Dx, &Dy)) {
        return RAISE(PyExc_TypeError, "move_ip requires a pair of numbers");
    }

    _pg_move_polygon_helper(&(self->polygon), Dx, Dy);

    Py_RETURN_NONE;
}

static PyObject *
pg_polygon_collidepoint(pgPolygonObject *self, PyObject *const *args,
                        Py_ssize_t nargs)
{
    double px, py;

    if (!pg_TwoDoublesFromFastcallArgs(args, nargs, &px, &py)) {
        return RAISE(
            PyExc_TypeError,
            "Polygon.collidepoint requires a point or PointLike object");
    }

    return PyBool_FromLong(pgCollision_PolygonPoint(&self->polygon, px, py));
}

static void
_pg_rotate_polygon_helper(pgPolygonBase *poly, double angle)
{
    double c_x = poly->c_x, c_y = poly->c_y;
    Py_ssize_t i2, verts_num = poly->verts_num;
    double *vertices = poly->vertices;

    /*convert the angle to radians*/
    double angle_rad = angle * M_PI / 180.0;

    if (fmod(angle_rad, M_PI_QUO_2) != 0.0) {
        /* handle the general angle case that's not 90, 180 or 270 degrees */
        double cos_a = cos(angle_rad) - 1;
        double sin_a = sin(angle_rad);

        for (i2 = 0; i2 < verts_num * 2; i2 += 2) {
            double dx = vertices[i2] - c_x;
            double dy = vertices[i2 + 1] - c_y;
            vertices[i2] += dx * cos_a - dy * sin_a;
            vertices[i2 + 1] += dx * sin_a + dy * cos_a;
        }
        return;
    }

    /*Ensure angle is between 0 and two pi*/
    angle_rad = fmod(angle_rad, M_TWOPI);
    if (angle_rad < 0) {
        angle_rad += M_TWOPI;
    }

    double v1, v2;
    /*special-cases rotation by 90, 180 and 270 degrees*/
    switch ((int)(angle_rad / M_PI_QUO_2)) {
        case 1:
            /*90 degrees*/
            v1 = c_x + c_y;
            v2 = c_y - c_x;
            for (i2 = 0; i2 < verts_num * 2; i2 += 2) {
                double tmp = vertices[i2];
                vertices[i2] = v1 - vertices[i2 + 1];
                vertices[i2 + 1] = v2 + tmp;
            }
            return;
        case 2:
            /*180 degrees*/
            v1 = c_x * 2;
            v2 = c_y * 2;
            for (i2 = 0; i2 < verts_num * 2; i2 += 2) {
                vertices[i2] = v1 - vertices[i2];
                vertices[i2 + 1] = v2 - vertices[i2 + 1];
            }
            return;
        case 3:
            /*270 degrees*/
            v1 = c_x + c_y;
            v2 = c_x - c_y;
            for (i2 = 0; i2 < verts_num * 2; i2 += 2) {
                double tmp = vertices[i2];
                vertices[i2] = v2 + vertices[i2 + 1];
                vertices[i2 + 1] = v1 - tmp;
            }
            return;
        default:
            /*should never happen*/
            break;
    }
}

static PyObject *
pg_polygon_rotate(pgPolygonObject *self, PyObject *arg)
{
    double angle;
    pgPolygonObject *ret;

    if (!pg_DoubleFromObj(arg, &angle)) {
        return RAISE(PyExc_TypeError,
                     "Invalid angle parameter, must be numeric");
    }

    if (!(ret = (pgPolygonObject *)_pg_polygon_subtype_new2_copy(
              Py_TYPE(self), &self->polygon))) {
        return NULL;
    }

    if (angle == 0.0 || fmod(angle, 360.0) == 0.0) {
        /* No rotation, return a copy */
        return (PyObject *)ret;
    }

    _pg_rotate_polygon_helper(&ret->polygon, angle);

    return (PyObject *)ret;
}

static PyObject *
pg_polygon_rotate_ip(pgPolygonObject *self, PyObject *arg)
{
    double angle;

    if (!pg_DoubleFromObj(arg, &angle)) {
        return RAISE(PyExc_TypeError,
                     "Invalid angle parameter, must be numeric");
    }

    if (angle == 0.0 || fmod(angle, 360.0) == 0.0) {
        /* No rotation, return None immediately */
        Py_RETURN_NONE;
    }

    _pg_rotate_polygon_helper(&self->polygon, angle);

    Py_RETURN_NONE;
}

static struct PyMethodDef pg_polygon_methods[] = {
    {"move", (PyCFunction)pg_polygon_move, METH_FASTCALL, NULL},
    {"move_ip", (PyCFunction)pg_polygon_move_ip, METH_FASTCALL, NULL},
    {"rotate", (PyCFunction)pg_polygon_rotate, METH_O, NULL},
    {"rotate_ip", (PyCFunction)pg_polygon_rotate_ip, METH_O, NULL},
    {"collidepoint", (PyCFunction)pg_polygon_collidepoint, METH_FASTCALL,
     NULL},
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

static int
pg_polygon_ass_vertex(pgPolygonObject *self, Py_ssize_t i, PyObject *v)
{
    pgPolygonBase *poly = &self->polygon;

    if (i < 0) {
        i += poly->verts_num;
    }

    if (i < 0 || i > poly->verts_num) {
        PyErr_SetString(PyExc_IndexError, "Invalid vertex Index");
        return -1;
    }

    double Vx, Vy;
    if (!pg_TwoDoublesFromObj(v, &Vx, &Vy)) {
        PyErr_SetString(PyExc_TypeError, "Must assign numeric values");
        return -1;
    }
    poly->vertices[i * 2] = Vx;
    poly->vertices[i * 2 + 1] = Vy;
    return 0;
}

static Py_ssize_t
pg_polygon_seq_length(pgPolygonObject *self)
{
    return pgPolygon_GETVERTSNUM(self);
}

static int
pg_polygon_ass_subscript(pgPolygonObject *self, PyObject *op, PyObject *value)
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
        return pg_polygon_ass_vertex(self, i, value);
    }
    else {
        PyErr_SetString(PyExc_TypeError, "Expected a number or sequence");
        return -1;
    }
}

static PyObject *
pg_polygon_subscript(pgPolygonObject *self, PyObject *op)
{
    PyObject *index = PyNumber_Index(op);
    Py_ssize_t i;

    if (!index) {
        return NULL;
    }
    i = PyNumber_AsSsize_t(index, NULL);
    Py_DECREF(index);

    pgPolygonBase *poly = &self->polygon;

    if (i < 0) {
        i += poly->verts_num;
    }

    if (i < 0 || i > poly->verts_num - 1) {
        return RAISE(PyExc_IndexError, "Invalid vertex Index");
    }

    return pg_TupleFromDoublePair(poly->vertices[i * 2],
                                  poly->vertices[i * 2 + 1]);
}

static int
pg_polygon_contains_seq(pgPolygonObject *self, PyObject *arg)
{
    double x, y;

    if (!pg_TwoDoublesFromObj(arg, &x, &y)) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
        return -1;
    }

    pgPolygonBase *poly = &self->polygon;
    Py_ssize_t i;
    for (i = 0; i < poly->verts_num; i++) {
        if (poly->vertices[i * 2] == x && poly->vertices[i * 2 + 1] == y) {
            return 1;
        }
    }

    return 0;
}

static PyMappingMethods pg_polygon_as_mapping = {
    .mp_subscript = (binaryfunc)pg_polygon_subscript,
    .mp_ass_subscript = (objobjargproc)pg_polygon_ass_subscript,
    .mp_length = (lenfunc)pg_polygon_seq_length};

static PySequenceMethods pg_polygon_as_sequence = {
    .sq_length = (lenfunc)pg_polygon_seq_length,
    .sq_item = (ssizeargfunc)pg_polygon_subscript,
    .sq_ass_item = (ssizeobjargproc)pg_polygon_ass_subscript,
    .sq_contains = (objobjproc)pg_polygon_contains_seq,
};

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
    _pg_move_polygon_helper(&(self->polygon), (val - self->polygon.c_x), 0.0);
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
    _pg_move_polygon_helper(&(self->polygon), 0.0, (val - self->polygon.c_y));
    return 0;
}

static PyObject *
pg_polygon_get_center(pgPolygonObject *self, void *closure)
{
    return pg_TupleFromDoublePair(self->polygon.c_x, self->polygon.c_y);
}

static PG_FORCEINLINE double
_pg_distance(double x1, double y1, double x2, double y2)
{
    double dx = x2 - x1;
    double dy = y2 - y1;
    return sqrt(dx * dx + dy * dy);
}

static PyObject *
pg_polygon_get_perimeter(pgPolygonObject *self, void *closure)
{
    double perimeter = 0;
    double *vertices = self->polygon.vertices;
    Py_ssize_t i;
    for (i = 0; i < self->polygon.verts_num - 1; i++) {
        perimeter +=
            _pg_distance(vertices[i * 2], vertices[i * 2 + 1],
                         vertices[(i + 1) * 2], vertices[(i + 1) * 2 + 1]);
    }
    perimeter += _pg_distance(vertices[i * 2], vertices[i * 2 + 1],
                              vertices[0], vertices[1]);

    return PyFloat_FromDouble(perimeter);
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
    _pg_move_polygon_helper(&(self->polygon), (new_c_x - self->polygon.c_x),
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
    {"perimeter", (getter)pg_polygon_get_perimeter, NULL,
     "Perimeter of the polygon", NULL},
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
    .tp_as_mapping = &pg_polygon_as_mapping,
    .tp_as_sequence = &pg_polygon_as_sequence,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = NULL,
    .tp_weaklistoffset = offsetof(pgPolygonObject, weakreflist),
    .tp_methods = pg_polygon_methods,
    .tp_getset = pg_polygon_getsets,
    .tp_init = (initproc)pg_polygon_init,
    .tp_new = pg_polygon_new,
};