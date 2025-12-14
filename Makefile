BIN_DIR := bin
BIN_FILES := taskB  
all: $(BIN_FILES)

$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

taskB: taskB.c | $(BIN_DIR)
	@gcc -fopenmp ./taskB.c  -lpthread -o ./bin/taskB
	@echo "Compiling taskB"

clean:
	@rm -r $(BIN_DIR)