# Coordinate-server - microservice to serve coordinate files for histo.fy

A Flask/Zappa based microservice to serve coordinate files using AWS Lambda with S3 as storage

## Endpoints

### View

This endpoint is used by various visualisations on the website and is not logged in Plausible

### Download/Load

This endpoint is used by PyMol integrations (load) and downloads from the website and is logged in Plausible

