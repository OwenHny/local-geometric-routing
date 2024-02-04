#include "node.h"
#include <stdio.h>

// on startup create timer 

//on shutdown stop timer and thread safe compile results

void startup(int input, int neighbors[][2], int num_neighbors)
{

    printf("%i \n\n", input);

    for(int i = 0; i < num_neighbors; i++)
    {
        close(neighbors[i][0]);
    }

    return 0;

}

read_from_input(int input)
{
    FILE *stream;
    int c;
    stream = fdopen(input, "r");
    while((c = fgetc(stream)) != EOF)
    {
        // gather message
    }
}


