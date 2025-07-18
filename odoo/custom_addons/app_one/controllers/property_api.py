import json
from odoo import http
from odoo.http import request

class PropertyApi(http.Controller):

    def validate_name_field_existence(self, vals):
        if not vals.get('name'):
            return False
        
        return True
   

         

    @http.route("/v1/property", method=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not self.validate_name_field_existence(vals):
            return request.make_json_response({
                "error": "Name is required!", 
            }, status=400) 
        try:
            res = request.env['property'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    "error": "Property has been created successfully", 
                    "id" : res.id,
                    "name" : res.name,
                    #201 code mean success for creation operation
                }, status=201)
        except Exception as error:
                return request.make_json_response({
                    "error": error, 
                }, status=400)

        
    @http.route("/v1/property/json", method=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['property'].sudo().create(vals)
        if res:
            return [{
                "error": "Property has been created successfully"
            }]
        
    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response({
                    "error": "ID does not exist", 
                }, status=400)
            print(property_id)    
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            print(vals)
            property_id.write(vals)
            print(property_id.garden_area)
            return request.make_json_response({
                        "error": "Property has been updated successfully", 
                        "id" : property_id.id,
                        "name" : property_id.name,
                        #201 code mean success for creation operation
                    }, status=200)
        except Exception as error:
                return request.make_json_response({
                    "error": error, 
                }, status=400)
        
    @http.route("/v1/property/<int:property_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response({
                    "error": "There is no property that match this ID", 
                }, status=400)
                
            return request.make_json_response({
                      "id": property_id.id ,
                      "name" : property_id.name,
                      "ref" : property_id.ref,
                      "description" : property_id.description,
                      "bedrooms" : property_id.bedrooms
            })
            
        except Exception as error:
                return request.make_json_response({
                    "error": error, 
                }, status=400)

