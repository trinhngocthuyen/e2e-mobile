bootstrap:
	which npm &> /dev/null || brew install node
	which appium &> /dev/null || npm install -g appium
	(appium driver list --installed 2>&1 | grep xcuitest) || appium driver install xcuitest

install:
	python3 -m pip install virtualenv
	python3 -m virtualenv .venv
	. .venv/bin/activate && pip install -r requirements.txt

demo.build:
	e2e demo build

test.unit:
	. .venv/bin/activate && pytest tests/unit

test.e2e:
	. .venv/bin/activate && pytest tests/e2e

format:
	. .venv/bin/activate && \
		pre-commit run --all-files

doc:
	. .venv/bin/activate && \
		cd docs && \
		rm -rf api/e2e* && \
		sphinx-apidoc \
			--implicit-namespaces \
			--force \
			--module-first \
			--templatedir=_templates/apidoc \
			--output-dir api \
			../src/e2e && \
		rm -rf api/modules.rst && \
		make clean html

doc.up: doc
	python3 -m http.server --directory docs/_build/html
