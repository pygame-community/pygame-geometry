#ifndef _CIRCLE_H
#define _CIRCLE_H

#include "pygame.h"

typedef struct pgCircleBase {
    double x, y, r, r_sqr;
} pgCircleBase;

typedef struct pgCircleObject {
    PyObject_HEAD pgCircleBase circle;
    PyObject *weakreflist;
} pgCircleObject;

#define pgCircle_CAST(o) ((pgCircleObject *)(o))
#define pgCircle_CIRCLE(o) (pgCircle_CAST(o)->circle)

#endif /* ~_CIRCLE_H */
