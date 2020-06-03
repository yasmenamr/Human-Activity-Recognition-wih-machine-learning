import logging

from model_code_and_Dashboard_code import app

server = app.server

if __name__ == "__main__":
    logger = logging.getLogger('my-logger')
    logger.propagate = False
    app.run_server(debug=True)