import logging
import logging.config
import time
import threading
from datetime import datetime
from datasets import Datasets
from ckan2rdf import CkanMetadata
import json
import os

def task():
	global time
	logging.info("Executing timer with time:"+str(time))
	list_datasets = datasets.getNewDatasets(time)
	for dataset in list_datasets:
		dataset_id = dataset[0]
		dataset_name = dataset[1]
		dataset_title = dataset[2]
		dataset_descp = dataset[5]
		tstamp = dataset[16]
		logging.info("ID:"+dataset_id)
		logging.info("Timestamp:"+datetime.strftime(tstamp,"%Y-%m-%dT%H:%M:%S.%f"))
#		logging.info("TST:"+str(tstamp))
		metadata=datasets.getMetadata(dataset[0])
		metadata["name"]=dataset_name
		metadata["title"]=dataset_title
		metadata["notes"]=dataset_descp
		logging.info(str(metadata))
		ckan_module = CkanMetadata(dataset_name)
		result = ckan_module.transformToRdf(metadata)
		logging.debug(result)
		filerdf = open(dataset_name+".ttl","w")
		filerdf.write(result)
		filerdf.close()
                logging.info("Generated rdf file:"+dataset_name+".ttl")
		time=datetime.strftime(tstamp,"%Y-%m-%dT%H:%M:%S.%fZ")
        fileid.seek(0)
#        fileid.write(datetime.strftime(time,"%Y-%m-%dT%H:%M:%S"))
	fileid.write(time)
        
        logging.info("Waiting for next execution")

        threading.Timer(60, task).start()

logging.config.fileConfig('config/logging.cfg') #logfile config
logging.debug("DEBUG MODE")
logging.info("INFO MODE")

time = datetime.utcnow()
pidfile = "timestamp"
fileid = open(pidfile,"r+")

if os.path.exists(pidfile):
    time = fileid.read()

logging.info("Get last datasets from "+time)

#time = datetime.datetime.utcnow()
#time = time - datetime.timedelta(days=2)

datasets = Datasets()

ckan_module = CkanMetadata("lens")

task()
