/*
  pygame - Python Game Library
  Copyright (C) 2000-2001  Pete Shinners
  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Library General Public
  License as published by the Free Software Foundation; either
  version 2 of the License, or (at your option) any later version.
  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Library General Public License for more details.
  You should have received a copy of the GNU Library General Public
  License along with this library; if not, write to the Free
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
  Pete Shinners
  pete@shinners.org
*/

/*
 i dont not claim this as my own code, just copied it from the pygame source
*/

#ifndef _PYGAME_H
#define _PYGAME_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifndef SDL_VERSION_ATLEAST
#ifdef _MSC_VER
typedef unsigned __int8 uint8_t;
typedef unsigned __int32 uint32_t;
#else
#include <stdint.h>
#endif
typedef uint32_t Uint32;
typedef uint8_t Uint8;
#endif /* no SDL */

/* Ensure PyPy-specific code is not in use when running on GraalPython (PR
 * #2580) */
#if defined(GRAALVM_PYTHON) && defined(PYPY_VERSION)
#undef PYPY_VERSION
#endif

#define RAISE(x, y) (PyErr_SetString((x), (y)), NULL)
#define DEL_ATTR_NOT_SUPPORTED_CHECK(name, value)                            \
    do {                                                                     \
        if (!value) {                                                        \
            PyErr_Format(PyExc_AttributeError, "Cannot delete attribute %s", \
                         name);                                              \
            return -1;                                                       \
        }                                                                    \
    } while (0)

#define DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value)                           \
    do {                                                                      \
        if (!value) {                                                         \
            PyErr_SetString(PyExc_AttributeError, "Cannot delete attribute"); \
            return -1;                                                        \
        }                                                                     \
    } while (0)

/* thread check */
#ifdef WITH_THREAD
#define PG_CHECK_THREADS() (1)
#else /* ~WITH_THREAD */
#define PG_CHECK_THREADS() \
    (RAISE(PyExc_NotImplementedError, "Python built without thread support"))
#endif /* ~WITH_THREAD */

#define PyType_Init(x) (((x).ob_type) = &PyType_Type)

/* version macros (defined since version 1.9.5) */
#define PG_MAJOR_VERSION 2
#define PG_MINOR_VERSION 1
#define PG_PATCH_VERSION 3
#define PG_VERSIONNUM(MAJOR, MINOR, PATCH) \
    (1000 * (MAJOR) + 100 * (MINOR) + (PATCH))
#define PG_VERSION_ATLEAST(MAJOR, MINOR, PATCH)                             \
    (PG_VERSIONNUM(PG_MAJOR_VERSION, PG_MINOR_VERSION, PG_PATCH_VERSION) >= \
     PG_VERSIONNUM(MAJOR, MINOR, PATCH))

#ifndef MIN
#define MIN(a, b) ((a) < (b) ? (a) : (b))
#endif
#ifndef MAX
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#endif
#ifndef ABS
#define ABS(a) (((a) < 0) ? -(a) : (a))
#endif

#ifndef PG_INLINE
#if defined(__clang__)
#define PG_INLINE __inline__ __attribute__((__unused__))
#elif defined(__GNUC__)
#define PG_INLINE __inline__
#elif defined(_MSC_VER)
#define PG_INLINE __inline
#elif defined(__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
#define PG_INLINE inline
#else
#define PG_INLINE
#endif
#endif /* ~PG_INLINE */

// Worth trying this on MSVC/win32 builds to see if provides any speed up
#ifndef PG_FORCEINLINE
#if defined(__clang__)
#define PG_FORCEINLINE __inline__ __attribute__((__unused__))
#elif defined(__GNUC__)
#define PG_FORCEINLINE __inline__
#elif defined(_MSC_VER)
#define PG_FORCEINLINE __forceinline
#elif defined(__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
#define PG_FORCEINLINE inline
#else
#define PG_FORCEINLINE
#endif
#endif /* ~PG_FORCEINLINE */
#define PG_FORCE_INLINE PG_FORCEINLINE

#define MODINIT_DEFINE(mod_name) PyMODINIT_FUNC PyInit_##mod_name(void)

#define RELATIVE_MODULE(m) ("." m)

#define MODPREFIX ""
#define IMPPREFIX "pygame."

#ifdef __SYMBIAN32__
#undef MODPREFIX
#undef IMPPREFIX
#define MODPREFIX "pygame_"
#define IMPPREFIX "pygame_"

#endif /* ~__SYMBIAN32__ */

#define PYGAMEAPI_LOCAL_ENTRY "_PYGAME_C_API"
#define PG_CAPSULE_NAME(m) (IMPPREFIX m "." PYGAMEAPI_LOCAL_ENTRY)
#define encapsulate_api(ptr, module) \
    PyCapsule_New(ptr, PG_CAPSULE_NAME(module), NULL)

// this is not meant to be used in prod
// so we can directly include the base source
#define import_pygame_base()

#ifndef SDL_VERSION_ATLEAST
typedef struct {
    float x, y, w, h;
} SDL_FRect;
typedef struct {
    int x, y, w, h;
} SDL_Rect;
#endif /* ~SDL_VERSION_ATLEAST */

#include "base.h"

#ifndef PySequence_FAST_CHECK
#define PySequence_FAST_CHECK(o) (PyList_Check(o) || PyTuple_Check(o))
#endif /* ~PySequence_FAST_CHECK */

#define _LOAD_SLOTS_FROM_PYGAME(module)                                       \
    {                                                                         \
        PyObject *_mod_##module = PyImport_ImportModule(IMPPREFIX #module);   \
                                                                              \
        if (_mod_##module != NULL) {                                          \
            PyObject *_c_api =                                                \
                PyObject_GetAttrString(_mod_##module, PYGAMEAPI_LOCAL_ENTRY); \
                                                                              \
            Py_DECREF(_mod_##module);                                         \
            if (_c_api != NULL && PyCapsule_CheckExact(_c_api)) {             \
                void **localptr = (void **)PyCapsule_GetPointer(              \
                    _c_api, PG_CAPSULE_NAME(#module));                        \
                _PGSLOTS_##module = localptr;                                 \
            }                                                                 \
            Py_XDECREF(_c_api);                                               \
        }                                                                     \
    }

#define PYGAMEAPI_GET_SLOT(module, index) _PGSLOTS_##module[(index)]

typedef struct {
    PyObject_HEAD SDL_Rect r;
    PyObject *weakreflist;
} pgRectObject;

void **_PGSLOTS_rect;

#define pgRect_AsRect(x) (((pgRectObject *)x)->r)
#define pgRect_Type (*(PyTypeObject *)PYGAMEAPI_GET_SLOT(rect, 0))

#define pgRect_Check(x) ((x)->ob_type == &pgRect_Type)
#define pgRect_New (*(PyObject * (*)(SDL_Rect *)) PYGAMEAPI_GET_SLOT(rect, 1))

#define pgRect_New4 \
    (*(PyObject * (*)(int, int, int, int)) PYGAMEAPI_GET_SLOT(rect, 2))

#define pgRect_FromObject \
    (*(SDL_Rect * (*)(PyObject *, SDL_Rect *)) PYGAMEAPI_GET_SLOT(rect, 3))

#define pgRect_Normalize (*(void (*)(SDL_Rect *))PYGAMEAPI_GET_SLOT(rect, 4))

#define import_pygame_rect() _LOAD_SLOTS_FROM_PYGAME(rect)

#endif /* ~_PYGAME_H */
