TEST_DOCKER_TAG := jautero/hopperbot:test

image:
	docker build -t $(TEST_DOCKER_TAG) .

test: image
	docker run -v $(PWD)/test:/app/test ${TEST_DOCKER_TAG} sh /app/test/test.sh