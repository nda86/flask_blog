from flask_restful import fields


get_post_field = {
	"title": fields.String,
	"tags": fields.List(fields.Nested({"title": fields.String()})),
	"created_at": fields.DateTime
}