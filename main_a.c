#include <stdio.h>
#include <stdlib.h>
#include "ppm_lib.h"
#include "string.h"
#include <time.h>
#define MAX_RUN_TIME 1000
int filterSofter[25] = { 0, 0, 0, 0, 0,
                        0, 1, 3, 1, 0,
                        0, 3, 5, 3, 0,
                        0, 1, 3, 1, 0,
                        0, 0, 0, 0, 0 };

int filterSharpen[25] = { -1, -1, -1, -1, -1,
                         -1, -1, -1, -1, -1,
                         -1, -1, 49, -1, -1,
                         -1, -1, -1, -1, -1,
                         -1, -1, -1, -1, -1 };
int filterBlur[25] = { 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0,
                      1, 2, 3, 2, 1,
                      0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0 };
int filterHoriSobel[25] = { 1, 2, 0, -2, -1,
                           4, 8, 0, -8, -4,
                           6, 12, 0, -12, -6,
                           4, 8, 0, -8, -4,
                           1, 2, 0, -2, -1 };
int filterShatter[25] = { 1, 0, 0, 0, 1,
                         0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0,
                         1, 0, 0, 0, 1 };

int filterSoften[25] = { 1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1 };

int filterVerSobel[25] = { -1, -4, -6, -4, -1,
                          -2, -8, -12, -8, -2,
                          0, 0, 0, 0, 0,
                          2, 8, 12, 8, 2,
                          1, 4, 6, 4, 1 };

int calculDivisionFactor(int* filter, int sizeFilter)
{
     int sum = 0;
     for (int i = 0; i < sizeFilter; i++)
     {
          sum += filter[i];
     }

     if (sum == 0)
          return 1;
     return sum;
}

PPMImage* applyFilter(PPMImage* img, int* filter, PPMImage* imgDestination, int divisionFactor)
{
     int top = 0;
     int bottom = img->y;
     int left = 0;
     int right = img->x;

     for (int y = top; y < bottom; y++)
     {
          // for each pixel in the image
          for (int x = left; x < right; x++)
          {
               int gridCounter = 0;
               // reset some values
               int finalRed = 0;
               int finalBlue = 0;
               int finalGreen = 0;
               int positionPixel = x + y * img->x;
               for (int y2 = -2; y2 <= 2; y2++)
               {
                    // and for each pixel around our
                    for (int x2 = -2; x2 <= 2; x2++)
                         // "hot pixel"...
                    { // Add to our running total
                         int Y = y + y2;
                         int X = x + x2;
                         if (X > -1 && Y > -1 && X < img->x && Y < img->y)
                         {
                              int position = X + Y * img->x;
                              finalRed += img->data[position].red * filter[gridCounter];
                              finalBlue += img->data[position].blue * filter[gridCounter];
                              finalGreen += img->data[position].green * filter[gridCounter];
                         }
                         gridCounter++;
                    }
               }
               finalRed /= divisionFactor;
               finalBlue /= divisionFactor;
               finalGreen /= divisionFactor;
               imgDestination->data[positionPixel].red = finalRed;
               imgDestination->data[positionPixel].blue = finalBlue;
               imgDestination->data[positionPixel].green = finalGreen;
          }
     }
     return imgDestination;
}

int main()
{
     clock_t start, end;
     PPMImage* image;
     image = readPPM("mon_image.ppm");
     char name[100];
     int* filter;

     int typeOutput = 0;
     char nameFile[100];
     printf("input type: ");
     scanf("%d", &typeOutput);

     while (typeOutput != -1)
     {
          double cpu_time_used = 0;
          switch (typeOutput)
          {
          case 0:
               strcpy(name, "mon_image_dest_softer.ppm");
               strcpy(nameFile, "result/main_a_softer.txt");
               filter = filterSofter;
               break;
          case 1:
               strcpy(name, "mon_image_dest_soften.ppm");
               strcpy(nameFile, "result/main_a_soften.txt");
               filter = filterSoften;
               break;
          case 2:
               strcpy(name, "mon_image_dest_sharpen.ppm");
               strcpy(nameFile, "result/main_a_sharpen.txt");
               filter = filterSharpen;
               break;
          case 3:
               strcpy(name, "mon_image_dest_shatter.ppm");
               strcpy(nameFile, "result/main_a_shatter.txt");
               filter = filterShatter;
               break;
          case 4:
               strcpy(name, "mon_image_dest_blur.ppm");
               strcpy(nameFile, "result/main_a_blur.txt");
               filter = filterBlur;
               break;
          case 5:
               strcpy(name, "mon_image_dest_horisobel.ppm");
               strcpy(nameFile, "result/main_a_horisobel.txt");
               filter = filterHoriSobel;
               break;
          case 6:
               strcpy(name, "mon_image_dest_versobel.ppm");
               strcpy(nameFile, "result/main_a_versobel.txt");
               filter = filterVerSobel;
               break;
          default:
               break;
          }

          // changeColorPPM(image);
          writePPM(name, image);
          PPMImage* imgDestination = readPPM(name);

          int divisionFactor = calculDivisionFactor(filter, 25);
          int loop = 0;
          double arrayTime[MAX_RUN_TIME + 1];
          while (loop < MAX_RUN_TIME) {
               start = clock();
               imgDestination = applyFilter(image, filter, imgDestination, divisionFactor);
               end = clock();
               double cpu_time_used_temp = ((double)(end - start));
               arrayTime[loop] = cpu_time_used_temp / 1000;
               loop++;
          }
          writePPM(name, imgDestination);

          // write result to file
          FILE* f = fopen(nameFile, "wb");
          for (int i = 0;i < MAX_RUN_TIME;i++) {
               cpu_time_used += arrayTime[i];
               fprintf(f, "%f\n", arrayTime[i]);
          }
          arrayTime[MAX_RUN_TIME] = cpu_time_used;
          fprintf(f, "%f\n", arrayTime[MAX_RUN_TIME]);
          fclose(f);
          printf("apply successful: %3.5f ms\n", cpu_time_used);
          free(imgDestination);

          typeOutput++;
          if(typeOutput >= 7){
               break;
          }
          // printf("input type: ");
          // scanf("%d", &typeOutput);
     }
     free(image);
}