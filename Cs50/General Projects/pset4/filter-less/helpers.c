#include "helpers.h"
#include <math.h>
//copy check
#include <stdio.h>
#include <stdbool.h>
//struct
struct RGBSTORE
{
    float red; //or int
    float green;
    float blue;
} RGBSTORE;

//helper prototypes
int sepiaRed(int oRed, int oGreen, int oBlue);
int sepiaGreen(int oRed, int oGreen, int oBlue);
int sepiaBlue(int oRed, int oGreen, int oBlue);
bool rgbcompare(RGBTRIPLE a, RGBTRIPLE b);
void rgbAdd(struct RGBSTORE *in, RGBTRIPLE *target);
void blurAvg(struct RGBSTORE *in, int counter);
void setPixel(RGBTRIPLE *current, struct RGBSTORE *copy);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //Iterate through every pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //store current pixel in variable
            RGBTRIPLE pixel = image[i][j];
            //to replace original pixel
            RGBTRIPLE gray;
            //average and round the original rgb values
            int avg = round((pixel.rgbtRed + pixel.rgbtBlue + pixel.rgbtGreen) / 3.0);
            //set the replacement's rgb values to the obtained avg
            gray.rgbtRed = avg;
            gray.rgbtBlue = avg;
            gray.rgbtGreen = avg;
            //replace original pixel with the gray
            image[i][j] = gray;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE pixel = image [i][j];
            RGBTRIPLE sepia;
            //storing original rgb values for formula
            BYTE originalRed = pixel.rgbtRed;
            BYTE originalGreen = pixel.rgbtGreen;
            BYTE originalBlue = pixel.rgbtBlue;
            //calculating sepia values
            sepia.rgbtRed = sepiaRed(originalRed, originalGreen, originalBlue);
            sepia.rgbtGreen = sepiaGreen(originalRed, originalGreen, originalBlue);
            sepia.rgbtBlue = sepiaBlue(originalRed, originalGreen, originalBlue);
            //replacing the orignal pixel
            image[i][j] = sepia;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        //iterate only to the halfway mark
        for (int j = 0; j < (width / 2); j++)
        {
            RGBTRIPLE *curr = &image[i][j];
            RGBTRIPLE *mirr = &image[i][(width - 1) - j];
            RGBTRIPLE temp = *curr;
            *curr = *mirr;
            *mirr = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //copy storage
    RGBTRIPLE copy[height][width];
    //copy the original array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    /*DELETE THIScheck if copied properly
    int same = 1; //true by default
    for (int x = 0; x < height; x++)
    {
        for (int y = 0; y < width; y++)
        {
            if (!rgbcompare(copy[x][y], image[x][y]))
            {
                same = 0; //false
            }
        }
    }
    if (same == 0)
    {
        printf("NOT COPIED PROPERLY\n");
    }
    else
    {
        printf("COPIED PROPERLY\n");
    }
    DELETE ABOVE */

    //blur the pixel by reading adjacent ones
    struct RGBSTORE blurPixel;
    blurPixel.red = 0;
    blurPixel.green = 0;
    blurPixel.blue = 0;
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width ; w++)
        {
            RGBTRIPLE *currentPixel = &image[h][w];
            blurPixel.red = 0;
            blurPixel.green = 0;
            blurPixel.blue = 0;
            //add current values
            rgbAdd(&blurPixel, &image[h][w]);
            int counter = 1;
            //check below
            if ((h + 1) < height)
            {
                rgbAdd(&blurPixel, &copy[h + 1][w]);
                counter++;
            }
            //check above
            if ((h - 1) >= 0)
            {
                rgbAdd(&blurPixel, &copy[h - 1][w]);
                counter++;
            }
            //check right
            if ((w + 1) < width)// or <= width
            {
                rgbAdd(&blurPixel, &copy[h][w + 1]);
                counter++;
            }
            //check left
            if ((w - 1) >= 0)
            {
                rgbAdd(&blurPixel, &copy[h][w - 1]);
                counter++;
            }
            //check lower right
            if (((h + 1) < height) && (w + 1) < width)
            {
                rgbAdd(&blurPixel, &copy[h + 1][w + 1]);
                counter++;
            }
            //check lower left
            if (((h + 1) < height) && ((w - 1) >= 0))
            {
                rgbAdd(&blurPixel, &copy[h + 1][w - 1]);
                counter++;
            }
            //check upper right
            if (((h - 1) >= 0) && ((w + 1) < width))
            {
                rgbAdd(&blurPixel, &copy[h - 1][w + 1]);
                counter++;
            }
            //check upper left
            if (((h - 1) >= 0) && ((w - 1) >= 0))
            {
                rgbAdd(&blurPixel, &copy[h - 1][w - 1]);
                counter++;
            }
            blurAvg(&blurPixel, counter);
            setPixel(currentPixel, &blurPixel);
        }
    }
}
//helper functions
//replaces the rgbt values of the current pixel with the copy's(averaged values)
void setPixel(RGBTRIPLE *current, struct RGBSTORE *copy)
{
    current->rgbtRed = copy->red;
    current->rgbtGreen = copy->green;
    current->rgbtBlue = copy->blue;
    return;
}
//sets the blurred pixels rgb values to the average of measured squares
void blurAvg(struct RGBSTORE *in, int counter)
{
    in->red = round((in->red) / counter);
    in->green = round((in->green) / counter);
    in->blue = round((in->blue) / counter);
    return;
}
//takes the rgb values of one pixel and adds them to storage
void rgbAdd(struct RGBSTORE *in, RGBTRIPLE *target)
{
    in->red += target->rgbtRed;
    in->green += target->rgbtGreen;
    in->blue += target->rgbtBlue;
    return;
}
//compares 2 rgbtriple pixels for equality
bool rgbcompare(RGBTRIPLE a, RGBTRIPLE b)
{
    if (a.rgbtRed != b.rgbtRed)
    {
        return false;
    }
    if (a.rgbtGreen != b.rgbtGreen)
    {
        return false;
    }
    if (a.rgbtBlue != b.rgbtBlue)
    {
        return false;
    }
    return true;
}
int sepiaRed(int oRed, int oGreen, int oBlue)
{
    int sRed = round(0.393 * oRed + 0.769 * oGreen + 0.189 * oBlue);
    if (sRed > 255)
    {
        sRed = 255;
    }
    return sRed;
}
int sepiaGreen(int oRed, int oGreen, int oBlue)
{
    int sGreen = round(0.349 * oRed + 0.686 * oGreen + 0.168 * oBlue);
    if (sGreen > 255)
    {
        sGreen = 255;
    }
    return sGreen;
}
int sepiaBlue(int oRed, int oGreen, int oBlue)
{
    int sBlue = round(0.272 * oRed + 0.534 * oGreen + 0.131 * oBlue);
    if (sBlue > 255)
    {
        sBlue = 255;
    }
    return sBlue;
}