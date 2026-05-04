PYTHON = .venv/bin/python3

.venv/.installed:
	python3 -m venv .venv
	.venv/bin/pip install --quiet qiskit qiskit-ibm-runtime qiskit-aer matplotlib cirq
	touch .venv/.installed

ex00: .venv/.installed
	$(PYTHON) ex00/ex00.py

ex01: .venv/.installed
	$(PYTHON) ex01/ex01.py

ex02: .venv/.installed
	set -a && . $(CURDIR)/.env && set +a && $(PYTHON) ex02/ex02.py

ex03: .venv/.installed
	$(PYTHON) ex03/ex03.py

ex04: .venv/.installed
	$(PYTHON) ex04/ex04.py

clean:
	rm -rf .venv

.PHONY: ex00 ex01 ex02 ex03 ex04 clean
