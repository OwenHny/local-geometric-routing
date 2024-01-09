# local-geometric-routing
Performance Analysis of Local Geometric Routing Algorithms

This project will be testing the real-world performance of local geometric routing algorithms and
comparing their outcomes. For each of the questions the initial goal will be to give data on
performance, afterwards an attempt would be made to generalize the results and answer why
the outcomes are occurring. Some of the questions to answer include:
- How does performance change when constraints on the graph type are removed and
when constraints are placed that the algorithm was not designed to handle?
- What is the proportion of resources spent on local processing as compared to message
passing?
- How large of a message and intensive computation to pick the next node, can an
algorithm be while still being more efficient with less message passing?
- Do algorithms perform differently when the minimum number of messages to the
destination is high compared to low?
- How does performance change when there are many nodes other than those on the
shortest path?