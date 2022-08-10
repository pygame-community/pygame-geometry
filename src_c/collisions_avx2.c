#include "include/pygame.h"
#include "include/geometry.h"

#include <immintrin.h>


static PG_FORCEINLINE int
pgIntersection_LineRect_avx2(pgLineBase *line, SDL_Rect *rect, double *X, double *Y, double *T) {
    double Rx = (double)rect->x;
    double Ry = (double)rect->y;
    double Rw = (double)rect->w;
    double Rh = (double)rect->h;

    __m256d x1_256d = _mm256_set1_pd(line->x1);
    __m256d y1_256d = _mm256_set1_pd(line->y1);
    __m256d x2_256d = _mm256_set1_pd(line->x2);
    __m256d y2_256d = _mm256_set1_pd(line->y2);

    __m256d x3_256d = _mm256_set_pd(Rx, Rx, Rx, Rx + Rw);
    __m256d y3_256d =_mm256_set_pd(Ry, Ry, Ry + Rh, Ry);
    __m256d x4_256d =_mm256_set_pd(Rx + Rw, Rx, Rx + Rw, Rx + Rw);
    __m256d y4_256d =_mm256_set_pd(Ry, Ry + Rh, Ry + Rh, Ry + Rh);

    __m256d x1_m_x2_256d = _mm256_sub_pd(x1_256d, x2_256d);
    __m256d y3_m_y4_256d = _mm256_sub_pd(y3_256d, y4_256d);
    __m256d y1_m_y2_256d = _mm256_sub_pd(y1_256d, y2_256d);
    __m256d x3_m_x4_256d = _mm256_sub_pd(x3_256d, x4_256d);

    __m256d den_256d = _mm256_sub_pd(
        _mm256_mul_pd(x1_m_x2_256d, y3_m_y4_256d),
        _mm256_mul_pd(y1_m_y2_256d, x3_m_x4_256d)
    );

    __m256d den_zero_256d = _mm256_cmp_pd(den_256d, _mm256_setzero_pd(), _CMP_EQ_OQ);
    if (_mm256_movemask_pd(den_zero_256d) == 0xF) {
        return 0;
    }
    den_256d = _mm256_or_pd(den_zero_256d, den_256d);
    
    __m256d x1_m_x3_256d = _mm256_sub_pd(x1_256d, x3_256d);
    __m256d y1_m_y3_256d = _mm256_sub_pd(y1_256d, y3_256d);

    __m256d t_256d = _mm256_sub_pd(
        _mm256_mul_pd(x1_m_x3_256d, y3_m_y4_256d),
        _mm256_mul_pd(y1_m_y3_256d, x3_m_x4_256d)
    );
    t_256d = _mm256_div_pd(t_256d, den_256d);

    __m256d u_256d = _mm256_sub_pd(
        _mm256_mul_pd(x1_m_x2_256d, y1_m_y3_256d),
        _mm256_mul_pd(y1_m_y2_256d, x1_m_x3_256d)
    );
    u_256d = _mm256_mul_pd(
        _mm256_div_pd(u_256d, den_256d),
        _mm256_set1_pd(-1.0)
    );

    __m256d t_zero_256d = _mm256_cmp_pd(t_256d, _mm256_setzero_pd(), _CMP_GE_OQ);
    __m256d t_one_256d = _mm256_cmp_pd(t_256d, _mm256_set1_pd(1.0), _CMP_LE_OQ);
    __m256d u_zero_256d = _mm256_cmp_pd(u_256d, _mm256_setzero_pd(), _CMP_GE_OQ);
    __m256d u_one_256d = _mm256_cmp_pd(u_256d, _mm256_set1_pd(1.0), _CMP_LE_OQ);
    __m256d t_u_256d = _mm256_and_pd(
        _mm256_and_pd(t_zero_256d, t_one_256d),
        _mm256_and_pd(u_zero_256d, u_one_256d)
    );
    if (_mm256_movemask_pd(t_u_256d) == 0x0) {
        return 0;
    }

    double t = DBL_MAX;

    int i = 0;
    for (i = 0; i < 4; i++) {
        double t_ = ((double*)&t_256d)[i];
        double u_ = ((double*)&u_256d)[i];
        if (t_ >= 0 && t_ <= 1 && u_ >= 0 && u_ <= 1) {
           t = MIN(t, t_); 
        }
    }

    if (t <= 1 && t >= 0) {
        if (T) *T = t;
        if (X) *X = line->x1 + t * (line->x2 - line->x1);
        if (Y) *Y = line->y1 + t * (line->y2 - line->y1);
        return 1;
    }

    return 0;
}

