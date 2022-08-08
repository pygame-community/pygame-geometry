#ifndef _SIMD_COLLISIONS_H_
#define _SIMD_COLLISIONS_H_

#include "include/pygame.h"
#include "include/geometry.h"

static int
pgIntersection_LineRect_avx2(pgLineBase *, SDL_Rect *, double *, double *, double *);

#endif /* ~_SIMD_COLLISIONS_H_ */
