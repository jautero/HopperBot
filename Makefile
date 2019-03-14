image:
	docker build .

test: image
	docker run -v $PWD/test:/app/test jautero/hopperbot sh /app/test/test.sh