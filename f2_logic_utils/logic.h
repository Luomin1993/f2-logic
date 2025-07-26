#ifndef LOGIC_H
#define LOGIC_H

#include "f2poly.h"

typedef struct {
    const char* name;
    F2Poly* poly;
} Predicate;

typedef enum {
    NOT,
    AND,
    OR,
    PLAIN // 直接返回原始谓词
} LogicOp;

// 计算逻辑表达式在指定赋值下的真假（0 或 1）
uint8_t rho(LogicOp op, Predicate* a, Predicate* b, uint8_t* values);

#endif