#include "include/collisions.h"
#include <stdio.h>

#ifndef ABS
#define ABS(x) ((x) < 0 ? -(x) : (x))
#endif /* ~ABS */
#ifndef DOT2D
#define DOT2D(X0, Y0, X1, Y1) ((X0) * (X1) + (Y0) * (Y1))
#endif /* ~DOT2D */


static int
pgCollision_LineLine(pgLineBase *A, pgLineBase *B)
{
    float x1_m_x2 = A->x1 - A->x2;
    float y3_m_y4 = B->y1 - B->y2;
    float y1_m_y2 = A->y1 - A->y2;
    float x3_m_x4 = B->x1 - B->x2;

    float den = x1_m_x2 * y3_m_y4 - y1_m_y2 * x3_m_x4;

    if (!den)
        return 0;

    float x1_m_x3 = A->x1 - B->x1;
    float y1_m_y3 = A->y1 - B->y1;

    float t1 = x1_m_x3 * y3_m_y4 - y1_m_y3 * x3_m_x4;
    float t = t1 / den;

    float u1 = x1_m_x2 * y1_m_y3 - y1_m_y2 * x1_m_x3;
    float u = -(u1 / den);

    return t >= 0 && t <= 1 && u >= 0 && u <= 1;
}

static int
pgIntersection_LineLine(pgLineBase *A, pgLineBase *B, float *X, float *Y,
                        float *T)
{
    float x1 = A->x1;
    float y1 = A->y1;
    float x2 = A->x2;
    float y2 = A->y2;
    float x3 = B->x1;
    float y3 = B->y1;
    float x4 = B->x2;
    float y4 = B->y2;

    float x1_m_x2 = x1 - x2;
    float y3_m_y4 = y3 - y4;
    float y1_m_y2 = y1 - y2;
    float x3_m_x4 = x3 - x4;

    float den = x1_m_x2 * y3_m_y4 - y1_m_y2 * x3_m_x4;

    if (!den)
        return 0;

    float x1_m_x3 = x1 - x3;
    float y1_m_y3 = y1 - y3;

    float t1 = x1_m_x3 * y3_m_y4 - y1_m_y3 * x3_m_x4;
    float t = t1 / den;

    float u1 = x1_m_x2 * y1_m_y3 - y1_m_y2 * x1_m_x3;
    float u = -(u1 / den);

    if (t >= 0 && t <= 1 && u >= 0 && u <= 1) {
        if (X)
            *X = x1 + t * (x2 - x1);
        if (Y)
            *Y = y1 + t * (y2 - y1);
        if (T)
            *T = t;
        return 1;
    }
    return 0;
}

static int
pgCollision_LinePoint(pgLineBase *line, float Cx, float Cy)
{
    float Ax = line->x1;
    float Ay = line->y1;
    float Bx = line->x2;
    float By = line->y2;

    /* https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection */
    return (Bx - Ax) * (Cy - Ay) == (Cx - Ax) * (By - Ay) &&
           ((Ax != Bx) ? (Ax <= Cx && Cx <= Bx) || (Bx <= Cx && Cx <= Ax)
                       : (Ay <= Cy && Cy <= By) || (By <= Cy && Cy <= Ay));
}

static int
pgCollision_CirclePoint(pgCircleBase *circle, float Cx, float Cy)
{
    float dx = circle->x - Cx;
    float dy = circle->y - Cy;
    return dx * dx + dy * dy <= circle->r_sqr;
}

static int
pgIntersection_LineCircle(pgLineBase *line, pgCircleBase *circle, float *X,
                          float *Y, float *T)
{
    float x1 = line->x1;
    float y1 = line->y1;
    float x2 = line->x2;
    float y2 = line->y2;
    float xc = circle->x;
    float yc = circle->y;
    float r = circle->r;
    float rsq = circle->r_sqr;

    float dx = x2 - x1;
    float dy = y2 - y1;
    float A = dx * dx + dy * dy;
    float B = 2 * (dx * (x1 - xc) + dy * (y1 - yc));
    float C = (x1 - xc) * (x1 - xc) + (y1 - yc) * (y1 - yc) - rsq;
    float descriminant = B * B - 4 * A * C;
    if (descriminant < 0) {
        return 0;
    }
    float t = (-B - sqrt(descriminant)) / (2 * A);
    if (t < 0 || t > 1) {
        t = (-B + sqrt(descriminant)) / (2 * A);
        if (t < 0 || t > 1) {
            return 0;
        }
    }

    if (X)
        *X = x1 + t * dx;
    if (Y)
        *Y = y1 + t * dy;
    if (T)
        *T = t;
    return 1;
}

static int
pgCollision_LineCircle(pgLineBase *line, pgCircleBase *circle)
{
    float x1 = line->x1;
    float y1 = line->y1;
    float x2 = line->x2;
    float y2 = line->y2;
    float cx = circle->x;
    float cy = circle->y;
    float r = circle->r;

    if (pgCollision_CirclePoint(circle, x1, y1) ||
        pgCollision_CirclePoint(circle, x2, y2))
        return 1;

    float dx = x1 - x2;
    float dy = y1 - y2;
    float len = sqrt((dx * dx) + (dy * dy));

    float dot =
        (((cx - x1) * (x2 - x1)) + ((cy - y1) * (y2 - y1))) / (len * len);

    float closest_x = x1 + (dot * (x2 - x1));
    float closest_y = y1 + (dot * (y2 - y1));

    pgLineBase line2 = {x1, y1, x2, y2};
    if (!pgCollision_LinePoint(&line2, closest_x, closest_y))
        return 0;

    dx = closest_x - cx;
    dy = closest_y - cy;
    float distance = sqrt((dx * dx) + (dy * dy));

    return distance <= r;
}

static int
pgCollision_CircleCircle(pgCircleBase *A, pgCircleBase *B)
{
    float dx, dy;
    float sum_radi;

    dx = A->x - B->x;
    dy = A->y - B->y;
    sum_radi = A->r + B->r;

    return dx * dx + dy * dy <= sum_radi * sum_radi;
}

static int
pgIntersection_LineRect(pgLineBase *line, SDL_Rect *rect, float *X, float *Y,
                        float *T)
{
    float x = (float)rect->x;
    float y = (float)rect->y;
    float w = (float)rect->w;
    float h = (float)rect->h;

    pgLineBase a = {x, y, x + w, y};
    pgLineBase b = {x, y, x, y + h};
    pgLineBase c = {x, y + h, x + w, y + h};
    pgLineBase d = {x + w, y, x + w, y + h};

    int ret = 0;

    float temp_t = FLT_MAX;
    float final_t = FLT_MAX;

    ret |= pgIntersection_LineLine(line, &a, NULL, NULL, &temp_t);
    final_t = MIN(temp_t, final_t);
    ret |= pgIntersection_LineLine(line, &b, NULL, NULL, &temp_t);
    final_t = MIN(temp_t, final_t);
    ret |= pgIntersection_LineLine(line, &c, NULL, NULL, &temp_t);
    final_t = MIN(temp_t, final_t);
    ret |= pgIntersection_LineLine(line, &d, NULL, NULL, &temp_t);
    final_t = MIN(temp_t, final_t);

    if (ret) {
        if (X)
            *X = line->x1 + final_t * (line->x2 - line->x1);
        if (Y)
            *Y = line->y1 + final_t * (line->y2 - line->y1);
        if (T)
            *T = final_t;
    }

    return ret;
}

static int
pgCollision_RectLine(SDL_Rect *rect, pgLineBase *line)
{
    return 0;
}

static int
pgCollision_RectCircle(SDL_Rect *rect, pgCircleBase *circle)
{
    float cx = circle->x, cy = circle->y;
    float rx = (float)rect->x, ry = (float)rect->y;
    float rw = (float)rect->w, rh = (float)rect->h;
    float r_bottom = ry + rh;
    float r_right = rx + rw;

    float test_x = cx;
    float test_y = cy;

    if (cx < rx) {
        test_x = rx;
    }
    else if (cx > r_right) {
        test_x = r_right;
    }

    if (cy < ry) {
        test_y = ry;
    }
    else if (cy > r_bottom) {
        test_y = r_bottom;
    }

    float dx = cx - test_x;
    float dy = cy - test_y;

    return dx * dx + dy * dy <= circle->r_sqr;
    return 0;
}
