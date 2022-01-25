# Helper file to quickly run docker compose commands

up:
	docker-compose up

watch:
	watchman-make -p 'docroot/**/*.py' 'docroot/**/*.html' 'docroot/**/*.css' 'docroot/**/*.js' -s 1 --run 'touch docroot/uwsgi.ini'

down:
	docker-compose down

clean:
	docker-compose down
	docker volume rm tts-portal_tts-db
	docker-compose --build --force-rm
