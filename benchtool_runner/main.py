import json
import sys
import urllib.request
from zipfile import ZipFile
import subprocess
import logging
import shutil
import os
import operator

def main():

    result = []

    config_file_name = 'config.json'

    workdir = "./workdir"

    if sys.argv.__len__() >= 2:
        config_file_name = sys.argv[1]

    with open(config_file_name) as config_file:
        config_json = json.load(config_file)

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
                resultData = None

            result.insert(0, (benchtool["name"], int(executionMs), resultData))

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