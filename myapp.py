import logging
import os
import sys
from flask import Flask
from asgs.meshblocks import Meshblock
from asgs.sa1 import StatisticalAreaLevel1
from asgs.sa2 import StatisticalAreaLevel2
from asgs.sa3 import StatisticalAreaLevel3
from asgs.sa4 import StatisticalAreaLevel4
from asgs.states import StateOrTerritory
import asgs.config
from myldapi import MyLDApi

app = Flask(__name__)
app.config.from_object(asgs.config)

myapi = MyLDApi(app, asgs.config.DATASET_NAME, asgs.config.DATASET_URI, [
        Meshblock(),
        StatisticalAreaLevel1(),
        StatisticalAreaLevel2(),
        StatisticalAreaLevel3(),
        StatisticalAreaLevel4(),
        StateOrTerritory()
    ])

# run the Flask app
if __name__ == "__main__":
    logging.basicConfig(filename=conf.LOGFILE,
                        level=logging.DEBUG,
                        datefmt="%Y-%m-%d %H:%M:%S",
                        format="%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s")

    # pyldapi.setup(app, conf.APP_DIR, conf.DATA_URI_PREFIX)

    # run the Flask app
    app.run(debug=conf.DEBUG, threaded=True, use_reloader=False)