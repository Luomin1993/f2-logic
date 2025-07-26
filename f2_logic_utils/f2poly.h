#ifndef F2POLY_H
#define F2POLY_H

#include <stdint.h>
#include <stddef.h>

#define MAX_VARS 32

typedef uint32_t Monomial; // 用位表示：x1*x3 = 0b101

typedef struct {
    Monomial* terms;
    size_t num_terms;
    size_t capacity;
} F2Poly;

// 基本功能
F2Poly* f2poly_empty();
void f2poly_free(F2Poly* p);
void f2poly_add_term(F2Poly* p, Monomial m);
F2Poly* f2poly_add(F2Poly* a, F2Poly* b);
F2Poly* f2poly_mul(F2Poly* a, F2Poly* b);
uint8_t f2poly_eval(F2Poly* p, uint8_t* values);
void f2poly_print(F2Poly* p);

// 新增：从字符串创建
F2Poly* f2poly_create(const char* str);

#endif