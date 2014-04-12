
ALL: ;

install:
	python setup.py install

test.js:
	mocha -R spec

test.py:
	py.test test

benchmark:
	python benchmark/benchmark3.py

nose:
	nosetests -v -x

.PHONY: test.js  test.py  benchmark