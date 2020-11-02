#include "string.h"
#include <cuda_device_runtime_api.h>
#include <cuda_runtime_api.h>
#include <driver_types.h>
#include <stdio.h>
#include <stdlib.h>
extern "C" {
#include "ppm_lib.h"
}
#define MAX_RUN_TIME 1

static void HandleError(cudaError_t err, const char *file, int line) {
  if (err != cudaSuccess) {
    printf("%s in %s at line %d \n", cudaGetErrorString(err), file, line);
    exit(EXIT_FAILURE);
  }
}
#define HANDLE_ERROR(err) (HandleError(err, __FILE__, __LINE__))
#define FILTER_SIZE 25

int filterSofter[FILTER_SIZE] = {0, 0, 0, 0, 0, 0, 1, 3, 1, 0, 0, 3, 5,
                                 3, 0, 0, 1, 3, 1, 0, 0, 0, 0, 0, 0};

int filterSharpen[FILTER_SIZE] = {-1, -1, -1, -1, -1, -1, -1, -1, -1,
                                  -1, -1, -1, 49, -1, -1, -1, -1, -1,
                                  -1, -1, -1, -1, -1, -1, -1};
int filterBlur[FILTER_SIZE] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3,
                               2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int filterHoriSobel[FILTER_SIZE] = {1,  2,  0,  -2, -1,  4,  8, 0, -8,
                                    -4, 6,  12, 0,  -12, -6, 4, 8, 0,
                                    -8, -4, 1,  2,  0,   -2, -1};
int filterShatter[FILTER_SIZE] = {1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1};

int filterSoften[FILTER_SIZE] = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};

int filterVerSobel[FILTER_SIZE] = {-1, -4, -6, -4, -1, -2, -8, -12, -8,
                                   -2, 0,  0,  0,  0,  0,  2,  8,   12,
                                   8,  2,  1,  4,  6,  4,  1};

int calculDivisionFactor(int *filter, int sizeFilter) {
  int sum = 0;
  for (int i = 0; i < sizeFilter; i++) {
    sum += filter[i];
  }

  if (sum == 0)
    return 1;

  return sum;
}

__global__ void applyFilterGPUAvance(PPMPixel *img, int *filter, PPMPixel *data,
                                     int divisionFactor) {
  int gridCounter = 0;
  int finalRed = 0;
  int finalBlue = 0;
  int finalGreen = 0;
  for (int y2 = -2; y2 <= 2; y2++) {
    for (int x2 = -2; x2 <= 2; x2++) {
      int Y = blockIdx.x + y2;
      int X = threadIdx.x + x2;
      if (X > -1 && Y > -1 && X < blockDim.x && Y < gridDim.x) {
        int position = X + Y * blockDim.x;
        finalRed += img[position].red * filter[gridCounter];
        finalBlue += img[position].blue * filter[gridCounter];
        finalGreen += img[position].green * filter[gridCounter];
      }
      gridCounter++;
    }
  }
  int positionPixel = threadIdx.x + blockIdx.x * blockDim.x;
  finalRed /= divisionFactor;
  finalBlue /= divisionFactor;
  finalGreen /= divisionFactor;
  data[positionPixel].red = finalRed;
  data[positionPixel].blue = finalBlue;
  data[positionPixel].green = finalGreen;
}

int main() {
  cudaEvent_t start, stop;
  float time;
  PPMImage *image;
  char name[100];
  int *filter;

  int typeOutput = 0;
  char nameFile[100];
  printf("input type: ");
  scanf("%d", &typeOutput);

  while (typeOutput != -1) {
    double gpu_time_used = 0;
    image = readPPM("mon_image.ppm");
    switch (typeOutput) {
    case 0:
      strcpy(name, "mon_image_dest_softer.ppm");
      strcpy(nameFile, "result/main_b_softer.txt");
      filter = filterSofter;
      break;
    case 1:
      strcpy(name, "mon_image_dest_soften.ppm");
      strcpy(nameFile, "result/main_b_soften.txt");
      filter = filterSoften;
      break;
    case 2:
      strcpy(name, "mon_image_dest_sharpen.ppm");
      strcpy(nameFile, "result/main_b_sharpen.txt");
      filter = filterSharpen;
      break;
    case 3:
      strcpy(name, "mon_image_dest_shatter.ppm");
      strcpy(nameFile, "result/main_b_shatter.txt");
      filter = filterShatter;
      break;
    case 4:
      strcpy(name, "mon_image_dest_blur.ppm");
      strcpy(nameFile, "result/main_b_blur.txt");
      filter = filterBlur;
      break;
    case 5:
      strcpy(name, "mon_image_dest_horisobel.ppm");
      strcpy(nameFile, "result/main_b_horisobel.txt");
      filter = filterHoriSobel;
      break;
    case 6:
      strcpy(name, "mon_image_dest_versobel.ppm");
      strcpy(nameFile, "result/main_b_versobel.txt");
      filter = filterVerSobel;
      break;
    default:
      break;
    }

    // changeColorPPM(image);
    writePPM(name, image);
    //     PPMImage *imgDestination = readPPM(name);

    PPMPixel *dev_dataImage;
    PPMPixel *dev_dataDestination;
    int *dev_filter;

    // start setup data malloc
    HANDLE_ERROR(cudaMalloc((PPMPixel **)&dev_dataImage,
                            image->x * image->y * sizeof(PPMPixel)));
    HANDLE_ERROR(cudaMemcpy(dev_dataImage, image->data,
                            image->x * image->y * sizeof(PPMPixel),
                            cudaMemcpyHostToDevice));
    HANDLE_ERROR(cudaMalloc((PPMPixel **)&dev_dataDestination,
                            image->x * image->y * sizeof(PPMPixel)));
    HANDLE_ERROR(cudaMemcpy(dev_dataDestination, image->data,
                            image->x * image->y * sizeof(PPMPixel),
                            cudaMemcpyHostToDevice));

    cudaMalloc((int **)&dev_filter, FILTER_SIZE * sizeof(int));
    cudaMemcpy(dev_filter, filter, FILTER_SIZE * sizeof(int),
               cudaMemcpyHostToDevice);
    // end setup data malloc

    int divisionFactor = calculDivisionFactor(filter, FILTER_SIZE);

    int loop = 0;
    double arrayTime[MAX_RUN_TIME + 1];
    while (loop < MAX_RUN_TIME) {
      cudaEventCreate(&start);
      cudaEventCreate(&stop);
      cudaEventRecord(start, 0);
      applyFilterGPUAvance<<<image->y, image->x>>>(
          dev_dataImage, dev_filter, dev_dataDestination, divisionFactor);
      cudaDeviceSynchronize();
      cudaEventRecord(stop, 0);
      cudaEventSynchronize(stop);
      cudaEventElapsedTime(&time, start, stop);
      arrayTime[loop] = time;
      loop++;
    }

    HANDLE_ERROR(cudaMemcpy(image->data, dev_dataDestination,
                            image->x * image->y * sizeof(PPMPixel),
                            cudaMemcpyDeviceToHost));
    printf(">%s \n", cudaGetErrorString(cudaGetLastError()));
    writePPM(name, image);

    // write result to file
    FILE *f = fopen(nameFile, "wb");
    for (int i = 0; i < MAX_RUN_TIME; i++) {
      gpu_time_used += arrayTime[i];
      fprintf(f, "%f\n", arrayTime[i]);
    }
    arrayTime[MAX_RUN_TIME] = gpu_time_used;
    fprintf(f, "%f\n", arrayTime[MAX_RUN_TIME]);
    fclose(f);
    printf("apply successful: %3.5f ms\n", gpu_time_used);
    printf("%d %d\n", image->x, image->y);

    // free cuda
    cudaFree(dev_dataImage);
    cudaFree(dev_filter);

    typeOutput++;
    if (typeOutput >= 7) {
      break;
    }
    // printf("input type: ");
    // scanf("%d", &typeOutput);
  }
  free(image);
}