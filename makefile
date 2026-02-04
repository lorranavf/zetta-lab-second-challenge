dev-build:
	docker compose -p bee-dev -f deploy/compose/dev.yml build --no-cache

dev-start:
	docker compose -p bee-dev -f deploy/compose/dev.yml up -d

dev-stop:
	docker compose -p bee-dev -f deploy/compose/dev.yml down

dev-restart: dev-stop dev-build dev-start

dev-restart-service:
	docker compose -p bee-dev -f deploy/compose/dev.yml build --no-cache $(SERVICE)
	docker compose -p bee-dev -f deploy/compose/dev.yml restart $(SERVICE)

dev-rm:
	docker compose -p bee-dev -f deploy/compose/dev.yml down --rmi all -v
	make clean

test-build:
	docker compose -p bee-test -f deploy/compose/test.yml build --build-arg INSTALL_TEST=true

test-start:
	docker compose -p bee-test -f deploy/compose/test.yml up --abort-on-container-exit --exit-code-from app-tests

test-rm:
	docker compose -p bee-test -f deploy/compose/test.yml down --rmi all -v

tests:
	docker compose -p bee-test -f deploy/compose/test.yml down --rmi all -v
	docker compose -p bee-test -f deploy/compose/test.yml build --build-arg INSTALL_TEST=true
	docker compose -p bee-test -f deploy/compose/test.yml up --abort-on-container-exit --exit-code-from app-tests
	docker compose -p bee-test -f deploy/compose/test.yml down --rmi all -v

pre-commit-install:
	uv tool install prek
	prek install

pre-commit-run:
	git add .
	prek run --all-files

clean:
	docker system prune -f
