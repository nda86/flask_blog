import os

from webapp import create_app


app = create_app()

if __name__ == "__main__":
	app.run(ssl_context=("cert.pem", "key.pem"), port=5005)
