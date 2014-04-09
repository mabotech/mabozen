
ALL: ;

test:
	mocha -R spec
	py.test

benchmark:
	python benchmark/benchmark3.py

nose:
	nosetests -v -x

.PHONY: test benchmark