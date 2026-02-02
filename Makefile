dev-build:
	docker compose -p bee-dev -f deploy/compose/dev.yml build --no-cache

dev-start:
	docker compose -p bee-dev -f deploy/compose/dev.yml up -d

dev-stop:
	docker compose -p bee-dev -f deploy/compose/dev.yml down

dev-restart: dev-stop dev-build dev-start

dev-rm:
	docker compose -p bee-dev -f deploy/compose/dev.yml down --rmi all -v 

clean:
	docker system prune -f

