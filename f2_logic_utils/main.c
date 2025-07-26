#include <stdio.h>
#include "f2poly.h"
#include "logic.h"
// gcc -o logic_test main.c f2poly.c logic.c
// ./logic_test
int main() {
    // 创建谓词 p(x1,x2,x3) = x1*x2 + x3
    F2Poly* f = f2poly_create("x1*x2 + x3");
    Predicate p = {"p", f};

    // 创建谓词 q(x1,x2,x3) = x2 + 1
    F2Poly* g = f2poly_create("x2 + 1");
    Predicate q = {"q", g};

    // 输入变量赋值：x1 = 1, x2 = 0, x3 = 1
    uint8_t input[3] = {1, 0, 1};

    printf("变量赋值：x1=%d, x2=%d, x3=%d\n", input[0], input[1], input[2]);

    // p,q
    printf("p 真值: %d\n", rho(PLAIN, &p, NULL, input));
    printf("q 真值: %d\n", rho(PLAIN, &p, NULL, input));

    // ¬p
    printf("¬p 真值: %d\n", rho(NOT, &p, NULL, input));

    // p ∧ q
    printf("p ∧ q 真值: %d\n", rho(AND, &p, &q, input));

    // p ∨ q
    printf("p ∨ q 真值: %d\n", rho(OR, &p, &q, input));

    // 清理
    f2poly_free(f);
    f2poly_free(g);

    return 0;
}
