NAME = docker-rm
TEST_DIR = tests


test:
	python3 -m unittest $(TEST_DIR)/dock-tests.py 

run:
	python3 $(NAME).py