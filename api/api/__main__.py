from api import create_app

if __name__ == "__main__":
    app = create_app()
    try:
        app.run(host="127.0.0.1", port=8080)
    finally:
        pass
