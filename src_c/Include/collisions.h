// pgCollision_* tells you if two objects are colliding.
// pgIntersection_* tells you if two objects are colliding and if where.

#ifndef _PG_COLLISIONS_H
#define _PG_COLLISIONS_H

#include "pygame.h"
#include "base.h"

#include "line.h"
#include "circle.h"

typedef pgCircle pgCircleBase;

static int
pgCollision_LineLine(pgLineBase *, pgLineBase *);
static int
pgIntersection_LineLine(pgLineBase *, pgLineBase *, double *, double *);
static int
pgCollision_LineCircle(pgLineBase *, pgCircleBase *);
static int
pgCollision_CircleCircle(pgCircleBase *, pgCircleBase *);
static int
pgCollision_RectLine(SDL_FRect *, pgLineBase *);
static int
pgCollision_RectCircle(SDL_FRect *, pgCircleBase *);

#endif /* ~_PG_COLLISIONS_H */
