#include "line.c"
#include "circle.c"
#include "polygon.c"
#include "collisions.c"
#ifdef __AVX2__
#include "simd_collisions_avx2.c"
#endif /* ~__AVX2__ */

#define PYGAMEAPI_GEOMETRY_NUMSLOTS 18

/*
 * origin, direction, max_dist
 * origin, angle, max_dist
 * origin, end
 * line
 *
 * sets the error messages
 * 1 if success
 * o if it fails
 */
static int
_pg_extract_ray_from_object_fastcall(PyObject *const *args, Py_ssize_t nargs,
                                     pgLineBase *line, double *max_t)
{
    if (nargs == 1) {
        if (!pgLine_FromObject(args[0], line)) {
            PyErr_SetString(
                PyExc_TypeError,
                "line parameter must be a Line or a LineLike object");
            return 0;
        }

        *max_t = 1.0;

        return 1;
    }
    else if (nargs == 2) {
        if (!pg_TwoDoublesFromObj(args[0], &line->xa, &line->ya)) {
            PyErr_SetString(
                PyExc_TypeError,
                "Invalid ray origin value, must be a pair of numeric values");
            return 0;
        }
        if (!pg_TwoDoublesFromObj(args[1], &line->xb, &line->yb)) {
            PyErr_SetString(
                PyExc_TypeError,
                "Invalid ray end value, must be a pair of numeric values");
            return 0;
        }

        *max_t = 1.0;

        return 1;
    }
    else if (nargs == 3) {
        if (!pg_TwoDoublesFromObj(args[0], &line->xa, &line->ya)) {
            PyErr_SetString(
                PyExc_TypeError,
                "Invalid ray origin value, must be a pair of numeric values");
            return 0;
        }

        if (PyNumber_Check(args[1])) {
            double angle;
            if (!pg_DoubleFromObj(args[1], &angle)) {
                PyErr_SetString(PyExc_TypeError,
                                "Invalid ray angle value, must be numeric");
                return 0;
            }
            angle = DEG_TO_RAD(angle);
            line->xb = line->xa - cos(angle);
            line->yb = line->ya - sin(angle);
        }
        else if (!pg_TwoDoublesFromObj(args[1], &line->xb, &line->yb)) {
            PyErr_SetString(PyExc_TypeError,
                            "expected a pair of floats or a single float");
            return 0;
        }

        double max_dist;
        if (!pg_DoubleFromObj(args[2], &max_dist)) {
            PyErr_SetString(
                PyExc_ValueError,
                "Invalid ray max distance threshold value, must be numeric");
            return 0;
        }
        if (max_dist < 0 || max_dist == DBL_MAX) {
            *max_t = DBL_MAX;
            return 1;
        }
        else if (max_dist == 0) {
            PyErr_SetString(
                PyExc_ValueError,
                "Invalid max distance value, must be nonzero numeric value");
            return 0;
        }
        line->xb = (line->xb - line->xa) * max_dist + line->xa;
        line->yb = (line->yb - line->ya) * max_dist + line->ya;

        *max_t = max_dist / pgLine_Length(line);

        return 1;
    }
    else {
        PyErr_SetString(PyExc_TypeError, "Invalid number of arguments");
        return 0;
    }
}

static PyObject *
pg_raycast(PyObject *_null, PyObject *const *args, Py_ssize_t nargs)
{
    PyObject **colliders;
    Py_ssize_t colliders_length;
    Py_ssize_t loop;
    double max_t;
    double x, y;
    pgLineBase line;

    if (nargs != 2 && nargs != 4) {
        return RAISE(PyExc_TypeError, "Invalid number of arguments");
    }

    if (!_pg_extract_ray_from_object_fastcall(args, nargs - 1, &line,
                                              &max_t)) {
        return NULL;
    }

    if (!PySequence_FAST_CHECK(args[nargs - 1])) {
        return RAISE(PyExc_TypeError,
                     "colliders parameter must be a sequence");
    }
    colliders = PySequence_Fast_ITEMS(args[nargs - 1]);
    colliders_length = PySequence_Fast_GET_SIZE(args[nargs - 1]);

    // find the best t
    double record_t = max_t;
    double temp_t = 0;

    for (loop = 0; loop < colliders_length; loop++) {
        PyObject *obj = colliders[loop];

        if (pgCircle_Check(obj)) {
            if (pgRaycast_LineCircle(&line, &pgCircle_AsCircle(obj), max_t,
                                     &temp_t)) {
                record_t = MIN(record_t, temp_t);
            }
        }
        else if (pgLine_Check(obj)) {
            if (pgRaycast_LineLine(&line, &pgLine_AsLine(obj), max_t,
                                   &temp_t)) {
                record_t = MIN(record_t, temp_t);
            }
        }
        else if (pgRect_Check(obj)) {
            if (pgRaycast_LineRect(&line, &pgRect_AsRect(obj), max_t,
                                   &temp_t)) {
                record_t = MIN(record_t, temp_t);
            }
        }
        else {
            return RAISE(PyExc_TypeError,
                         "collisions must be a sequence of "
                         "Line, Circle or Rect objects");
        }
    }

    if (record_t == max_t) {
        Py_RETURN_NONE;
    }

    pgLine_At(&line, record_t, &x, &y);

    return pg_TupleFromDoublePair(x, y);
}

static PyObject *
geometry_regular_polygon(PyObject *_null, PyObject *const *args,
                         Py_ssize_t nargs)
{
    Py_ssize_t sides;
    double radius;
    double angle = 0;
    double Cx, Cy;

    if (nargs < 3 || nargs > 4) {
        return RAISE(PyExc_TypeError,
                     "invalid number of arguments, expected 3 or 4 arguments");
    }
    sides = PyLong_AsSsize_t(args[0]);
    if (PyErr_Occurred()) {
        return NULL;
    }

    if (sides < 3) {
        if (sides < 0) {
            return RAISE(PyExc_ValueError,
                         "the sides can not be a negative number");
        }
        return RAISE(PyExc_ValueError, "polygons need at least 3 sides");
    }

    if (!pg_TwoDoublesFromObj(args[1], &Cx, &Cy)) {
        return RAISE(PyExc_TypeError,
                     "the second parameter must be a sequence of 2 numbers");
    }

    if (!pg_DoubleFromObj(args[2], &radius)) {
        return RAISE(PyExc_TypeError, "the third parameter must be a number");
    }
    if (nargs == 4) {
        if (!pg_DoubleFromObj(args[3], &angle)) {
            return RAISE(PyExc_TypeError,
                         "the forth parameter must be a number");
        }
        angle = DEG_TO_RAD(angle);
    }

    double *vertices = PyMem_New(double, sides * 2);
    if (!vertices) {
        return RAISE(PyExc_MemoryError,
                     "cannot allocate memory for the polygon vertices");
    }

    Py_ssize_t loop;
    double fac = M_TWOPI / sides;

    /*If the number of sides is even, mirror the vertices*/
    if (sides % 2 == 0) {
        for (loop = 0; loop < sides / 2; loop++) {
            double ang = angle + fac * loop;
            double radi_cos_a = radius * cos(ang);
            double radi_sin_a = radius * sin(ang);

            vertices[loop * 2] = Cx + radi_cos_a;
            vertices[loop * 2 + 1] = Cy + radi_sin_a;

            vertices[sides + loop * 2] = Cx - radi_cos_a;
            vertices[sides + loop * 2 + 1] = Cy - radi_sin_a;
        }
    }
    else {
        for (loop = 0; loop < sides; loop++) {
            double ang = angle + fac * loop;
            vertices[loop * 2] = Cx + radius * cos(ang);
            vertices[loop * 2 + 1] = Cy + radius * sin(ang);
        }
    }

    pgPolygonObject *ret =
        (pgPolygonObject *)pgPolygon_Type.tp_new(&pgPolygon_Type, NULL, NULL);

    if (!ret) {
        PyMem_Free(vertices);
        return NULL;
    }

    ret->polygon.vertices = vertices;
    ret->polygon.verts_num = sides;
    ret->polygon.centerx = Cx;
    ret->polygon.centery = Cy;

    return (PyObject *)ret;
}

static PyObject *
geometry_multiraycast(PyObject *_null, PyObject *const *args, Py_ssize_t nargs)
{
    PyObject **colliders, **rays, *list;
    Py_ssize_t colliders_length, rays_length, i, j;

    if (nargs != 2) {
        return RAISE(PyExc_TypeError,
                     "Invalid number of arguments, expected "
                     "exactly 2 arguments");
    }

    if (!PySequence_FAST_CHECK(args[0])) {
        return RAISE(PyExc_TypeError,
                     "Invalid rays parameter, expected a sequence");
    }

    rays_length = PySequence_Fast_GET_SIZE(args[0]);

    /*If there are no rays, return an empty list*/
    if (!rays_length) {
        return PyList_New(0);
    }

    if (!PySequence_FAST_CHECK(args[1])) {
        return RAISE(PyExc_TypeError,
                     "Invalid colliders parameter, expected a sequence");
    }

    colliders_length = PySequence_Fast_GET_SIZE(args[1]);

    /*If there are no colliders, return a list of None objects,
     * with the same length as the rays*/
    if (!colliders_length) {
        list = PyList_New(rays_length);
        if (!list) {
            return NULL;
        }
        for (i = 0; i < rays_length; i++) {
            Py_INCREF(Py_None);
            PyList_SET_ITEM(list, i, Py_None);
        }

        return list;
    }

    rays = PySequence_Fast_ITEMS(args[0]);
    colliders = PySequence_Fast_ITEMS(args[1]);

    /*Create a list to store the results*/
    list = PyList_New(rays_length);
    if (!list) {
        return NULL;
    }

    pgLineBase ray;
    for (i = 0; i < rays_length; i++) {
        PyObject *ray_obj = rays[i];
        double max_t = 0;

        /*Convert the PyObject into a ray*/
        if (pgLine_Check(ray_obj)) {
            ray = pgLine_AsLine(ray_obj);
            max_t = 1.0;
        }
        else if (PyTuple_Check(ray_obj)) {
            PyObject *const *ray_items =
                (PyObject *const *)PySequence_Fast_ITEMS(ray_obj);

            if (!_pg_extract_ray_from_object_fastcall(
                    ray_items, PyTuple_GET_SIZE(ray_obj), &ray, &max_t)) {
                Py_DECREF(list);
                return NULL;
            }
        }
        else {
            Py_DECREF(list);
            return RAISE(PyExc_TypeError,
                         "rays must be a sequence of lines or tuples");
        }

        double record_t = max_t;
        double temp_t = 0;
        for (j = 0; j < colliders_length; j++) {
            PyObject *obj = colliders[j];

            if (pgCircle_Check(obj)) {
                if (pgRaycast_LineCircle(&ray, &pgCircle_AsCircle(obj), max_t,
                                         &temp_t)) {
                    record_t = MIN(record_t, temp_t);
                }
            }
            else if (pgLine_Check(obj)) {
                if (pgRaycast_LineLine(&ray, &pgLine_AsLine(obj), max_t,
                                       &temp_t)) {
                    record_t = MIN(record_t, temp_t);
                }
            }
            else if (pgRect_Check(obj)) {
                if (pgRaycast_LineRect(&ray, &pgRect_AsRect(obj), max_t,
                                       &temp_t)) {
                    record_t = MIN(record_t, temp_t);
                }
            }
            else {
                Py_DECREF(list);
                return RAISE(PyExc_TypeError,
                             "collisions must be a sequence of "
                             "Line, Circle or Rect objects");
            }
        }

        if (record_t == max_t) {
            Py_INCREF(Py_None);
            PyList_SET_ITEM(list, i, Py_None);
        }
        else {
            double x, y;
            pgLine_At(&ray, record_t, &x, &y);
            PyObject *point = pg_TupleFromDoublePair(x, y);
            if (!point) {
                Py_DECREF(list);
                return NULL;
            }
            PyList_SET_ITEM(list, i, point);
        }
    }

    return list;
}

static PG_FORCE_INLINE void
_normalize_rect(SDL_Rect *rect)
{
    if (rect->w < 0) {
        rect->x += rect->w;
        rect->w = -rect->w;
    }
    if (rect->h < 0) {
        rect->y += rect->h;
        rect->h = -rect->h;
    }
}

static PyObject *
geometry_rect_to_polygon(PyObject *_null, PyObject *arg)
{
    SDL_Rect rect, *tmp;

    if (!(tmp = pgRect_FromObject(arg, &rect))) {
        if (PyErr_Occurred()) {
            return NULL;
        }
        return RAISE(PyExc_TypeError, "rect must be a valid Rect object");
    }

    _normalize_rect(tmp);

    double vertices[] = {tmp->x, tmp->y,          tmp->x + tmp->w,
                         tmp->y, tmp->x + tmp->w, tmp->y + tmp->h,
                         tmp->x, tmp->y + tmp->h};

    return pgPolygon_New4(vertices, 4, tmp->x + tmp->w / 2,
                          tmp->y + tmp->h / 2);
}

static PyObject *
geometry_is_line(PyObject *_null, PyObject *arg)
{
    if (pgLine_Check(arg)) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyObject *
geometry_is_circle(PyObject *_null, PyObject *arg)
{
    if (pgCircle_Check(arg)) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyObject *
geometry_is_polygon(PyObject *_null, PyObject *arg)
{
    if (pgPolygon_Check(arg)) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyMethodDef _pg_module_methods[] = {
    {"regular_polygon", (PyCFunction)geometry_regular_polygon, METH_FASTCALL,
     NULL},
    {"multiraycast", (PyCFunction)geometry_multiraycast, METH_FASTCALL, NULL},
    {"raycast", (PyCFunction)pg_raycast, METH_FASTCALL, NULL},
    {"rect_to_polygon", (PyCFunction)geometry_rect_to_polygon, METH_O, NULL},
    {"is_line", (PyCFunction)geometry_is_line, METH_O, NULL},
    {"is_circle", (PyCFunction)geometry_is_circle, METH_O, NULL},
    {"is_polygon", (PyCFunction)geometry_is_polygon, METH_O, NULL},
    {NULL, NULL, 0, NULL}};

MODINIT_DEFINE(geometry)
{
    PyObject *module, *apiobj;
    static void *c_api[PYGAMEAPI_GEOMETRY_NUMSLOTS];

    static struct PyModuleDef _module = {
        PyModuleDef_HEAD_INIT,
        "geometry",
        "Module for shapes like Line, Circle, "
        "Polygon and extra functionalities\n",
        -1,
        _pg_module_methods,
        NULL,
        NULL,
        NULL,
        NULL};

    import_pygame_base();
    import_pygame_rect();

    if (PyErr_Occurred()) {
        return NULL;
    }

    /* Create the module and add the functions */
    if (PyType_Ready(&pgLine_Type) < 0) {
        return NULL;
    }
    if (PyType_Ready(&pgCircle_Type) < 0) {
        return NULL;
    }
    if (PyType_Ready(&pgPolygon_Type) < 0) {
        return NULL;
    }

    module = PyModule_Create(&_module);
    if (module == NULL) {
        return NULL;
    }

    Py_INCREF(&pgLine_Type);
    if (PyModule_AddObject(module, "LineType", (PyObject *)&pgLine_Type)) {
        Py_DECREF(&pgLine_Type);
        Py_DECREF(module);
        return NULL;
    }
    Py_INCREF(&pgLine_Type);
    if (PyModule_AddObject(module, "Line", (PyObject *)&pgLine_Type)) {
        Py_DECREF(&pgLine_Type);
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&pgCircle_Type);
    if (PyModule_AddObject(module, "CircleType", (PyObject *)&pgCircle_Type)) {
        Py_DECREF(&pgCircle_Type);
        Py_DECREF(module);
        return NULL;
    }
    Py_INCREF(&pgCircle_Type);
    if (PyModule_AddObject(module, "Circle", (PyObject *)&pgCircle_Type)) {
        Py_DECREF(&pgCircle_Type);
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&pgPolygon_Type);
    if (PyModule_AddObject(module, "PolygonType",
                           (PyObject *)&pgPolygon_Type)) {
        Py_DECREF(&pgPolygon_Type);
        Py_DECREF(module);
        return NULL;
    }
    Py_INCREF(&pgPolygon_Type);
    if (PyModule_AddObject(module, "Polygon", (PyObject *)&pgPolygon_Type)) {
        Py_DECREF(&pgPolygon_Type);
        Py_DECREF(module);
        return NULL;
    }

    /* export the c api */
    c_api[0] = &pgLine_Type;
    c_api[1] = pgLine_New;
    c_api[2] = pgLine_New4;
    c_api[3] = pgLine_FromObject;
    c_api[4] = pgLine_FromObjectFastcall;
    c_api[5] = pgLine_Length;
    c_api[6] = pgLine_LengthSquared;
    c_api[7] = pgLine_At;
    c_api[8] = &pgCircle_Type;
    c_api[9] = pgCircle_New;
    c_api[10] = pgCircle_New3;
    c_api[11] = pgCircle_FromObject;
    c_api[12] = &pgPolygon_Type;
    c_api[13] = pgPolygon_New;
    c_api[14] = pgPolygon_New2;
    c_api[15] = pgPolygon_New4;
    c_api[16] = pgPolygon_FromObject;
    c_api[17] = pgPolygon_FromObjectFastcall;

    apiobj = encapsulate_api(c_api, "geometry");
    if (PyModule_AddObject(module, PYGAMEAPI_LOCAL_ENTRY, apiobj)) {
        Py_XDECREF(apiobj);
        Py_DECREF(module);
        return NULL;
    }
    return module;
}
 