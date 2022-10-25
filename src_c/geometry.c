#include "line.c"
#include "circle.c"
#include "polygon.c"
#include "collisions.c"
#ifdef __AVX2__
#include "simd_collisions_avx2.c"
#endif /* ~__AVX2__ */

#define PYGAMEAPI_GEOMETRY_NUMSLOTS 21

static PyObject *
pg_raycast(PyObject *_null, PyObject *const *args, Py_ssize_t nargs)
{
    double start_x, start_y;
    double end_x, end_y;
    PyObject **farr;
    Py_ssize_t col_length;
    Py_ssize_t loop;
    double angle;
    double max_dist;

    if (nargs == 3) {
        if (!PySequence_FAST_CHECK(args[2])) {
            return RAISE(PyExc_TypeError, "argument of raycast() must be a sequence");
        }
        
        if (!pg_TwoDoublesFromObj(args[0], &start_x, &start_y)) {
            return RAISE(PyExc_TypeError, "the starting position requires a pair of floats");
        }
        if (!pg_TwoDoublesFromObj(args[1], &end_x, &end_y)) {
            return RAISE(PyExc_TypeError, "the end position requires a pair of floats");
        }
        farr = PySequence_Fast_ITEMS(args[2]);
        col_length = PySequence_Fast_GET_SIZE(args[2]);
    }
    else if (nargs == 4) {
        if (!PySequence_FAST_CHECK(args[3])) {
            return RAISE(PyExc_TypeError, "argument of raycast() must be a sequence");
        }

        if (!pg_TwoDoublesFromObj(args[0], &start_x, &start_y)) {
            return RAISE(PyExc_TypeError, "the starting position requires a pair of floats");
        }
        if (!pg_DoubleFromObj(args[1], &angle)) {
            return RAISE(PyExc_TypeError, "invalid angle");
        }
        if (!pg_DoubleFromObj(args[2], &max_dist)) {
            return RAISE(PyExc_TypeError, "invalid max distance");
        }
        end_x = start_x - cos(angle * PI / 180) * max_dist;
        end_y = start_y - sin(angle * PI / 180) * max_dist;

        if (!PySequence_FAST_CHECK(args[3])) {
            return RAISE(PyExc_TypeError, "an internal error has occured");
        }
        farr = PySequence_Fast_ITEMS(args[3]);
        col_length = PySequence_Fast_GET_SIZE(args[3]);
    }
    else {
        return RAISE(PyExc_TypeError,
                    "invalid number of arguments");
    }


    pgLineBase line;
    line.x1 = start_x;
    line.y1 = start_y;
    line.x2 = end_x;
    line.y2 = end_y;

    // find the best t
    double record = DBL_MAX;
    double temp_t = 0;

    for (loop = 0; loop < col_length; loop++) {
        if (pgCircle_Check(farr[loop])) {
            if (pgIntersection_LineCircle(&line,
                                          &pgCircle_AsCircle(farr[loop]), NULL,
                                          NULL, &temp_t)) {
                record = MIN(record, temp_t);
            }
        }
        else if (pgLine_Check(farr[loop])) {
            if (pgIntersection_LineLine(&line,
                                        &pgLine_AsLine(farr[loop]), NULL, NULL,
                                        &temp_t)) {
                record = MIN(record, temp_t);
            }
        }
        else if (pgRect_Check(farr[loop])) {
            if (pgIntersection_LineRect(&line,
                                        &pgRect_AsRect(farr[loop]), NULL, NULL,
                                        &temp_t)) {
                record = MIN(record, temp_t);
            }
        }
        else {
            return RAISE(PyExc_TypeError,
                         "collisions must be a sequence of "
                         "Line, Circle or Rect objects");
        }
    }

    if (record == DBL_MAX) {
        return pg_TupleFromDoublePair(
            line.x2,
            line.y2);
    }

    // construct the return with this formula: A+tB
    return pg_TupleFromDoublePair(
        line.x1 + record * (line.x2 - line.x1),
        line.y1 + record * (line.y2 - line.y1));
}



static PyObject *
geometry_regular_polygon(PyObject *_null, PyObject *const *args,
                         Py_ssize_t nargs)
{
    int sides;
    double radius;
    double angle = 0;
    double Cx, Cy;

    if (nargs < 3 || nargs > 4) {
        return RAISE(PyExc_TypeError,
                     "invalid number of arguments, expected 3 or 4 arguments");
    }
    sides = PyLong_AsLong(args[0]);
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
        angle *= PI / 180.0;
    }

    double *vertices = PyMem_New(double, sides * 2);
    if (!vertices) {
        return RAISE(PyExc_MemoryError,
                     "cannot allocate memory for the polygon vertices");
    }

    int loop;
    double fac = TAU / sides;
    for (loop = 0; loop < sides; loop++) {
        double ang = angle + fac * loop;
        vertices[loop * 2] = Cx + radius * cos(ang);
        vertices[loop * 2 + 1] = Cy + radius * sin(ang);
    }

    PyObject *ret = pgPolygon_New2(vertices, sides);
    PyMem_Free(vertices);

    return ret;
}


static PyMethodDef _pg_module_methods[] = {
    {"regular_polygon", (PyCFunction)geometry_regular_polygon, METH_FASTCALL,
     NULL},
    {"raycast", (PyCFunction)pg_raycast, METH_FASTCALL, NULL},
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
    c_api[0] = pgCollision_LineLine;
    c_api[1] = pgIntersection_LineLine;
    c_api[2] = pgCollision_LineCircle;
    c_api[3] = pgCollision_CircleCircle;
    c_api[4] = pgCollision_RectLine;
    c_api[5] = pgCollision_RectCircle;
    c_api[6] = &pgLine_Type;
    c_api[7] = pgLine_New;
    c_api[8] = pgLine_New4;
    c_api[9] = pgLine_FromObject;
    c_api[10] = pgLine_FromObjectFastcall;
    c_api[11] = pgLine_Length;
    c_api[12] = pgLine_LengthSquared;
    c_api[13] = &pgCircle_Type;
    c_api[14] = pgCircle_New;
    c_api[15] = pgCircle_New3;
    c_api[16] = pgCircle_FromObject;
    c_api[17] = &pgPolygon_Type;
    c_api[18] = pgPolygon_New;
    c_api[19] = pgPolygon_New2;
    c_api[20] = pgPolygon_FromObject;

    apiobj = encapsulate_api(c_api, "geometry");
    if (PyModule_AddObject(module, PYGAMEAPI_LOCAL_ENTRY, apiobj)) {
        Py_XDECREF(apiobj);
        Py_DECREF(module);
        return NULL;
    }
    return module;
}
                         