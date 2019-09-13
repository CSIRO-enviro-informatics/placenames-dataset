import logging
from flask import Flask
from myldapi import register, myldapi

# app = Flask(__name__, template_folder=conf.TEMPLATES_DIR, static_folder=conf.STATIC_DIR)
app = Flask(__name__)

meshblock = register.Register(name="Meshblock", 
                                      path="meshblock", 
                                      type_uri="http://linked.data.gov.au/def/asgs#MeshBlock",
                                      base_uri="http://linked.data.gov.au/dataset/asgs2016/meshblock/")

# group_one = myldapi.object_group.ObjectGroup("http://linkeddata.gov.ay/dataset/asgs")
# group_one.add_creators()

myapi = myldapi.MyLDApi(app, [meshblock]) #, views, formats)

# run the Flask app
if __name__ == '__main__':
    logging.basicConfig(filename=conf.LOGFILE,
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s')

    # pyldapi.setup(app, conf.APP_DIR, conf.DATA_URI_PREFIX)

    # run the Flask app
    app.run(debug=conf.DEBUG, threaded=True, use_reloader=False)

