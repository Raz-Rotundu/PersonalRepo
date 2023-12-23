// A function to determine if two unsigned ints can be safely added
#include <stdio.h>
int uadd_ok(unsigned int x, unsigned int y);

int uadd_ok(unsigned int x, unsigned int y){
    unsigned int result = x + y;
    if(result < x || result < y){
        return 0; //FALSE, will overflow
    }
    else{
        return 1; //TRUE, will not overflow
    }
}

int main(){
    int max = 4294967295;
    int y = 1;
    printf("%i\n",uadd_ok(max, y)); //O
    printf("%i\n", uadd_ok(y, y)); //1
    

}