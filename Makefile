
setup_version := `python async_notifications/__init__.py`
current_path := `pwd`
clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm celerybeat-schedule.db


clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	pycodestyle --max-line-length=88 async_notifications
	pycodestyle --max-line-length=88 demo

test:
	python manage.py test

docs:
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	sphinx-build -b linkcheck ./docs/source docs/build/
	sphinx-build -b html ./docs/source docs/build/

version:
   $echo $(setup_version)

release:
	git tag -a "v$(setup_version)" -m "Bump version $(setup_version)"
	git push origin "v$(setup_version)"
	twine upload -s dist/*

sdist: clean
	python manage.py makemigrations
	django-admin compilemessages -l es
	python3 -m build
	ls -l dist

messages:
	python manage.py makemessages --all --no-location --no-obsolete
	django-admin makemessages -d djangojs -l es  --ignore *.min.js --no-location --no-obsolete

trans:
	django-admin compilemessages --locale es
