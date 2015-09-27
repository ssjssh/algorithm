#include <stdio.h>
#include <string.h>
#include <limits.h>


static int intToString(int i,char *arr){
    int t_len = sprintf(arr,"%d",i);
    arr[t_len] = '\0';
    return t_len;
}
static int myStrcmp(char *start,char *end,char *other){
    for(char *c1 = start,*c2 = other;c1<=end&&c2!='\0';c1++,c2++){
        if (*c1 > *c2){
            return 1;
        }else if(*c1 < *c2){
            return -1;
        }
    }
    return 0;
}

int myAtoi(char* str) {
    int is_negative = 0;
    char *start=NULL,*end=NULL;
    for(char *c=str;c!='\0';c++){
        if(start==NULL && (*c == ' ' || *c =='\n' || *c == '\t')){
            continue;
        }else if((*c=='-' || (*c >='0' && *c<='9') || *c=='+') && start==NULL){
            start = c;
            if(*c == '-'){
                is_negative=1;
            }
        }else if(*c >='0' && *c<='9'&& start!=NULL){
             end = c;
        }else{
            break;
        }
    }

    if(start==NULL){
        return 0;
    }else if (end==NULL){
        end = start;
    }

    if(*start == '+'){
        start++;
    }

//    printf("%c:%c\n",*start,*end);
    //检查是否越界
    int result_len = end - start + 1;
    if(is_negative){
        char min_str[40];
        int min_len = intToString(INT_MIN,min_str);
        if(result_len>min_len || (result_len == min_len && myStrcmp(start,end,min_str)>0)){
            return INT_MIN;
        }
    }else{
        char max_str[40];
        int max_len = intToString(INT_MAX,max_str);
        if(result_len>max_len || (result_len == max_len && myStrcmp(start,end,max_str)>0)){
             return INT_MAX;
        }
    }

    int result = 0;

//       printf("%c:%c",*start,*end);
    for(char *c=start;c<=end;c++){
        if(*c != '-' && *c != '+'){
            result *= 10;
            result += (*c - '0');
        }
    }

    if(*start=='-'){
        result = -result;
    }
    return result;
}


int main(){
    printf("%d\n",myAtoi("+1231312"));
    printf("%d\n",myAtoi("      -11919730356x"));
    printf("%d\n",myAtoi("    +1146905820n1"));
    printf("%d\n",myAtoi("1"));
    printf("%d\n",myAtoi("123"));
    printf("%d\n",myAtoi("-1231312"));
    printf("%d\n",myAtoi("-1231312fqwef"));
    printf("%d\n",myAtoi("-1231312 992"));
    printf("%d\n",myAtoi("3000000001"));
    printf("%d\n",myAtoi("-3000000001"));
    printf("%d\n",myAtoi("wefwqef-3000000001"));
    printf("%d\n",myAtoi("   -3000000001"));
    return 0;
}