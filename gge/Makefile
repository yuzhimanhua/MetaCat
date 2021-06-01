CC = g++
CPPFLAGS = -std=c++11 -lpthread -lgsl -lgslcblas -O3
OBJS = line

all: $(OBJS)

$(OBJS):
	$(CC) $@.cpp $(CPPFLAGS) -o $@

clean:
	rm $(OBJS)