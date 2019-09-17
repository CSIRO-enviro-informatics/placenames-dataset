import logging
from flask import Flask
from myldapi import register, myldapi, wfs_source, attr_mapping
from .asgs.meshblocks import Meshblock

app = Flask(__name__)

myapi = myldapi.MyLDApi(app, [
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


