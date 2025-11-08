
PYTHON_VERSION=python3.13
PYTHON=${PYTHON_VERSION}
VENV_PYTHON=.venv/bin/python

venv:
	uv venv .venv --clear

clean_cache:
	find . -type d -name "*_cache" -exec rm -rf {} +
	
clean: clean_cache
	rm -rf .venv

setup: venv
	uv pip install --upgrade pip
	uv pip install -e .

app:
	${PYTHON} -m streamlit run dashboard/main.py