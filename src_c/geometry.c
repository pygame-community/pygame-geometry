#include "line.c"


#define PYGAMEAPI_GEOMETRY_NUMSLOTS 4


static PyMethodDef _pg_module_methods[] = {
    {NULL, NULL, 0, NULL}
};

MODINIT_DEFINE(geometry) {
    PyObject *module, *apiobj;
    static void *c_api[PYGAMEAPI_GEOMETRY_NUMSLOTS];

    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "geometry",
                                         "Module for the rectangle object\n",
                                         -1,
                                         _pg_module_methods,
                                         NULL,
                                         NULL,
                                         NULL,
                                         NULL};

    import_pygame_base();
    if (PyErr_Occurred()) {
        return NULL;
    }

    /* Create the module and add the functions */
    if (PyType_Ready(&pgLine_Type) < 0) {
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

    /* export the c api */
    c_api[0] = &pgLine_Type;
    c_api[1] = pgLine_New;
    c_api[2] = pgLine_New4;
    c_api[3] = pgLine_FromObject;
    apiobj = encapsulate_api(c_api, "geometry");
    if (PyModule_AddObject(module, PYGAMEAPI_LOCAL_ENTRY, apiobj)) {
        Py_XDECREF(apiobj);
        Py_DECREF(module);
        return NULL;
    }
    return module;
}
