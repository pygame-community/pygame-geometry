// pgCollision_* tells you if two objects are colliding.
// pgIntersection_* tells you if two objects are colliding and if where.

#ifndef _PG_COLLISIONS_H
#define _PG_COLLISIONS_H

#include "pygame.h"

#include "geometry.h"

int
pgCollision_LineLine(pgLineBase *, pgLineBase *);
int
pgIntersection_LineLine(pgLineBase *, pgLineBase *, double *, double *);
int
pgCollision_LinePoint(pgLineBase *, double, double);
int
pgCollision_CirclePoint(pgCircleBase *circle, double, double);
int
pgCollision_LineCircle(pgLineBase *, pgCircleBase *);
int
pgCollision_CircleCircle(pgCircleBase *, pgCircleBase *);
int
pgCollision_RectLine(SDL_FRect *, pgLineBase *);
int
pgCollision_RectCircle(SDL_FRect *, pgCircleBase *);

#endif /* ~_PG_COLLISIONS_H */
