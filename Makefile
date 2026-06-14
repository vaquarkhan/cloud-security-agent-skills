.PHONY: validate validate-sme test demo install sync-manifest pre-commit plugin-sync

PYTHON ?= python

validate:
	$(PYTHON) scripts/validate-skills.py
	$(PYTHON) scripts/validate-assets.py
	$(PYTHON) scripts/validate-plugin-manifest.py
	$(PYTHON) scripts/sync-install-manifest.py
	$(PYTHON) evals/benchmark/skill_routing_benchmark.py

validate-sme:
	$(PYTHON) scripts/validate-skills.py
	@test -f registry/provenance.yaml

test:
	$(PYTHON) -m pytest tests/unit/ -v

demo:
	$(PYTHON) examples/mock-posture-check/run_posture_check.py

install:
	$(PYTHON) -m pip install -e ".[dev]"

sync-manifest:
	$(PYTHON) scripts/sync-install-manifest.py

pre-commit:
	pre-commit run --all-files

plugin-sync:
	$(PYTHON) scripts/sync-install-manifest.py
	cp registry/install-manifest.json vscode-extension/install-manifest.json
	cp registry/install-manifest.json jetbrains-plugin/src/main/resources/install-manifest.json
