CXX := g++
CXXFLAGS := -std=c++11 -Wall -lpthread

SRC := controller.cpp node.cpp
TARGET := controller

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)
