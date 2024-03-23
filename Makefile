.PHONY: build

pip = pip
python = python

build:
	${python} -m build

build-system-packages:
	${python} -m build --wheel --no-isolation

install:
	${pip} install . -U

install-editable:
	${pip} install -e . --config-settings editable_mode=compat -U

test:
	ruff check --target-version=py38 .