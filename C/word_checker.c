#include<stdio.h>


int main()
{
    int x;
    while(1)
    {
        scanf("%d",&x);
        if(x == 0)
           break;
        printf("Number %d id hexadecimal is %X\n",x , x);
    }

    return 0;
}
