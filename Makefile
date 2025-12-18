BIN_DIR := bin
BIN_FILES := taskA taskB  
all: $(BIN_FILES)

$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

taskA: ./src/tasks/taskA.c | $(BIN_DIR)
	@gcc -fopenmp ./src/tasks/taskA.c  -lpthread -o ./bin/taskA
	@echo "Compiling taskA"

taskB: ./src/tasks/taskB.c | $(BIN_DIR)
	@gcc -fopenmp ./src/tasks/taskB.c  -lpthread -o ./bin/taskB
	@echo "Compiling taskB"

clean:
	@rm -r $(BIN_DIR)