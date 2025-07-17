import json
from odoo import http
from odoo.http import request

class PropertyApi(http.Controller):

    def validate_name_field_existence(self, vals):
        if not vals.get('name'):
            return False
   

         

    @http.route("/v1/property", method=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not self.validate_name_field_existence(vals):
            return request.make_json_response({
                "message": "Name is required!", 
            }, status=400) 
        try:
            res = request.env['property'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    "message": "Property has been created successfully", 
                    "id" : res.id,
                    "name" : res.name,
                    #201 code mean success for creation operation
                }, status=201)
        except Exception as error:
                return request.make_json_response({
                    "message": error, 
                }, status=400)

        
    @http.route("/v1/property/json", method=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['property'].sudo().create(vals)
        if res:
            return [{
                "message": "Property has been created successfully"
            }]
        



