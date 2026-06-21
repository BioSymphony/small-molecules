.PHONY: help release-check audit style py-compile markdown-links clean-runtime

help:
	@echo "BioSymphony Small Molecules public commands"
	@echo "  make release-check    Run local public-release checks"
	@echo "  make audit            Scan for local paths, secrets, and oversized files"
	@echo "  make style            Check front-door public-doc style"
	@echo "  make py-compile       Compile public Python scripts"
	@echo "  make markdown-links   Check local markdown links"

release-check: py-compile markdown-links audit

audit:
	python3 scripts/public_audit.py .

style:
	python3 scripts/public_audit.py . --style-only

py-compile:
	python3 -m py_compile demos/kras-glue/*.py demos/kras-glue/ddg/pod/*.py scripts/public_audit.py

markdown-links:
	python3 scripts/public_audit.py . --links-only

clean-runtime:
	rm -rf .runtime
