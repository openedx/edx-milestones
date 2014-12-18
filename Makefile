PACKAGE = milestones

# This is the main entry point into the validation  build step
validate: quality


quality:
	pep8 --config=.pep8 $(PACKAGE)
	pylint --rcfile=.pylintrc $(PACKAGE)
