BIN_DIR := bin
BIN_FILES := taskA taskB  
all: $(BIN_FILES)

$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

taskA: taskA.c | $(BIN_DIR)
#@gcc -fopenmp ./taskA.c  -lpthread -o ./bin/taskA
	@gcc-15 -fopenmp ./taskA.c  -lpthread -o ./bin/taskA
	@echo "Compiling taskA"

taskB: taskB.c | $(BIN_DIR)
#@gcc -fopenmp ./taskA.c  -lpthread -o ./bin/taskB
	@gcc-15 -fopenmp ./taskB.c  -lpthread -o ./bin/taskB
	@echo "Compiling taskB"

clean:
	@rm -r $(BIN_DIR)