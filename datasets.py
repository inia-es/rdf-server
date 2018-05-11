import os
import psycopg2
import logging
import logging.config
import datetime

host = os.getenv('DB_HOST', 'localhost')
dbname = os.getenv('DB_NAME', 'name')
user = os.getenv('DB_USER', 'user')
password = os.getenv('DB_PASSWORD','password')

conn = psycopg2.connect("dbname='"+dbname+"' host='"+host+"' user='"+user+"' password='"+password+"'")
cursor = conn.cursor()

logging.config.fileConfig('config/logging.cfg')

class Datasets:
	def __init__(self):
                connection_parameters = "dbname='"+dbname+"' host='"+host+"' user='"+user+"' password='"+password+"'"
                self.conn = psycopg2.connect(connection_parameters)
		self.cursor = self.conn.cursor()

	def getNewDatasets(self,tstamp):
		logging.info("Get datasets from "+tstamp)
		sql_query = "SELECT * FROM package WHERE metadata_modified>'"+tstamp+"' ORDER BY metadata_modified ASC"
		cursor.execute(sql_query)
		rows = cursor.fetchall()
		list_datasets = []
		for row in rows:
			logging.info(row)
			list_datasets.append(row)
		return list_datasets
	def getMetadata(self,name):
		sql_query = "SELECT key,value FROM package_extra WHERE package_id='"+name+"'"
		cursor.execute(sql_query)
		rows = cursor.fetchall()
		list_metadata = {}
		for row in rows:
			list_metadata[row[0]] = row[1]
		return list_metadata
	def closeDatasets():
		cursor.close()
		conn.close()
