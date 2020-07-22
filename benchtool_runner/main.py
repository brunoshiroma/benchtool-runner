import json
import sys
import urllib.request
from zipfile import ZipFile
import subprocess
import logging
import shutil
import os
import operator
from googleapiclient.discovery import build
import pickle
import codecs
from google.auth.transport.requests import Request
import re
from datetime import datetime

def send_to_sheet(bench, ms, result, success, cpu_info, config, date, service):
    if result != None:
                result = result[:min(len(result), 10)]

    str_date = date.strftime('%Y/%m/%d %H:%M:%S')

    if os.environ['SEND_TO_SHEET'] == 'true' :
        values = [
                    [
                        os.environ['RUNNER_ENV'], bench, ms, success, cpu_info, str_date, config['nElement'], result
                    ]
                ]
        body = {
            'values': values
        }
        sheet_result = service.spreadsheets().values().append(valueInputOption='RAW',range='results!A2:H',spreadsheetId=os.environ['GOOGLE_SHEET_ID'], body=body).execute()

def main():

    result = []

    config_file_name = 'config.json'

    workdir = "./workdir"

    if sys.argv.__len__() >= 2:
        config_file_name = sys.argv[1]

    with open(config_file_name) as config_file:
        config_json = json.load(config_file)

        #current date
        now = datetime.now()

        #google sheets    
        if os.environ['SEND_TO_SHEET'] == 'true' :
            creds = pickle.loads(codecs.decode(os.environ['GOOGLE_TOKEN'].encode(), 'base64'))
            creds.refresh(Request())
            service = build('sheets', 'v4', credentials=creds)
        else:
            service = None

        #cpu info
        cpu_info = "UNKNOWN"
        command = "cat /proc/cpuinfo"
        all_info = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout,stderr = all_info.communicate()
        rawResult = stdout.decode('ascii')
        for line in rawResult.split("\n"):
            if "model name" in line:
                cpu_info =  re.sub( ".*model name.*:", "", line,1)

        if config_json["loggingLevel"] is not None:
            logging.basicConfig(level=config_json["loggingLevel"])
        else:
            logging.basicConfig(level=logging.INFO)

        executionCount = config_json["executionCount"]

        logging.debug(config_json["version"])
        logging.debug("Execution count {count}".format(count=executionCount))

        pullCommand = "docker pull {image}"
        runCommand = "docker run {image} {benchtype} {nelement} {executionCount}"

        for benchtool in config_json["benchtools"]:
            #pull first
            commandLine = pullCommand.format(image=benchtool["image"])
            logging.debug("Executing PULL {commands}".format(commands=commandLine))
            pull = subprocess.Popen(commandLine.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout,stderr = pull.communicate()

            #exec the command..
            commandLine = runCommand.format(image=benchtool["image"], executionCount=executionCount, nelement=config_json["nElement"], benchtype=config_json["benchType"])
            logging.debug("Executing {commands}".format(commands=commandLine))
            bench = subprocess.Popen(commandLine.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout,stderr = bench.communicate()
            rawResult = stdout.decode('ascii')

            resultParts = rawResult.split(" ")

            executionMs = resultParts[0].strip()
            resultData = resultParts[1].strip()

            if resultData != config_json["validResult"]:
                logging.warning("Result {resultData} from {name} is not valid, will be ignored".format(resultData=resultData, name=benchtool["name"]))
                send_to_sheet(benchtool["name"], int(executionMs), resultData, False, cpu_info, config_json, now, service)
                resultData = None

            result.insert(0, (benchtool["name"], int(executionMs), resultData))
            send_to_sheet(benchtool["name"], int(executionMs), resultData, True, cpu_info, config_json, now, service)
            
            resultTrunc = ""

            if resultData != None:
                resultTrunc = resultData[:min(len(resultData), 10)]

            logging.info("Result from {benchname} execution time {executionMs}, partial result data {resultData}".format(benchname=benchtool["name"], executionMs=executionMs, resultData=resultTrunc) )
            if stderr is not None:
                logging.warning(stderr)

        #sort result by execution ms
        result.sort(key = operator.itemgetter(1))

        for singleResult in result :
            logging.info("RESULT FROM {name} {executionMs}ms".format(name=singleResult[0], executionMs=singleResult[1]) )
        
        logging.info("Faster bench {name} with execution time of {executionMs}ms".format(name=result[0][0], executionMs=result[0][1]))

if __name__ == "__main__" :
    main()