TESTS = test/test_*.js
TIMEOUT = 10

test:
	mocha -R spec

nose:
	nosetests -v -x
#	$(TESTS)
#	mocha  -R html-cov > coverage.html

.PHONY: test