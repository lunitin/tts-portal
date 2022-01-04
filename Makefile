up:
	docker-compose up -d
	watchman-make -p 'docroot/**/*.py' 'docroot/templates/**' -s 1 --run 'touch docroot/uwsgi-reload'

down:
	docker-compose down

clean:
	docker-compose down
	docker volume rm tts-portal_tts-db
	docker-compose --build --force-rm
