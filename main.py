from webapp import create_app


app = create_app()

# запускаем сервер flask с использованием тестовых сертифкатов ssl(это нужно для проверки работы OAuth)
if __name__ == "__main__":
	app.run(ssl_context=("test_cert.pem", "test_key.pem"), port=5005)
