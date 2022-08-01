#ifndef _LINE_H
#define _LINE_H

#include "pygame.h"

typedef struct pgLineBase {
    double x1, y1;
    double x2, y2;
} pgLineBase;

typedef struct pgLineObject {
    PyObject_HEAD
    pgLineBase line;
    PyObject* weakreflist;
} pgLineObject;

#define pgLine_CAST(o) ((pgLineObject*)(o))

#define pgLine_GETLINE(o) (pgLine_CAST(o)->line)
#define pgLine_GETX1(self) (pgLine_CAST(self)->line.x1)
#define pgLine_GETY1(self) (pgLine_CAST(self)->line.y1)
#define pgLine_GETX2(self) (pgLine_CAST(self)->line.x2)
#define pgLine_GETY2(self) (pgLine_CAST(self)->line.y2)


#endif /* ~_LINE_H */
