import os
from myldapi import utils
from rdflib import Namespace

APP_TITLE = "GNAF Dataset"
DATASET_NAME = "GNAF Dataset"
DATASET_URI = "http://linked.data.gov.au/dataset/gnaf"

GNAF = Namespace('http://linked.data.gov.au/def/gnaf#')

if os.environ['GNAF_CONNECTION'] is None:
    print('You must set an environment variable for the DB connection called GNAF_CONNECTION')
    exit()
else:
    GNAF_CONNECTION = os.environ['GNAF_CONNECTION']
