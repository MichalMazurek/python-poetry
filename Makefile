args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`


install:
	poetry install

all:
	poetry run python3 dockerfiles.py clean
	poetry run python3 dockerfiles.py make $(call args,defaultstring)
	poetry run python3 dockerfiles.py build

push:
	poetry run python3 dockerfiles.py push $(call args,defaultstring)