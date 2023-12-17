up:
	docker-compose up -d --build app

down:
	docker-compose rm -fsv

psql:
	psql -p 5434 -U postgres