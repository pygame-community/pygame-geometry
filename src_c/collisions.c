#include "include/collisions.h"
#include <stdio.h>

#ifndef ABS
#define ABS(x) ((x) < 0 ? -(x) : (x))
#endif /* ~ABS */

static int
pgCollision_LineLine(pgLineBase *A, pgLineBase *B)
{
    double x1_m_x2 = A->x1 - A->x2;
    double y3_m_y4 = B->y1 - B->y2;
    double y1_m_y2 = A->y1 - A->y2;
    double x3_m_x4 = B->x1 - B->x2;

    double den = x1_m_x2 * y3_m_y4 - y1_m_y2 * x3_m_x4;

    if (!den)
        return 0;

    double x1_m_x3 = A->x1 - B->x1;
    double y1_m_y3 = A->y1 - B->y1;

    double t1 = x1_m_x3 * y3_m_y4 - y1_m_y3 * x3_m_x4;
    double t = t1 / den;

    double u1 = x1_m_x2 * y1_m_y3 - y1_m_y2 * x1_m_x3;
    double u = -(u1 / den);

    return t >= 0 && t <= 1 && u >= 0 && u <= 1;
}

static int
pgIntersection_LineLine(pgLineBase *A, pgLineBase *B, double *X, double *Y)
{
    double x1 = A->x1;
    double y1 = A->y1;
    double x2 = A->x2;
    double y2 = A->y2;
    double x3 = B->x1;
    double y3 = B->y1;
    double x4 = B->x2;
    double y4 = B->y2;

    double x1_m_x2 = x1 - x2;
    double y3_m_y4 = y3 - y4;
    double y1_m_y2 = y1 - y2;
    double x3_m_x4 = x3 - x4;

    double den = x1_m_x2 * y3_m_y4 - y1_m_y2 * x3_m_x4;

    if (!den)
        return 0;

    double x1_m_x3 = x1 - x3;
    double y1_m_y3 = y1 - y3;

    double t1 = x1_m_x3 * y3_m_y4 - y1_m_y3 * x3_m_x4;
    double t = t1 / den;

    double u1 = x1_m_x2 * y1_m_y3 - y1_m_y2 * x1_m_x3;
    double u = -(u1 / den);

    if (t >= 0 && t <= 1 && u >= 0 && u <= 1) {
        if (X)
            *X = x1 + t * (x2 - x1);
        if (Y)
            *Y = y1 + t * (y2 - y1);
        return 1;
    }
    return 0;
}

static int
pgCollision_LinePoint(pgLineBase *line, double Cx, double Cy)
{
    double Ax = line->x1;
    double Ay = line->y1;
    double Bx = line->x2;
    double By = line->y2;

    /* https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection */
    return (Bx - Ax) * (Cy - Ay) == (Cx - Ax) * (By - Ay) &&
           ((Ax != Bx) ? (Ax <= Cx && Cx <= Bx) || (Bx <= Cx && Cx <= Ax)
                       : (Ay <= Cy && Cy <= By) || (By <= Cy && Cy <= Ay));
}

static int
pgCollision_CirclePoint(pgCircleBase *circle, double Cx, double Cy)
{
    double dx = circle->x - Cx;
    double dy = circle->y - Cy;
    return dx * dx + dy * dy <= circle->r * circle->r;
}

static int
pgCollision_LineCircle(pgLineBase *line, pgCircleBase *circle)
{
    double x1 = line->x1;
    double y1 = line->y1;
    double x2 = line->x2;
    double y2 = line->y2;
    double cx = circle->x;
    double cy = circle->y;
    double r = circle->r;

    if (pgCollision_CirclePoint(circle, x1, y1) ||
        pgCollision_CirclePoint(circle, x2, y2))
        return 1;

    double dx = x1 - x2;
    double dy = y1 - y2;
    double len = sqrt((dx * dx) + (dy * dy));

    double dot =
        (((cx - x1) * (x2 - x1)) + ((cy - y1) * (y2 - y1))) / (len * len);

    double closest_x = x1 + (dot * (x2 - x1));
    double closest_y = y1 + (dot * (y2 - y1));

    pgLineBase line2 = {x1, y1, x2, y2};
    if (!pgCollision_LinePoint(&line2, closest_x, closest_y))
        return 0;

    dx = closest_x - cx;
    dy = closest_y - cy;
    double distance = sqrt((dx * dx) + (dy * dy));

    return distance <= r;
}

static int
pgCollision_CircleCircle(pgCircleBase *A, pgCircleBase *B)
{
    return 0;
}

static int
pgCollision_RectLine(SDL_FRect *rect, pgLineBase *line)
{
    return 0;
}

static int
pgCollision_RectCircle(SDL_FRect *rect, pgCircleBase *circle)
{
    return 0;
}
