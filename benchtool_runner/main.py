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

def send_to_sheet(results, cpu_info, config, date, service):
    
    if os.environ['SEND_TO_SHEET'] == 'true' :

        str_date = date.strftime('%Y/%m/%d %H:%M:%S')
        values = []

        #truncate result
        for result in results:
            trunc_result = ""
            if result[2] != None:
                trunc_result = result[2][:min(len(result), 10)]
        
            values.insert(0, [os.environ['RUNNER_ENV'], result[0], result[1], result[3], cpu_info, str_date, config['nElement'], trunc_result])

        body = {
            'values': values
        }
        sheet_result = service.spreadsheets().values().append(valueInputOption='RAW',range='results!A2:H',spreadsheetId=os.environ['GOOGLE_SHEET_ID'], body=body).execute()
        logging.debug(sheet_result)


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
        command = "lscpu"
        all_info = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout,stderr = all_info.communicate()
        rawResult = stdout.decode('ascii')
        for line in rawResult.split("\n"):
            if re.search("model name", line, re.IGNORECASE):
                cpu_info =  re.sub( ".*model name.*:", "", line,count=1, flags=re.I).strip()

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
                result.insert(0, (benchtool["name"], int(executionMs), resultData, False))
            else:
                result.insert(0, (benchtool["name"], int(executionMs), resultData, True))
                
                resultTrunc = ""

                if resultData != None:
                    resultTrunc = resultData[:min(len(resultData), 10)]

                logging.info("Result from {benchname} execution time {executionMs}, partial result data {resultData}".format(benchname=benchtool["name"], executionMs=executionMs, resultData=resultTrunc) )
                if stderr is not None:
                    logging.warning(stderr)

        for singleResult in result :
            logging.info("RESULT FROM {name} {executionMs}ms, success {success}".format(name=singleResult[0], executionMs=singleResult[1], success=singleResult[3]) )
        
        #sort result by execution ms
        success_results = list(filter(lambda r : r[3], result))
        success_results.sort(key = operator.itemgetter(1))

        logging.info("Faster bench {name} with execution time of {executionMs}ms".format(name=success_results[0][0], executionMs=success_results[0][1]))
        send_to_sheet(result, cpu_info, config_json, now, service)

if __name__ == "__main__" :
    main()