#ifdef __AVX2__
#include <immintrin.h>
#endif

#include "include/collisions.h"
#include <stdio.h>

#ifndef DOT2D
#define DOT2D(X0, Y0, X1, Y1) ((X0) * (X1) + (Y0) * (Y1))
#endif /* ~DOT2D */

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
pgIntersection_LineLine(pgLineBase *A, pgLineBase *B, double *X, double *Y,
                        double *T)
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
        if (T)
            *T = t;
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
    return dx * dx + dy * dy <= circle->r_sqr;
}

static int
pgIntersection_LineCircle(pgLineBase *line, pgCircleBase *circle, double *X,
                          double *Y, double *T)
{
    double x1 = line->x1;
    double y1 = line->y1;
    double x2 = line->x2;
    double y2 = line->y2;
    double xc = circle->x;
    double yc = circle->y;
    double r = circle->r;
    double rsq = circle->r_sqr;

    double dx = x2 - x1;
    double dy = y2 - y1;
    double A = dx * dx + dy * dy;
    double B = 2 * (dx * (x1 - xc) + dy * (y1 - yc));
    double C = (x1 - xc) * (x1 - xc) + (y1 - yc) * (y1 - yc) - rsq;
    double descriminant = B * B - 4 * A * C;
    if (descriminant < 0) {
        return 0;
    }
    double t = (-B - sqrt(descriminant)) / (2 * A);
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
    double dx, dy;
    double sum_radi;

    dx = A->x - B->x;
    dy = A->y - B->y;
    sum_radi = A->r + B->r;

    return dx * dx + dy * dy <= sum_radi * sum_radi;
}

static int
pgIntersection_LineRect(pgLineBase *line, SDL_Rect *rect, double *X, double *Y,
                        double *T)
{
#ifdef __AVX2__
    // this function does 4 line-line collisions at once
    double Rx = (double)rect->x;
    double Ry = (double)rect->y;
    double Rw = (double)rect->w;
    double Rh = (double)rect->h;

    // here we start to setup the variables
    __m256d x1_256d = _mm256_set1_pd(line->x1);
    __m256d y1_256d = _mm256_set1_pd(line->y1);
    __m256d x2_256d = _mm256_set1_pd(line->x2);
    __m256d y2_256d = _mm256_set1_pd(line->y2);
    __m256d x3_256d = _mm256_set_pd(Rx, Rx, Rx, Rx + Rw);
    __m256d y3_256d = _mm256_set_pd(Ry, Ry, Ry + Rh, Ry);
    __m256d x4_256d = _mm256_set_pd(Rx + Rw, Rx, Rx + Rw, Rx + Rw);
    __m256d y4_256d = _mm256_set_pd(Ry, Ry + Rh, Ry + Rh, Ry + Rh);

    // here we calculate the differences between the the coords of the points
    __m256d x1_m_x2_256d = _mm256_sub_pd(x1_256d, x2_256d);
    __m256d y3_m_y4_256d = _mm256_sub_pd(y3_256d, y4_256d);
    __m256d y1_m_y2_256d = _mm256_sub_pd(y1_256d, y2_256d);
    __m256d x3_m_x4_256d = _mm256_sub_pd(x3_256d, x4_256d);

    // we calculate the denominator of the equations
    __m256d den_256d =
        _mm256_sub_pd(_mm256_mul_pd(x1_m_x2_256d, y3_m_y4_256d),
                      _mm256_mul_pd(y1_m_y2_256d, x3_m_x4_256d));

    // if the denominator is 0 then the line is parallel to the other line
    // in this occasion this can't be true here as a line will never be
    // parallel to all four sides of a rectangle
    __m256d den_zero_256d =
        _mm256_cmp_pd(den_256d, _mm256_setzero_pd(), _CMP_EQ_OQ);

    // we dont want to cause any floating point errors by dividing by 0
    // so we set the ones that are equal to 0 to 1
    den_256d = _mm256_or_pd(den_zero_256d, den_256d);

    // we calculate the rest of the differences between the coords of the
    // points
    __m256d x1_m_x3_256d = _mm256_sub_pd(x1_256d, x3_256d);
    __m256d y1_m_y3_256d = _mm256_sub_pd(y1_256d, y3_256d);

    // calculate the t values
    __m256d t_256d = _mm256_sub_pd(_mm256_mul_pd(x1_m_x3_256d, y3_m_y4_256d),
                                   _mm256_mul_pd(y1_m_y3_256d, x3_m_x4_256d));
    t_256d = _mm256_div_pd(t_256d, den_256d);

    // calculate the u values
    __m256d u_256d = _mm256_sub_pd(_mm256_mul_pd(x1_m_x2_256d, y1_m_y3_256d),
                                   _mm256_mul_pd(y1_m_y2_256d, x1_m_x3_256d));
    u_256d =
        _mm256_mul_pd(_mm256_div_pd(u_256d, den_256d), _mm256_set1_pd(-1.0));

    // we check this condition t >= 0 && t <= 1 && u >= 0 && u <= 1
    __m256d ones_256d = _mm256_set1_pd(1.0);
    __m256d zeros_256d = _mm256_set1_pd(0.0);
    __m256d t_zero_256d = _mm256_cmp_pd(t_256d, zeros_256d, _CMP_GE_OQ);
    __m256d t_one_256d = _mm256_cmp_pd(t_256d, ones_256d, _CMP_LE_OQ);
    __m256d u_zero_256d = _mm256_cmp_pd(u_256d, zeros_256d, _CMP_GE_OQ);
    __m256d u_one_256d = _mm256_cmp_pd(u_256d, ones_256d, _CMP_LE_OQ);
    __m256d t_u_256d = _mm256_and_pd(_mm256_and_pd(t_zero_256d, t_one_256d),
                                     _mm256_and_pd(u_zero_256d, u_one_256d));

    // if no lines touch the rectangle then this will be true
    if (_mm256_movemask_pd(t_u_256d) == 0x0) {
        return 0;
    }

    double t = DBL_MAX;

    // here we know that there is at least one intersection so
    // we search for the smallest t value that still meets the above conditions
    int i = 0;
    for (i = 0; i < 4; i++) {
        if (((double *)&t_u_256d)[i]) {
            t = MIN(t, ((double *)&t_256d)[i]);
        }
    }

    // outputs
    if (T)
        *T = t;
    if (X)
        *X = line->x1 + t * (line->x2 - line->x1);
    if (Y)
        *Y = line->y1 + t * (line->y2 - line->y1);

    return 1;
#else

    double x = (double)rect->x;
    double y = (double)rect->y;
    double w = (double)rect->w;
    double h = (double)rect->h;

    pgLineBase a = {x, y, x + w, y};
    pgLineBase b = {x, y, x, y + h};
    pgLineBase c = {x, y + h, x + w, y + h};
    pgLineBase d = {x + w, y, x + w, y + h};

    int ret = 0;

    double temp_t = DBL_MAX;
    double final_t = DBL_MAX;

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
#endif /* ~__AVX2__ */
}

static int
pgCollision_RectLine(SDL_Rect *rect, pgLineBase *line)
{
    return 0;
}

static int
pgCollision_RectCircle(SDL_Rect *rect, pgCircleBase *circle)
{
    double cx = circle->x, cy = circle->y;
    double rx = (double)rect->x, ry = (double)rect->y;
    double rw = (double)rect->w, rh = (double)rect->h;
    double r_bottom = ry + rh;
    double r_right = rx + rw;

    double test_x = cx;
    double test_y = cy;

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

    double dx = cx - test_x;
    double dy = cy - test_y;

    return dx * dx + dy * dy <= circle->r_sqr;
    return 0;
}
