#include "include/geometry.h"
#include "include/collisions.h"

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
    polygon->centerx = sum_x / polygon->verts_num;
    polygon->centery = sum_y / polygon->verts_num;
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
    /* This function initializes a Polygon object. It can resize the memory
     * for the vertices if needed, and therefore it should be used only when
     * the polygon is not yet initialized. */
    Py_ssize_t length;

    /* If the Python object is already a pgPolygonBase object, copy the
     * relevant information from that object to the init_poly object into
     * the memory, resize if needed. */
    if (pgPolygon_Check(obj)) {
        pgPolygonBase *poly = &pgPolygon_AsPolygon(obj);

        /* Copy the vertices from the old polygon to the new polygon, while
         * also allocating new memory. Resize the vertices array if needed. */
        if (poly->verts_num > 3) {
            PyMem_Resize(init_poly->vertices, double, poly->verts_num * 2);
            if (!init_poly->vertices) {
                return 0;
            }
        }
        memcpy(init_poly->vertices, poly->vertices,
               poly->verts_num * 2 * sizeof(double));

        init_poly->verts_num = poly->verts_num;
        init_poly->centerx = poly->centerx;
        init_poly->centery = poly->centery;

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

            /* Resize the vertices array if needed. */
            if (length > 3) {
                PyMem_Resize(init_poly->vertices, double, length * 2);
                if (!init_poly->vertices) {
                    return 0;
                }
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
                init_poly->centerx += x;
                init_poly->centery += y;
            }

            init_poly->verts_num = length;
            /*Calculate the centroid of the polygon*/
            init_poly->centerx /= length;
            init_poly->centery /= length;

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
            if (length > 3) {
                PyMem_Resize(init_poly->vertices, double, length * 2);
                if (!init_poly->vertices) {
                    return 0;
                }
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
                init_poly->centerx += x;
                init_poly->centery += y;
            }

            init_poly->verts_num = length;
            /*Calculate the centroid of the polygon*/
            init_poly->centerx /= length;
            init_poly->centery /= length;

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

    /* If the Python object is an iterable sequence (generator) */
    else if (PyIter_Check(obj)) {
        PyObject *item = NULL;
        PyObject *iter = PyObject_GetIter(obj);
        Py_ssize_t i = 0, currently_allocated = 3;

        /* Extract the x and y coordinates of each vertex and store
           them in the init_poly object */
        while ((item = PyIter_Next(iter))) {
            double x, y;
            if (!pg_TwoDoublesFromObj(item, &x, &y)) {
                Py_DECREF(item);
                Py_DECREF(iter);
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
            init_poly->centerx += x;
            init_poly->centery += y;

            i++;
            if (i + 1 > currently_allocated) {
                /* Reallocate memory for the vertices of the polygon to 50%
                   more than the current size */
                currently_allocated = (currently_allocated * 3) / 2;
                init_poly->vertices = PyMem_Resize(init_poly->vertices, double,
                                                   2 * currently_allocated);
                if (!init_poly->vertices) {
                    Py_DECREF(iter);
                    return 0;
                }
            }
        }

        if (i < 3) {
            Py_DECREF(iter);
            return 0;
        }

        /* Shrink the allocated memory to the actual size if necessary */
        if (i < currently_allocated) {
            init_poly->vertices =
                PyMem_Resize(init_poly->vertices, double, 2 * i);
            if (!init_poly->vertices) {
                Py_DECREF(iter);
                return 0;
            }
        }

        Py_DECREF(iter);

        init_poly->verts_num = i;
        /* Calculate the centroid of the polygon */
        init_poly->centerx /= i;
        init_poly->centery /= i;

        return 1;
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
    /* This function converts a Polygon compatible object to a pgPolygonBase
     * object for use in C code. The "was_sequence" parameter indicates whether
     * the object being converted was a sequence (1) or a pgPolygonBase struct
     * (0). The "was_sequence" parameter should be used to determine whether to
     * free the vertices of the pgPolygonBase object after use.
     *
     * 1. If "was_sequence" is 0, the object being converted was a
     * pgPolygonBase struct. In this case, the vertices of the pgPolygonBase
     * object do not need to be freed because they are part of the object
     * and were not newly allocated.
     *
     * 2. If "was_sequence" is 1, the object being converted was a
     * sequence (such as a list or tuple). In this case, the vertices of the
     * pgPolygonBase's vertices must be freed using PyMem_Free after the object
     * has been utilized, as they were allocated when the object was created
     * from the sequence.
     *
     *  If the object being converted is a pgPolygonBase struct, the conversion
     *  is more performant as it avoids a whole memory allocation and memcpy
     *  (just doing a shallow copy), as well as making the other functions
     *  that utilize this one simpler.
     */

    Py_ssize_t length;

    if (pgPolygon_Check(obj)) {
        /*Do a shallow copy of the pgPolygonBase object*/
        *was_sequence = 0;
        memcpy(out, &pgPolygon_AsPolygon(obj), sizeof(pgPolygonBase));
        return 1;
    }

    if (PySequence_FAST_CHECK(obj)) {
        *was_sequence = 1;
        PyObject **f_arr = PySequence_Fast_ITEMS(obj);
        length = PySequence_Fast_GET_SIZE(obj);

        if (length >= 3) {
            Py_ssize_t i;

            /*Allocate memory for the vertices of the polygon*/
            out->vertices = PyMem_New(double, length * 2);
            if (!out->vertices) {
                return 0;
            }

            for (i = 0; i < length; i++) {
                double x, y;
                if (!pg_TwoDoublesFromObj(f_arr[i], &x, &y)) {
                    PyMem_Free(out->vertices);
                    return 0;
                }
                out->vertices[i * 2] = x;
                out->vertices[i * 2 + 1] = y;
                out->centerx += x;
                out->centery += y;
            }

            out->verts_num = length;
            /*Calculate the centroid of the polygon*/
            out->centerx /= length;
            out->centery /= length;

            return 1;
        }
        else if (length == 1) {
            if (!pgPolygon_FromObject(f_arr[0], out, was_sequence)) {
                return 0;
            }
            return 1;
        }
        /*Length is 0 or 2 -> invalid polygon*/
        return 0;
    }

    else if (PySequence_Check(obj)) {
        /* Path for other sequences or Types that count as sequences*/
        *was_sequence = 1;
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
                    PyMem_Free(out->vertices);
                    return 0;
                }
                Py_DECREF(tmp);
                out->vertices[i * 2] = x;
                out->vertices[i * 2 + 1] = y;
                out->centerx += x;
                out->centery += y;
            }

            out->verts_num = length;
            out->centerx /= length;
            out->centery /= length;

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
            return 1;
        }
        /*Length is 0 or 2 -> invalid polygon*/
        return 0;
    }

    /* If the object is not a sequence, attempt to extract the vertices of the
     * polygon from the object's "polygon" attribute */
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
    /* This function converts a Polygon compatible object to a pgPolygonBase
     * object for use in C code (in the case of a FASTCALL method).
     * The "was_sequence" parameter indicates whether the object being
     * converted was a sequence (1) or a pgPolygonBase struct (0). The
     * "was_sequence" parameter should be used to determine whether to free the
     * vertices of the pgPolygonBase object after use.
     *
     * 1. If "was_sequence" is 0, the object being converted was a
     * pgPolygonBase struct. In this case, the vertices of the pgPolygonBase
     * object do not need to be freed because they are part of the object
     * and were not newly allocated.
     *
     * 2. If "was_sequence" is 1, the object being converted was a
     * sequence (such as a list or tuple). In this case, the vertices of the
     * pgPolygonBase's vertices must be freed using PyMem_Free after the object
     * has been utilized, as they were allocated when the object was created
     * from the sequence.
     *
     *  If the object being converted is a pgPolygonBase struct, the conversion
     *  is more performant as it avoids a whole memory allocation and memcpy
     *  (just doing a shallow copy), as well as making the other functions
     *  that utilize this one simpler.
     */

    if (nargs == 1) {
        return pgPolygon_FromObject(args[0], out, was_sequence);
    }
    /* Make sure the object has at least 3 items (a polygon needs at
       least 3 vertices)*/
    else if (nargs >= 3) {
        Py_ssize_t i;

        *was_sequence = 1;

        out->vertices = PyMem_New(double, nargs * 2);
        if (!out->vertices) {
            return 0;
        }

        for (i = 0; i < nargs; i++) {
            double x, y;
            if (!pg_TwoDoublesFromObj(args[i], &x, &y)) {
                PyMem_Free(out->vertices);
                return 0;
            }
            out->vertices[i * 2] = x;
            out->vertices[i * 2 + 1] = y;
            out->centerx += x;
            out->centery += y;
        }

        out->verts_num = nargs;
        out->centerx /= nargs;
        out->centery /= nargs;

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

static pgPolygonObject *
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
    polygon_obj->polygon.centerx = polygon->centerx;
    polygon_obj->polygon.centery = polygon->centery;

    return polygon_obj;
}

static PyObject *
pg_polygon_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    pgPolygonObject *self = (pgPolygonObject *)type->tp_alloc(type, 0);

    if (self) {
        self->polygon.vertices = PyMem_New(double, 6);
        if (!self->polygon.vertices) {
            Py_DECREF(self);
            return NULL;
        }
        self->polygon.verts_num = 3;
        self->polygon.centerx = 0;
        self->polygon.centery = 0;
        self->weakreflist = NULL;
    }

    return (PyObject *)self;
}

static PyObject *
pgPolygon_New(pgPolygonBase *p)
{
    return (PyObject *)_pg_polygon_subtype_new2_copy(&pgPolygon_Type, p);
}

static PyObject *
pgPolygon_New2(double *vertices, Py_ssize_t verts_num)
{
    return _pg_polygon_subtype_new2(&pgPolygon_Type, vertices, verts_num);
}

static PyObject *
pgPolygon_New4(double *vertices, Py_ssize_t verts_num, double centerx,
               double centery)
{
    pgPolygonObject *polygon_obj =
        (pgPolygonObject *)pgPolygon_Type.tp_new(&pgPolygon_Type, NULL, NULL);

    if (!polygon_obj) {
        return NULL;
    }

    if (verts_num < 3 || !vertices) {
        /*A polygon requires 3 or more vertices*/
        Py_DECREF(polygon_obj);
        return NULL;
    }

    if (!(polygon_obj->polygon.vertices =
              _pg_new_vertices_from_vertices(vertices, verts_num))) {
        Py_DECREF(polygon_obj);
        return NULL;
    }

    polygon_obj->polygon.verts_num = verts_num;
    polygon_obj->polygon.centerx = centerx;
    polygon_obj->polygon.centery = centery;

    return (PyObject *)polygon_obj;
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

static void
_pg_move_polygon_helper(pgPolygonBase *polygon, double dx, double dy)
{
    if (!dx && !dy) {
        return;
    }

    polygon->centerx += dx;
    polygon->centery += dy;

    Py_ssize_t i2;
    double *vertices = polygon->vertices;
    if (dx) {
        if (dy) {
            for (i2 = 0; i2 < polygon->verts_num * 2; i2 += 2) {
                vertices[i2] += dx;
                vertices[i2 + 1] += dy;
            }
            return;
        }
        for (i2 = 0; i2 < polygon->verts_num * 2; i2 += 2) {
            vertices[i2] += dx;
        }
        return;
    }

    if (dy) {
        for (i2 = 1; i2 < polygon->verts_num * 2; i2 += 2) {
            vertices[i2] += dy;
        }
    }
}

static PyObject *
pg_polygon_move(pgPolygonObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    double Dx, Dy;
    pgPolygonObject *ret;

    if (!pg_TwoDoublesFromFastcallArgs(args, nargs, &Dx, &Dy)) {
        return RAISE(PyExc_TypeError, "move requires a pair of numbers");
    }

    ret = _pg_polygon_subtype_new2_copy(Py_TYPE(self), &self->polygon);
    if (!ret) {
        return NULL;
    }

    _pg_move_polygon_helper(&ret->polygon, Dx, Dy);

    return (PyObject *)ret;
}

static PyObject *
pg_polygon_as_segments(pgPolygonObject *self, PyObject *_null)
{
    double *vertices = self->polygon.vertices;
    Py_ssize_t verts_num = self->polygon.verts_num;
    Py_ssize_t verts_num_double = verts_num * 2;

    PyObject *list = PyList_New(verts_num);
    if (!list) {
        return NULL;
    }

    for (Py_ssize_t i = 0; i < verts_num; i++) {
        Py_ssize_t i2 = i * 2;
        PyObject *line = pgLine_New4(vertices[i2], vertices[i2 + 1],
                                     vertices[(i2 + 2) % verts_num_double],
                                     vertices[(i2 + 3) % verts_num_double]);
        if (!line) {
            Py_DECREF(list);
            return NULL;
        }

        PyList_SET_ITEM(list, i, line);
    }

    return list;
}

static PyObject *
pg_polygon_move_ip(pgPolygonObject *self, PyObject *const *args,
                   Py_ssize_t nargs)
{
    double Dx, Dy;

    if (!pg_TwoDoublesFromFastcallArgs(args, nargs, &Dx, &Dy)) {
        return RAISE(PyExc_TypeError, "move_ip requires a pair of numbers");
    }

    _pg_move_polygon_helper(&self->polygon, Dx, Dy);

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

static PyObject *
pg_polygon_insert_vertex(pgPolygonObject *self, PyObject *const *args,
                         Py_ssize_t nargs)
{
    double x, y;
    pgPolygonBase *poly = &self->polygon;
    Py_ssize_t v_ix, v_num = poly->verts_num;

    if (nargs != 2) {
        return RAISE(PyExc_TypeError,
                     "insert_vertex requires a vertex index and a vertex");
    }

    if (!pg_IndexFromObj(args[0], &v_ix)) {
        return RAISE(PyExc_TypeError, "Invalid vertex index");
    }

    if (!pg_TwoDoublesFromObj(args[1], &x, &y)) {
        return RAISE(PyExc_TypeError, "Invalid vertex coordinate");
    }

    PyMem_Resize(poly->vertices, double, v_num * 2 + 2);

    if (!poly->vertices) {
        return PyErr_NoMemory();
    }

    if (v_ix < 0) {
        v_ix += v_num + 1;
        if (v_ix < 0) {
            v_ix = 0;
        }
    }
    else if (v_ix > v_num) {
        v_ix = v_num;
    }

    if (v_ix < v_num) {
        memmove(poly->vertices + v_ix * 2 + 2, poly->vertices + v_ix * 2,
                (v_num - v_ix) * 2 * sizeof(double));
    }

    poly->vertices[v_ix * 2] = x;
    poly->vertices[v_ix * 2 + 1] = y;

    poly->centerx = (poly->centerx * v_num + x) / (v_num + 1);
    poly->centery = (poly->centery * v_num + y) / (v_num + 1);

    poly->verts_num++;

    Py_RETURN_NONE;
}

static PyObject *
pg_polygon_remove_vertex(pgPolygonObject *self, PyObject *arg)
{
    pgPolygonBase *poly = &self->polygon;
    Py_ssize_t v_ix, v_num = poly->verts_num;

    if (v_num == 3) {
        return RAISE(PyExc_TypeError,
                     "Cannot remove a vertex from a triangle");
    }

    if (!pg_IndexFromObj(arg, &v_ix)) {
        return RAISE(PyExc_TypeError, "Invalid vertex index");
    }

    if (v_ix < 0) {
        v_ix += v_num;
        if (v_ix < 0) {
            v_ix = 0;
        }
    }
    else if (v_ix >= v_num) {
        return RAISE(PyExc_IndexError, "vertex index out of range");
    }

    poly->centerx =
        (poly->centerx * v_num - poly->vertices[v_ix * 2]) / (v_num - 1);
    poly->centery =
        (poly->centery * v_num - poly->vertices[v_ix * 2 + 1]) / (v_num - 1);

    if (v_ix < v_num) {
        memmove(poly->vertices + v_ix * 2, poly->vertices + v_ix * 2 + 2,
                (v_num - v_ix - 1) * 2 * sizeof(double));
    }

    PyMem_Resize(poly->vertices, double, v_num * 2 - 2);

    if (!poly->vertices) {
        return PyErr_NoMemory();
    }

    poly->verts_num--;

    Py_RETURN_NONE;
}

static PyObject *
pg_polygon_pop_vertex(pgPolygonObject *self, PyObject *arg)
{
    pgPolygonBase *poly = &self->polygon;
    Py_ssize_t v_ix = -1, v_num = poly->verts_num;

    if (v_num == 3) {
        return RAISE(PyExc_TypeError, "Cannot pop a vertex from a triangle");
    }

    if (!pg_IndexFromObj(arg, &v_ix)) {
        return RAISE(PyExc_TypeError, "Invalid vertex index");
    }

    if (v_ix < 0) {
        v_ix += v_num;
        if (v_ix < 0) {
            v_ix = 0;
        }
    }
    else if (v_ix >= v_num) {
        return RAISE(PyExc_IndexError, "Vertex index out of range");
    }

    poly->centerx =
        (poly->centerx * v_num - poly->vertices[v_ix * 2]) / (v_num - 1);
    poly->centery =
        (poly->centery * v_num - poly->vertices[v_ix * 2 + 1]) / (v_num - 1);

    PyObject *vertex = pg_TupleFromDoublePair(poly->vertices[v_ix * 2],
                                              poly->vertices[v_ix * 2 + 1]);
    if (!vertex) {
        return NULL;
    }

    if (v_ix < v_num) {
        memmove(poly->vertices + v_ix * 2, poly->vertices + v_ix * 2 + 2,
                (v_num - v_ix - 1) * 2 * sizeof(double));
    }

    PyMem_Resize(poly->vertices, double, v_num * 2 - 2);

    if (!poly->vertices) {
        return PyErr_NoMemory();
    }

    poly->verts_num--;

    return vertex;
}

static void
_pg_rotate_polygon_helper(pgPolygonBase *poly, double angle, double rx,
                          double ry)
{
    if (angle == 0.0 || fmod(angle, 360.0) == 0.0) {
        return;
    }
    Py_ssize_t i2, verts_num = poly->verts_num;
    double *vertices = poly->vertices;

    /*convert the angle to radians*/
    double angle_rad = DEG_TO_RAD(angle);

    if (fmod(angle_rad, M_PI_QUO_2) != 0.0) {
        /* handle the general angle case that's not 90, 180 or 270 degrees */
        double c = cos(angle_rad) - 1;
        double s = sin(angle_rad);

        for (i2 = 0; i2 < verts_num * 2; i2 += 2) {
            double dx = vertices[i2] - rx;
            double dy = vertices[i2 + 1] - ry;
            vertices[i2] += dx * c - dy * s;
            vertices[i2 + 1] += dx * s + dy * c;
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
            v1 = rx + ry;
            v2 = ry - rx;
            for (i2 = 0; i2 < verts_num * 2; i2 += 2) {
                double tmp = vertices[i2];
                vertices[i2] = v1 - vertices[i2 + 1];
                vertices[i2 + 1] = v2 + tmp;
            }
            return;
        case 2:
            /*180 degrees*/
            v1 = rx * 2;
            v2 = ry * 2;
            for (i2 = 0; i2 < verts_num * 2; i2 += 2) {
                vertices[i2] = v1 - vertices[i2];
                vertices[i2 + 1] = v2 - vertices[i2 + 1];
            }
            return;
        case 3:
            /*270 degrees*/
            v1 = rx + ry;
            v2 = rx - ry;
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
pg_polygon_rotate(pgPolygonObject *self, PyObject *const *args,
                  Py_ssize_t nargs)
{
    if (!nargs || nargs > 2) {
        return RAISE(PyExc_TypeError, "rotate requires 1 or 2 arguments");
    }

    pgPolygonObject *ret;
    pgPolygonBase *poly = &self->polygon;
    double angle, rx = poly->centerx, ry = poly->centery;

    /*get the angle argument*/
    if (!pg_DoubleFromObj(args[0], &angle)) {
        return RAISE(PyExc_TypeError,
                     "Invalid angle argument, must be numeric");
    }

    /*get the rotation point argument if given*/
    if (nargs == 2 && !pg_TwoDoublesFromObj(args[1], &rx, &ry)) {
        return RAISE(PyExc_TypeError,
                     "Invalid rotation_point argument, must be a sequence of "
                     "two numbers");
    }

    ret = _pg_polygon_subtype_new2_copy(Py_TYPE(self), poly);
    if (!ret) {
        return NULL;
    }

    _pg_rotate_polygon_helper(&ret->polygon, angle, rx, ry);

    return (PyObject *)ret;
}

static PyObject *
pg_polygon_rotate_ip(pgPolygonObject *self, PyObject *const *args,
                     Py_ssize_t nargs)
{
    if (!nargs || nargs > 2) {
        return RAISE(PyExc_TypeError, "rotate_ip requires 1 or 2 arguments");
    }

    pgPolygonBase *poly = &self->polygon;
    double angle;
    double rx = poly->centerx, ry = poly->centery;

    /*get the angle argument*/
    if (!pg_DoubleFromObj(args[0], &angle)) {
        return RAISE(PyExc_TypeError,
                     "Invalid angle argument, must be numeric");
    }

    /*get the rotation point argument if given*/
    if (nargs == 2 && !pg_TwoDoublesFromObj(args[1], &rx, &ry)) {
        return RAISE(PyExc_TypeError,
                     "Invalid rotation_point argument, must be a sequence of "
                     "two numbers");
    }

    _pg_rotate_polygon_helper(&self->polygon, angle, rx, ry);

    Py_RETURN_NONE;
}

static PyObject *
pg_polygon_as_rect(pgPolygonObject *self, PyObject *_null)
{
    /* Return a Rect object that is the smallest rectangle that contains
       the polygon. */
    double min_x, min_y, max_x, max_y;
    double *vertices = self->polygon.vertices;
    Py_ssize_t i2, verts_num = self->polygon.verts_num;

    min_x = max_x = vertices[0];
    min_y = max_y = vertices[1];

    for (i2 = 2; i2 < verts_num * 2; i2 += 2) {
        min_x = MIN(min_x, vertices[i2]);
        min_y = MIN(min_y, vertices[i2 + 1]);
        max_x = MAX(max_x, vertices[i2]);
        max_y = MAX(max_y, vertices[i2 + 1]);
    }

    return pgRect_New4((int)floor(min_x), (int)floor(min_y),
                       (int)ceil(max_x - min_x + 1),
                       (int)ceil(max_y - min_y + 1));
}

/*
 * this function takes in `pgPolygonBase *` and
 * it returns an int representing whether the polygon is convex or not
 * (concave)
 */
static int
_pg_polygon_is_convex_helper(pgPolygonBase *poly)
{
    /* A polygon is convex if and only if the cross products of all the
     * adjacent edges are all of the same sign.
     */
    Py_ssize_t i, i0, i1, i2;
    Py_ssize_t verts_num = poly->verts_num;
    Py_ssize_t count = 2 * verts_num;
    double *vertices = poly->vertices;
    int sign = 0;

    for (i = 0; i < verts_num; i++) {
        i0 = 2 * i % count;
        i1 = 2 * (i + 1) % count;
        i2 = 2 * (i + 2) % count;
        double dx1 = vertices[i1] - vertices[i0];
        double dy1 = vertices[i1 + 1] - vertices[i0 + 1];
        double dx2 = vertices[i2] - vertices[i1];
        double dy2 = vertices[i2 + 1] - vertices[i1 + 1];

        double cross = dx1 * dy2 - dy1 * dx2;

        if (cross == 0) {
            /* The polygon is not convex if any two edges are colinear. */
            return 0;
        }
        else if (sign == 0) {
            sign = cross < 0 ? -1 : 1;
        }
        else if ((sign == -1 && cross > 0) || (sign == 1 && cross < 0)) {
            /* The polygon is not convex if the cross products of any
             * two adjacent edges are of different signs.
             */
            return 0;
        }
    }

    return 1;
}

static PyObject *
pg_polygon_is_convex(pgPolygonObject *self, PyObject *_null)
{
    return PyBool_FromLong(_pg_polygon_is_convex_helper(&self->polygon));
}
static int
_pg_polygon_scale_helper(pgPolygonBase *poly, double factor)
{
    /* Takes in a factor and scales the polygon by that factor,
     * if the factor is less than 1, the polygon will be shrunk, if the
     * factor is greater than 1, the polygon will be enlarged.
     */
    if (factor == 1.0) {
        return 1;
    }
    else if (factor <= 0.0) {
        PyErr_SetString(PyExc_ValueError, "Invalid scale factor, must be > 0");
        return 0;
    }

    double *vertices = poly->vertices;
    double one_m_fac = 1.0 - factor;
    double omf_cx = one_m_fac * poly->centerx;
    double omf_cy = one_m_fac * poly->centery;

    Py_ssize_t i2;
    for (i2 = 0; i2 < poly->verts_num * 2; i2 += 2) {
        vertices[i2] = vertices[i2] * factor + omf_cx;
        vertices[i2 + 1] = vertices[i2 + 1] * factor + omf_cy;
    }
    return 1;
}

static PyObject *
pg_polygon_scale(pgPolygonObject *self, PyObject *arg)
{
    double factor;
    pgPolygonObject *new_poly;

    if (!pg_DoubleFromObj(arg, &factor)) {
        return RAISE(PyExc_TypeError, "Invalid scale factor, must be numeric");
    }

    if (!(new_poly = (pgPolygonObject *)_pg_polygon_subtype_new2_copy(
              Py_TYPE(self), &self->polygon))) {
        return NULL;
    }

    if (!_pg_polygon_scale_helper(&new_poly->polygon, factor)) {
        Py_DECREF(new_poly);
        return NULL;
    }

    return (PyObject *)new_poly;
}

static PyObject *
pg_polygon_scale_ip(pgPolygonObject *self, PyObject *arg)
{
    double factor;

    if (!pg_DoubleFromObj(arg, &factor)) {
        return RAISE(PyExc_TypeError, "Invalid scale factor, must be numeric");
    }

    if (!_pg_polygon_scale_helper(&self->polygon, factor)) {
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_polygon_collideline(pgPolygonObject *self, PyObject *const *args,
                       Py_ssize_t nargs)
{
    pgLineBase line;
    int only_edges = 0;

    /* Check for the optional only_edges argument */
    if (PyBool_Check(args[nargs - 1])) {
        only_edges = args[nargs - 1] == Py_True;
        nargs--;
    }

    if (!pgLine_FromObjectFastcall(args, nargs, &line)) {
        return RAISE(PyExc_TypeError, "Invalid line parameter");
    }

    return PyBool_FromLong(
        pgCollision_PolygonLine(&self->polygon, &line, only_edges));
}

static PyObject *
pg_polygon_collidecircle(pgPolygonObject *self, PyObject *const *args,
                         Py_ssize_t nargs)
{
    pgCircleBase circle;
    int only_edges = 0;

    /* Check for the optional only_edges argument */
    if (PyBool_Check(args[nargs - 1])) {
        only_edges = args[nargs - 1] == Py_True;
        nargs--;
    }

    if (!pgCircle_FromObjectFastcall(args, nargs, &circle)) {
        return RAISE(PyExc_TypeError, "Invalid circle parameter");
    }

    return PyBool_FromLong(
        pgCollision_CirclePolygon(&circle, &self->polygon, only_edges));
}

static void
pg_polygon_flip_helper(pgPolygonBase *poly, int dirx, int diry, double c_x,
                       double c_y)
{
    Py_ssize_t i2, verts_num = poly->verts_num;
    double *vertices = poly->vertices;

    if (dirx && diry) {
        for (i2 = 0; i2 < verts_num * 2; i2 += 2) {
            vertices[i2] = c_x - (vertices[i2] - c_x);
            vertices[i2 + 1] = c_y - (vertices[i2 + 1] - c_y);
        }
        return;
    }

    if (dirx) {
        for (i2 = 0; i2 < verts_num * 2; i2 += 2) {
            vertices[i2] = c_x - (vertices[i2] - c_x);
        }
        return;
    }

    for (i2 = 0; i2 < verts_num * 2; i2 += 2) {
        vertices[i2 + 1] = c_y - (vertices[i2 + 1] - c_y);
    }
}

#define FLIP_PREP                                                         \
    pgPolygonBase *poly = &self->polygon;                                 \
    int dirx, diry = 0;                                                   \
    double c_x = poly->centerx, c_y = poly->centery;                      \
    if (!nargs || nargs > 3) {                                            \
        return RAISE(                                                     \
            PyExc_TypeError,                                              \
            "Invalid number of arguments, expected 1, 2 or 3 arguments"); \
    }                                                                     \
    dirx = PyObject_IsTrue(args[0]);                                      \
    if (nargs >= 2) {                                                     \
        diry = PyObject_IsTrue(args[1]);                                  \
    }                                                                     \
    if (nargs == 3 && !pg_TwoDoublesFromObj(args[2], &c_x, &c_y)) {       \
        return RAISE(PyExc_TypeError,                                     \
                     "Invalid flip point argument, must be a sequence "   \
                     "of two numbers");                                   \
    }

static PyObject *
pg_polygon_flip(pgPolygonObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    FLIP_PREP

    pgPolygonObject *ret = _pg_polygon_subtype_new2_copy(Py_TYPE(self), poly);
    if (!ret) {
        return NULL;
    }

    pg_polygon_flip_helper(&ret->polygon, dirx, diry, c_x, c_y);

    return (PyObject *)ret;
}

static PyObject *
pg_polygon_flip_ip(pgPolygonObject *self, PyObject *const *args,
                   Py_ssize_t nargs)
{
    FLIP_PREP

    pg_polygon_flip_helper(poly, dirx, diry, c_x, c_y);

    Py_RETURN_NONE;
}
#undef FLIP_PREP

static struct PyMethodDef pg_polygon_methods[] = {
    {"as_segments", (PyCFunction)pg_polygon_as_segments, METH_NOARGS, NULL},
    {"move", (PyCFunction)pg_polygon_move, METH_FASTCALL, NULL},
    {"move_ip", (PyCFunction)pg_polygon_move_ip, METH_FASTCALL, NULL},
    {"rotate", (PyCFunction)pg_polygon_rotate, METH_FASTCALL, NULL},
    {"rotate_ip", (PyCFunction)pg_polygon_rotate_ip, METH_FASTCALL, NULL},
    {"collidepoint", (PyCFunction)pg_polygon_collidepoint, METH_FASTCALL,
     NULL},
    {"collideline", (PyCFunction)pg_polygon_collideline, METH_FASTCALL, NULL},
    {"collidecircle", (PyCFunction)pg_polygon_collidecircle, METH_FASTCALL,
     NULL},
    {"as_rect", (PyCFunction)pg_polygon_as_rect, METH_NOARGS, NULL},
    {"is_convex", (PyCFunction)pg_polygon_is_convex, METH_NOARGS, NULL},
    {"__copy__", (PyCFunction)pg_polygon_copy, METH_NOARGS, NULL},
    {"copy", (PyCFunction)pg_polygon_copy, METH_NOARGS, NULL},
    {"insert_vertex", (PyCFunction)pg_polygon_insert_vertex, METH_FASTCALL,
     NULL},
    {"remove_vertex", (PyCFunction)pg_polygon_remove_vertex, METH_O, NULL},
    {"pop_vertex", (PyCFunction)pg_polygon_pop_vertex, METH_O, NULL},
    {"scale", (PyCFunction)pg_polygon_scale, METH_O, NULL},
    {"scale_ip", (PyCFunction)pg_polygon_scale_ip, METH_O, NULL},
    {"flip", (PyCFunction)pg_polygon_flip, METH_FASTCALL, NULL},
    {"flip_ip", (PyCFunction)pg_polygon_flip_ip, METH_FASTCALL, NULL},
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
pg_polygon_set_vertices(pgPolygonObject *self, PyObject *value, void *closure)
{
    PyObject **new_vertices = NULL;
    Py_ssize_t i, len;

    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);

    pgPolygonBase *s_poly = &self->polygon;

    if (!PySequence_FAST_CHECK(value)) {
        PyErr_SetString(PyExc_TypeError, "vertices must be a sequence");
        return -1;
    }

    len = PySequence_Fast_GET_SIZE(value);

    if (len < 3) {
        PyErr_SetString(PyExc_ValueError,
                        "vertices must have at least 3 items");
        return -1;
    }

    new_vertices = PySequence_Fast_ITEMS(value);

    if (s_poly->verts_num != len) {
        PyMem_Resize(s_poly->vertices, double, len * 2);
        if (!s_poly->vertices) {
            PyErr_NoMemory();
            return -1;
        }
        s_poly->verts_num = len;
    }

    s_poly->centerx = 0.0;
    s_poly->centery = 0.0;

    for (i = 0; i < len; i++) {
        double x, y;
        if (!pg_TwoDoublesFromObj(new_vertices[i], &x, &y)) {
            PyErr_SetString(
                PyExc_TypeError,
                "Invalid coordinate, must be a sequence of 2 numbers");
            return -1;
        }
        s_poly->vertices[i * 2] = x;
        s_poly->vertices[i * 2 + 1] = y;
        s_poly->centerx += x;
        s_poly->centery += y;
    }

    s_poly->verts_num = len;

    s_poly->centerx /= len;
    s_poly->centery /= len;

    return 0;
}

static int
pg_polygon_ass_vertex(pgPolygonBase *poly, Py_ssize_t i, PyObject *v)
{
    double new_x, new_y;

    /* Adjust the index */
    if (i < 0) {
        i += poly->verts_num;
    }

    if (i < 0 || i > poly->verts_num) {
        PyErr_SetString(PyExc_IndexError, "Invalid vertex Index");
        return -1;
    }

    /* Extract the new vertex position */
    if (!pg_TwoDoublesFromObj(v, &new_x, &new_y)) {
        PyErr_SetString(PyExc_TypeError, "Must assign numeric values");
        return -1;
    }

    /* Update the center */
    poly->centerx += (new_x - poly->vertices[i * 2]) / poly->verts_num;
    poly->centery += (new_y - poly->vertices[i * 2 + 1]) / poly->verts_num;

    /* Update the vertex */
    poly->vertices[i * 2] = new_x;
    poly->vertices[i * 2 + 1] = new_y;

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
        Py_ssize_t i = PyNumber_AsSsize_t(op, NULL);
        if (PyErr_Occurred()) {
            return -1;
        }

        return pg_polygon_ass_vertex(&self->polygon, i, value);
    }
    /* If we want to support slicing add here */
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
    return PyFloat_FromDouble(self->polygon.centerx);
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
    _pg_move_polygon_helper(&(self->polygon), (val - self->polygon.centerx),
                            0.0);
    return 0;
}

static PyObject *
pg_polygon_get_center_y(pgPolygonObject *self, void *closure)
{
    return PyFloat_FromDouble(self->polygon.centery);
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
    _pg_move_polygon_helper(&(self->polygon), 0.0,
                            (val - self->polygon.centery));
    return 0;
}

static PyObject *
pg_polygon_get_center(pgPolygonObject *self, void *closure)
{
    return pg_TupleFromDoublePair(self->polygon.centerx,
                                  self->polygon.centery);
}

static PG_FORCEINLINE double
_pg_distance(double xa, double ya, double xb, double yb)
{
    double dx = xb - xa;
    double dy = yb - ya;
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

static PyObject *
pg_polygon_get_area(pgPolygonObject *self, void *closure)
{
    double area = 0;
    double *vertices = self->polygon.vertices;
    int vert_num = self->polygon.verts_num;
    Py_ssize_t i;
    for (i = 0; i < vert_num; i++) {
        area +=
            vertices[(i * 2)] * vertices[(((i + 1) * 2) + 1) % (vert_num * 2)];
        area -=
            vertices[((i + 1) * 2) % (vert_num * 2)] * vertices[(i * 2) + 1];
    }

    return PyFloat_FromDouble(ABS(area / 2));
}

static int
pg_polygon_set_center(pgPolygonObject *self, PyObject *value, void *closure)
{
    double new_centerx = 0, new_centery = 0;
    DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value);
    if (!pg_TwoDoublesFromObj(value, &new_centerx, &new_centery)) {
        PyErr_SetString(PyExc_TypeError, "Expected a sequence of 2 numbers");
        return -1;
    }
    _pg_move_polygon_helper(&(self->polygon),
                            (new_centerx - self->polygon.centerx),
                            (new_centery - self->polygon.centery));
    return 0;
}

static PyGetSetDef pg_polygon_getsets[] = {
    {"centerx", (getter)pg_polygon_get_center_x,
     (setter)pg_polygon_set_center_x, NULL, NULL},
    {"centery", (getter)pg_polygon_get_center_y,
     (setter)pg_polygon_set_center_y, NULL, NULL},
    {"center", (getter)pg_polygon_get_center, (setter)pg_polygon_set_center,
     NULL, NULL},
    {"verts_num", (getter)pg_polygon_get_verts_num, NULL,
     "Number of vertices of the polygon", NULL},
    {"vertices", (getter)pg_polygon_get_vertices,
     (setter)pg_polygon_set_vertices, "Vertices of the polygon", NULL},
    {"perimeter", (getter)pg_polygon_get_perimeter, NULL,
     "Perimeter of the polygon", NULL},
    {"area", (getter)pg_polygon_get_area, NULL, "area of the polygon", NULL},
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
