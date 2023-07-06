// pgCollision_* tells you if two objects are colliding.
// pgIntersection_* tells you if two objects are colliding and if where.
// pgIntersection_*'s three final parameters are pointers to X, optional, Y,
// optional, T, optional.

#ifndef _PG_COLLISIONS_H
#define _PG_COLLISIONS_H

#include "pygame.h"
#include "geometry.h"

static int
pgCollision_LineLine(pgLineBase *, pgLineBase *);
static int
pgIntersection_LineLine(pgLineBase *, pgLineBase *, double *, double *,
                        double *);
static int
pgCollision_LinePoint(pgLineBase *, double, double);
static int
pgCollision_CirclePoint(pgCircleBase *circle, double, double);
static int
pgCollision_LineCircle(pgLineBase *, pgCircleBase *);
static int
pgIntersection_LineCircle(pgLineBase *, pgCircleBase *, double *, double *,
                          double *);
static int
pgCollision_CircleCircle(pgCircleBase *, pgCircleBase *);
static int
pgIntersection_LineRect(pgLineBase *, SDL_Rect *, double *, double *,
                        double *);
static int
pgCollision_RectLine(SDL_Rect *, pgLineBase *);
static int
pgCollision_RectCircle(SDL_Rect *, pgCircleBase *);

static int
pgRaycast_LineLine(pgLineBase *, pgLineBase *, double, double *);
static int
pgRaycast_LineRect(pgLineBase *, SDL_Rect *, double, double *);
static int
pgRaycast_LineCircle(pgLineBase *, pgCircleBase *, double, double *);

static int
pgCollision_PolygonPoint(pgPolygonBase *, double, double);

static int
pgCollision_PolygonLine(pgPolygonBase *, pgLineBase *, int);
static int
pgCollision_CirclePolygon(pgCircleBase *, pgPolygonBase *, int);


#endif /* ~_PG_COLLISIONS_H */
