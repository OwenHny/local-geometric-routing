#include <stdio.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <thread>
#include "./node.cpp"

using namespace std;

int main()
{
    // read graph file
    ifstream file("graphs.csv");

    if(!file.is_open())
    {
        cerr << "Error opening file\n";
        return 1;
    }

    string line;
    while(std::getline(file, line))
    {
        istringstream iss(line);
        string token;
        vector<string> row;

        while (std::getline(iss, token, ',')) {
            row.push_back(token);
        }

        // Print the elements of the row
        for (const auto &element : row) {
            //std::cout << element << " | ";
        }

        cout << "\n";
        
        startup();
        //start threads for nodes

        // change and keep I/O pipes to those nodes
        // give each node the accessible pipes to its neighborhood
        //

        // wait for all thread startup
    }

    file.close();

    
}
