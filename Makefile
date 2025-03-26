GLUE_PLUGINS=$(notdir $(wildcard pulp-glue-console/pulp_glue/*))
CLI_PLUGINS=$(notdir $(wildcard pulpcore/cli/*))

info:
	@echo Pulp glue
	@echo plugins: $(GLUE_PLUGINS)
	@echo Pulp CLI
	@echo plugins: $(CLI_PLUGINS)

build:
	cd pulp-glue-console; pyproject-build -n
	pyproject-build -n

black: format

format:
	isort .
	cd pulp-glue-console; isort .
	black .

lint:
	find tests .ci -name '*.sh' -print0 | xargs -0 shellcheck -x
	isort -c --diff .
	cd pulp-glue-console; isort -c --diff .
	black --diff --check .
	flake8
	python3 .ci/scripts/check_cli_dependencies.py
	python3 .ci/scripts/check_click_for_mypy.py
	MYPYPATH=pulp-glue-console mypy
	cd pulp-glue-console; mypy
	@echo "🙊 Code 🙈 LGTM 🙉 !"

tests/cli.toml:
	cp $@.example $@
	@echo "In order to configure the tests to talk to your test server, you might need to edit $@ ."

test: | tests/cli.toml
	python3 -m pytest -v tests pulp-glue-console/tests

livetest: | tests/cli.toml
	python3 -m pytest -v tests pulp-glue-console/tests -m live

unittest:
	python3 -m pytest -v tests pulp-glue-console/tests -m "not live"

unittest_glue:
	python3 -m pytest -v pulp-glue-console/tests -m "not live"
.PHONY: build info black lint test