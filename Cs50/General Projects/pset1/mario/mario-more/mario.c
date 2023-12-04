# include <stdio.h>
# include <cs50.h>

void RowPrint(int x);
void ColPrint(int y);
void RevPrint(int row, int height);
int main(void)
{
    int height;
    //collect input, check if in correct range
    do
    {
        height = get_int("height? ");
    }
    while (height < 1 || height > 8);
    //print height first
    //printf ("Height: %i\n", height);
    //print pyramid
    RowPrint(height);
}
//prints the left side of the pyramid
void RevPrint(int row, int height)
{
    //print (row-height) spaces
    for (int i = 0; i < (height - row); i++)
    {
        printf(" ");
    }
    //hashtags
    ColPrint(row);
}
//prints the right side of the pyramid
void ColPrint(int y)
{
    for (int q = 0; q < y; q++)
    {
        printf("#");
    }
}
//prints the correct number of rows
void RowPrint(int x)
{
    for (int i = 1; i < (x + 1); i++)
    {
        //print left side of pyramid
        RevPrint(i, x);
        //space for design
        printf("  ");
        //for each row, print i amount of hashtags
        ColPrint(i);
        printf("\n");
    }

}