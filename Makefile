up:
	docker-compose up &
	watchman-make -p 'docroot/**/*.py' 'docroot/templates/**' -s 1 --run 'touch docroot/uwsgi.ini'

down:
	docker-compose down

clean:
	docker-compose down
	docker volume rm tts-portal_tts-db
	docker-compose --build --force-rm
