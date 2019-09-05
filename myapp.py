import logging
from flask import Flask
import myldapi

app = Flask(__name__, template_folder=conf.TEMPLATES_DIR, static_folder=conf.STATIC_DIR)

placename = myldapi.rdf_object.ObjectCreator("PlaceName", "")
juridiction = myldapi.rdf_object.ObjectCreator("Jurisdiction", "")
gazetteer = myldapi.rdf_object.ObjectCreator("Gazetteer", "")

objects = [placename, juridiction, gazetteer]

pnapi = myldapi.myldapi.MyLDApi(app, objects, views, formats)

# run the Flask app
if __name__ == '__main__':
    logging.basicConfig(filename=conf.LOGFILE,
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s')

    # pyldapi.setup(app, conf.APP_DIR, conf.DATA_URI_PREFIX)

    # run the Flask app
    app.run(debug=conf.DEBUG, threaded=True, use_reloader=False)

