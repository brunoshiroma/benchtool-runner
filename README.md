## Runner for benchtool

[![Github](https://github.com/brunoshiroma/benchtool-runner/workflows/Python%20application/badge.svg)](https://github.com/brunoshiroma/benchtool-runner)
[![Gitlab](https://gitlab.com/brunoshiroma/benchtool-runner/badges/master/pipeline.svg)](https://gitlab.com/brunoshiroma/benchtool-runner)
[![CircleCI](https://circleci.com/gh/brunoshiroma/benchtool-runner.svg?style=svg)](https://circleci.com/gh/brunoshiroma/benchtool-runner)
[![Build Status](https://brunoshiroma.visualstudio.com/benchtool-runner/_apis/build/status/brunoshiroma.benchtool-runner?branchName=master)](https://brunoshiroma.visualstudio.com/benchtool-runner/)
[![Build Status](https://travis-ci.com/brunoshiroma/benchtool-runner.svg?branch=master)](https://travis-ci.com/brunoshiroma/benchtool-runner)
 [![Run Status](https://api.shippable.com/projects/5ef34dffaf951100075e6924/badge?branch=master)]() 


Run with command :
```bash
# With env alread set
python3 benchtool_runner/main.py [config_sample.json]

# Without envs
GOOGLE_TOKEN=[GENERATED_TOKEN]GOOGLE_SHEET_ID=[SHEET_ID]
RUNNER_ENV=[ENV OF RUNNER] SEND_TO_SHEET=true|false python benchtool_runner/main.py [config_sample.json]

```

This script, uses by default the config with name config.json

#### Projects from benchtool:

 * https://github.com/brunoshiroma/benchtool_julia
 * https://github.com/brunoshiroma/benchtool-java
 * https://github.com/brunoshiroma/benchtool-dotnetcore
 * https://github.com/brunoshiroma/benchtool-rust
 * https://github.com/brunoshiroma/benchtool-cpp
 * https://github.com/brunoshiroma/benchtool-android

#### Sheet with results:
[Google Spreadsheets](https://docs.google.com/spreadsheets/d/1unaPbZy-9vFtzbWeRxfC4IzcuGVExz6aO2EXjePUhro/edit?usp=sharing)

#### Env Vars to send to Sheet
```
GOOGLE_TOKEN=[TOKEN_GENERATED_IN_BASE64]
GOOGLE_SHEET_ID=[SHEET_ID]
RUNNER_ENV=local
SEND_TO_SHEET=true
```
#### Generate GOOGLE_TOKEN
```
#SHEET_ID you can get it from the google sheet URL ou share
python3 benchtool_runner/generate_token.py [SHEET_ID]
```
It will open a browser to ask for permissions and then output the generated token  
You will need a **credentials.json**, in same dictory of execution, [Google documentation](https://developers.google.com/docs/api/quickstart/python) for Python
