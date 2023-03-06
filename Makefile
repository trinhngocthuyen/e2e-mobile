install:
	python3 -m pip install virtualenv
	python3 -m virtualenv .venv
	. .venv/bin/activate && pip install -r requirements.txt

test: test.py test.integration.ios

test.py:
	. .venv/bin/activate && pytest

test.integration.ios:
	. .venv/bin/activate && sh scripts/integration_test_ios.sh

format:
	. .venv/bin/activate && \
		pre-commit run --all-files

doc:
	. .venv/bin/activate && \
		cd docs && \
		rm -rf api/cicd* && \
		sphinx-apidoc \
			--implicit-namespaces \
			--force \
			--module-first \
			--templatedir=_templates/apidoc \
			--output-dir api \
			../src/cicd && \
		rm -rf api/modules.rst && \
		make clean html
