.PHONY: docs

init:
	pip install -r requirements.txt

test:
	# This runs all of the tests. To run an individual test, run py.test with
	# the -k flag, like "py.test -k test_path_is_not_double_encoded"
	#

coverage:
	#

ci: init
	#


deps: project_root

project_root:
	git clone git@github.com:chao-han/project_root.git && rm -fr project_sub/packages/yottaautil && 	mv project_root/yottaautil project_sub/packages/ && rm -fr project_root

