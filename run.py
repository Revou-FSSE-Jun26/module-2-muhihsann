from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug value comes from .env via config (DEBUG=True/False)
    # threaded=True lets the dev server handle concurrent requests
    # (needed for Locust load tests with many simultaneous users)
    app.run(debug=app.config["DEBUG"], threaded=True)