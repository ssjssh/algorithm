/**
*本题目使用C编写，因为Python的int类型是无限大的，要判断一个数字是否溢出非常简单，祝需要和2^32-1比较就好了
*/

#include <stdio.h>
#include <limits.h>
#include <stdlib.h>

int reverse(int x) {
      int res = 0;
      while (x != 0) {
          /**
          * 假设INT_MAX / 10 ＝ m，因为他是一个浮点数，那么假设他在n-1，n之间
          * 那么也就是abs(res)的最大值是n-1，这个数字是在接下来的计算中可能会越界（依赖于x % 10的值）
          * 如果abs(res)为n，那么就一定会发生越界
          */
          if (abs(res) > INT_MAX / 10 || abs(res) * 10 > INT_MAX - abs(x) % 10) return 0;
           res = res * 10 + x % 10;
           x /= 10;
      }
      return res;
}



int main(){
    printf("%d\n",reverse(1231312));
    printf("%d\n",reverse(123));
    printf("%d\n",reverse(-1231312));
    printf("%d\n",reverse(1000000003));
    printf("%d\n",reverse(-1000000003));
    return 0;
}