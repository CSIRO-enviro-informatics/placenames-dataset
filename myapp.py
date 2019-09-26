import logging
from flask import Flask
from asgs.meshblocks import Meshblock
import asgs.config
from myldapi import MyLDApi

app = Flask(__name__)
app.config.from_object(asgs.config)

myapi = MyLDApi(app, asgs.config.DATASET_NAME, asgs.config.DATASET_URI, [
        Meshblock()
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