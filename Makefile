ifneq (,$(wildcard ./.env))
    include .env
    export
endif

#https://stackoverflow.com/a/46188210
venv: venv/touchfile

venv/touchfile: requirements.txt
	test -d .venv || python3 -m venv .venv
	. .venv/bin/activate; pip3 install -Ur requirements.txt
	touch .venv/touchfile

token:
	. .venv/bin/activate; python3 benchtool_runner/generate_token.py

run:
	. .venv/bin/activate; python3 benchtool_runner/main.py config_sample.json

run-without-publish:
	. .venv/bin/activate; SEND_TO_SHEET=false python3 benchtool_runner/main.py config_sample.json 