import json
import math
from urllib.parse import parse_qs
from odoo import http
from odoo.http import request


def valid_response(data, status, pagination_info):
     
    response_body = {  
    'message' : 'successful',   
    'data' : data
    }

    if pagination_info:
        response_body['pagination_info'] = pagination_info
        
    return request.make_json_response(response_body, status=status)

def invalid_response(error, status):
     response_body = {
          'error' : error
     }

     return request.make_json_response(response_body, status=status)
     

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
                return invalid_response("There is no property that match this ID", status=400)
                
            return valid_response({
                      "id": property_id.id ,
                      "name" : property_id.name,
                      "ref" : property_id.ref,
                      "description" : property_id.description,
                      "bedrooms" : property_id.bedrooms
            }, status=200)
            
        except Exception as error:
                return request.make_json_response({
                    "error": error, 
                }, status=400)


    @http.route("/v1/properties", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            print("\n\n")
            print(params)
            property_domain = []
            page = offset = None
            limit = 5
            if params:   
                if(params.get('limit')):
                    limit = int(params.get('limit')[0])

                if(params.get('page')):
                    page = int(params.get('page')[0])

            if page:
                offset = (page * limit) - limit     
            if params.get('state'):
                property_domain += [('state', '=', params.get('state')[0])]
            print(property_domain)

            property_ids = request.env['property'].sudo().search(property_domain, offset=offset, limit=limit, order='id desc')
            property_count = request.env['property'].sudo().search_count(property_domain)

            if not property_ids:
                return request.make_json_response({
                    "error": "There are not records", 
                }, status=400)
                
            return valid_response([{
                      "id": property_id.id ,
                      "name" : property_id.name,
                      "ref" : property_id.ref,
                      "description" : property_id.description,
                      "bedrooms" : property_id.bedrooms
            } for property_id in property_ids], pagination_info={
                'page' : page if page else 1,
                'limit' : limit,
                'pages' : math.ceil(property_count / limit) if limit else 1,
                'count' : property_count
            }, status=200)
            
        except Exception as error:
                return request.make_json_response({
                    "error": error, 
                }, status=400)
