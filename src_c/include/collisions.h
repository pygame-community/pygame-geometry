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
pgCollision_PolyPoly(pgPolygonBase *polygon_1, pgPolygonBase *polygon_2);
static int
pgCollision_PolyLine(pgPolygonBase *polygon, pgLineBase *line);
static int
pgCollision_PolyRect(pgPolygonBase *poly, SDL_Rect *rect);
static int
pgCollision_PolyCircle(pgPolygonBase *poly, pgCircleBase *circle);
static int

pgIntersection_PolyPoly(pgPolygonBase *polygon_1, pgPolygonBase *polygon_2);
static int
pgIntersection_PolyLine(pgPolygonBase *polygon, pgLineBase *line);
static int
pgIntersection_PolyRect(pgPolygonBase *polygon, SDL_Rect *rect);
static int
pgIntersection_PolyCircle(pgPolygonBase *polygon, pgCircleBase *circle);
#endif /* ~_PG_COLLISIONS_H */
