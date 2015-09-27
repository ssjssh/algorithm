/**
*本题目使用C编写，因为Python的int类型是无限大的，要判断一个数字是否溢出非常简单，祝需要和2^32-1比较就好了
*/

#include <stdio.h>
#include <string.h>
#include <limits.h>


int intToString(int i,char *arr){
    int t_len = sprintf(arr,"%d",i);
    arr[t_len] = '\0';
    return t_len;
}
int willOverflow(char *result,int is_negative){
    char min_str[40];
    char max_str[40];
    int max_len = intToString(INT_MAX,max_str);
    int min_len = intToString(INT_MIN,min_str);
    int result_len = strlen(result);
    if((is_negative&&result_len<min_len) || (!is_negative&&result_len<max_len)){
       return 0;
    }
    return is_negative?(strcmp(min_str,result)<0):(strcmp(max_str,result)<0);
}
int reverse(int x) {
    char *s_char,*tar_c;
    int result=0;
    char intStr[40];
    int is_negative=0;
    tar_c = intStr;
    if(x<0){
        *tar_c = '-';
        tar_c++;
        x = -x;
        is_negative=1;
    }

    while(x > 0){
        *tar_c = x%10+'0';
        x /= 10;
        tar_c++;
    }
    *tar_c='\0';
    if(willOverflow(intStr,is_negative)){
           return 0;
    }
    for(tar_c = intStr;(*tar_c)!='\0';tar_c++){
        if ((*tar_c)!='-'){

            result *= 10;
            result += (*tar_c)-'0';
        }
    }
    if(intStr[0]=='-'){
        result = -result;
    }

    return result;
}



int main(){
    printf("%d\n",reverse(1231312));
    printf("%d\n",reverse(123));
    printf("%d\n",reverse(-1231312));
    printf("%d\n",reverse(1000000003));
    printf("%d\n",reverse(-1000000003));
    return 0;
}