import logging
import os
import sys
from flask import Flask
from gnaf.address_site import AddressSite
from gnaf.address import Address
import gnaf.config
from myldapi import MyLDApi

app = Flask(__name__, static_folder='gnaf/static', template_folder='gnaf/templates')
app.config.from_object(gnaf.config)

myapi = MyLDApi(app, gnaf.config.DATASET_NAME, gnaf.config.DATASET_URI, [
        Address(),
        AddressSite()
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