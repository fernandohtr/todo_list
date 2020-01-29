all: create_db
	
create_db:
	sudo -u postgres createdb todo
