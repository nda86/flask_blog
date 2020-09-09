def date_format(d):
	# 2020-06-13 00:00:00
	return d.strftime("%d.%m.%Y")


def create_filters(app):
	app.jinja_env.filters["date_format"] = date_format
