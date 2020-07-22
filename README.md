## Runner for benchtool

[![Github](https://github.com/brunoshiroma/benchtool-runner/workflows/Python%20application/badge.svg)](https://github.com/brunoshiroma/benchtool-runner)
[![Gitlab](https://gitlab.com/brunoshiroma/benchtool-runner/badges/master/pipeline.svg)](https://gitlab.com/brunoshiroma/benchtool-runner)
[![CircleCI](https://circleci.com/gh/brunoshiroma/benchtool-runner.svg?style=svg)](https://circleci.com/gh/brunoshiroma/benchtool-runner)
[![Build Status](https://brunoshiroma.visualstudio.com/benchtool-runner/_apis/build/status/brunoshiroma.benchtool-runner?branchName=master)](https://brunoshiroma.visualstudio.com/benchtool-runner/)

Run with command :
```
python3 benchtool_runner/main.py [config_sample.json]
```

This script, uses by default the config with name config.json

#### Projects from benchtool:

 * https://github.com/brunoshiroma/benchtool_julia
 * https://github.com/brunoshiroma/benchtool-java
 * https://github.com/brunoshiroma/benchtool-dotnetcore
 * https://github.com/brunoshiroma/benchtool-rust
 * https://github.com/brunoshiroma/benchtool-cpp

#### Sheet with results:
[Google Spreadsheets](https://docs.google.com/spreadsheets/d/1unaPbZy-9vFtzbWeRxfC4IzcuGVExz6aO2EXjePUhro/edit?usp=sharing)

#### Env Vars to send to Sheet
```
GOOGLE_TOKEN=[TOKEN_GENERATED_IN_BASE64]
GOOGLE_SHEET_ID=[SHEET_ID]
RUNNER_ENV=local
SEND_TO_SHEET=true
```
