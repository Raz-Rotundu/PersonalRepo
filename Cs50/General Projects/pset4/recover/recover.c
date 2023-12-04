#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

//define 8 bits as a byte
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //check if file name given
    if (argc != 2)
    {
        printf("./ recover IMAGE\n");
        return 1;
    }
    //check if file can be opened
    FILE *INFILE = fopen(argv[1], "r");
    //buffer variable 512 bytes at a time
    BYTE buffer[512];
    if (INFILE == NULL)
    {
        printf("file %s not found\n", argv[1]);
        return 1;
    }
    int counter = 000;
    FILE *OUTFILE;
    //read 1 byte, 512 bytes at a time from infile into buffer, until end of file
    while (fread(buffer, 1, 512, INFILE) == 512)
    {
        //check first 3 bytes like this.
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff)
        {
            //check the fourth byte is between 224(0xe0) and 239(0xef)
            if ((224 <= buffer[3]) && (buffer[3] <= 239))
            {
                //buffer for file title
                char *test = malloc(8);
                //numerically iterate the title
                sprintf(test, "%03d.jpg", counter);
                //open the new file for writing
                OUTFILE = fopen(test, "w");
                //write current block, keep writing until another jpg is detected
                //use break
                //DELETE THESE
                //fclose(OUTFILE);
                free(test);
                counter++;
            }
        }
        //seg fault
        if (OUTFILE != NULL)
        {
            fwrite(buffer, 1, 512, OUTFILE);
        }
    }
//close all outfiles
//supposed to be 50
//printf("POSSIBLE PICS: %i\n", counter);
    fclose(INFILE);
}