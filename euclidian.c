#include "stdio.h"

void main(){ 
    int a,b;
    int x;
    printf("Numbers:\n");
    scanf("%d", &a);
    printf("");
    scanf("%d", &b);
    if(a<b){
        a,b=b,a;
    }

    while(a%b!=0){
        x=b;
        b=a%b;
        a=x;
    }
    printf("The GMD is: %d",b);
}