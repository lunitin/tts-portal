# Helper file to quickly run docker compose commands

up:
	docker-compose up

down:
	docker-compose down

clean:
	docker-compose down
	docker volume rm tts-portal_tts-db
	docker-compose --build --force-rm
