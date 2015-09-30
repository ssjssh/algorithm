/**
*Determine whether an integer is a palindrome. Do this without extra space.
*/

/**
可以直接把int逆转，然后只需要判断他们是不是相等就可以了
关于溢出的问题
1，如果原来的数字没有溢出，那么如果他们是回文，那么逆转后的数字也不会越界。这样保证如果是回文，那么就不会越界。
2，如果原来的数字不是回文，那么逆转后的数字一定不会溢出，因此一旦在逆转数字的时候出现溢出，那么就可以判断这个数字不是回文
**/

#include <stdio.h>
#include <limits.h>
#include <stdlib.h>
#include <stdbool.h>

bool isPalindrome(int x){
    if(x<0) return 0;
    int res = 0;
    int tmp = x;
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
      return res==tmp;
}

int main(){
    printf("%d\n",isPalindrome(1));
    printf("%d\n",isPalindrome(0));
    printf("%d\n",isPalindrome(12311321));
    printf("%d\n",isPalindrome(-12311321));
    printf("%d\n",isPalindrome(-2147447412));
    return 0;
}
