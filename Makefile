.PHONY: clean install build serve

clean:
	rm -fr _builds

install:
	bundle install
	pip install -r requirements.txt --upgrade

build:
	python build.py

serve:
	cd _builds/site && python -m http.server
