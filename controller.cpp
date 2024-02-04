#include <stdio.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <thread>
#include "node.h"
#define CSV_IO_NO_THREAD
#include "csv.h"
#include <stdlib.h>
#include <sys/wait.h>

using namespace std;

int main()
{
    io::CSVReader<6, io::trim_chars<>,io::double_quote_escape<',','"'>> in("graphs.csv"); // 5 columns in CSV file
   // in.read_header(io::ignore_no_column, "num_nodes", "graph", "start", "end", "points", "path_length");
    in.next_line();

    string graph, points;
    int num_nodes, start, end, path_length;

    while (in.read_row(num_nodes, graph, start, end, points, path_length)) // Read each graph
    {

        int pid;         
        int links[num_nodes][2];

        for(int i = 0; i < num_nodes; i++) // create all pipes for the nodes(processes)
        {
            if(pipe(links[i]))
            {
                fprintf(stderr, "could not open pipe");
                return EXIT_FAILURE;
            }
        }

        size_t pos = 0; 
        while((pos = graph.find("],")) != string::npos) // loop for each node in the graph
        {
            string node = graph.substr(1, pos+1);
            graph.erase(0,pos+2);
            
            int node_id = -1;
            
            if((pos = node.find(":")) != string::npos){
                string node_name = node.substr(0,pos);
                node_id = stoi(node_name);
            
                int neighbors[] = {1,2};
                pid = fork(); //start threads for nodes

            
                if(pid < 0)
                {
                    startup(node_id, neighbors);
                }    
            }


            // change and keep I/O pipes to those nodes
            // give each node the accessible pipes to its neighborhood
            //
        }
    }
        
        

        // wait for all thread startup

}
