from typing import Dict, List

from providers.aws import awsKeyProvider
from providers.s3 import s3Provider
from providers.plausible import plausibleProvider

import toml

from flask import Flask, make_response, Response
from flask_cors import CORS

def create_app():
    """
    Creates an instance of the Flask app, and associated configuration and blueprints registration for specific routes. 

    Configuration includes

    - Relevant secrets stored in the config.toml file
    - Storing in configuration a set of credentials for AWS (decided upon by the environment of the application e.g. development, live)
    
    Returns:
            A configured instance of the Flask app

    """
    app = Flask(__name__)

    app.config.from_file('config.toml', toml.load)

    app.config['AWS_CONFIG'] = {
        'aws_access_key_id':app.config['AWS_ACCESS_KEY_ID'],
        'aws_access_secret':app.config['AWS_ACCESS_SECRET'],
        'aws_region':app.config['AWS_REGION'],
        's3_bucket':app.config['S3_BUCKET'] 
    }

    return app


app = create_app()
CORS(app)



def fetch_coordinates(mhc_class, pdb_code, assembly_id, coordinates_type, solvent, format):
    if coordinates_type == 'abd':
        coordinates_type = 'antigen_binding_domains'
    elif coordinates_type == 'alpha':
        coordinates_type = 'alpha_chains'
    s3 = s3Provider(app.config['AWS_CONFIG'])
    key = awsKeyProvider().coordinates_file_key(mhc_class, pdb_code, assembly_id, coordinates_type, solvent, format)
    coordinates, success, error = s3.get(key, 'txt')
    return coordinates, success, error




@app.route('/structures/view/<string:mhc_class>/<string:solvent>/<string:pdb_code>_<string:assembly_id>_<string:coordinates_type>.<string:format>')
def coordinates_view(mhc_class, solvent, pdb_code, assembly_id, coordinates_type, format):
    coordinates, success, error = fetch_coordinates(mhc_class, pdb_code, assembly_id, coordinates_type, solvent, format)
    if success:
        response = make_response(coordinates, 200)
        response.mimetype = "text/plain"
    else:
        response = make_response('The requested file could not be found', 404)
        response.mimetype = "text/plain"
    return response



@app.route('/structures/<string:action>/<string:mhc_class>/<string:solvent>/<string:pdb_code>_<string:assembly_id>_<string:coordinates_type>.<string:format>')
def coordinates_download(action, mhc_class, solvent, pdb_code, assembly_id, coordinates_type, format):
    coordinates, success, error = fetch_coordinates(mhc_class, pdb_code, assembly_id, coordinates_type, solvent, format)
    if success:
        file_name = f'{pdb_code}_{assembly_id}_{coordinates_type}.{format}'
        plausible = plausibleProvider('histo.fyi')
        # TODO make an action which will distinguish coordinate downloads (action = download) and coordinates loaded into PyMol (action = load)
        plausible.structure_download(file_name, coordinates_type, pdb_code)
        return Response(coordinates,
                        mimetype="text/plain",
                        headers={"Content-disposition": f"attachment; filename={file_name}"})

    else:
        response = make_response('The requested file could not be found', 404)
        response.mimetype = "text/plain"
        return response




