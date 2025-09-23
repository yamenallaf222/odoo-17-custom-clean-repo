import json
import math
from urllib.parse import parse_qs
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


def valid_response(data, status, pagination_info=""):
     
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
     
def is_valid_json(json_string):
    try:
        json.loads(json_string)
        return True
    except ValueError:
        return False

class TodoTaskApi(http.Controller):

    def validate_name_field_existence(self, vals):
        if not vals.get('name'):
            return False
        
        return True
    
    @http.route("/v1/todo/<int:todo_task_id>", method=["DELETE"], type="http", auth="none", csrf=False)
    def delete_todo_task(self, todo_task_id):
        try:
            res = request.env['todo.task'].browse(todo_task_id)
            res_id_deleted = res.id
            res_name_deleted = res.name
            res_bool = res.unlink()
            print(res_bool)
            if res_bool:
                return valid_response({
                    "message": "Todo task has been deleted successfully", 
                    "id" : res_id_deleted,
                    "name" : res_name_deleted
                }, status=200)
            else:
                raise Exception("Failed to delete the todo task") 
            
        except Exception as error:
                return invalid_response({
                    "error": error, 
                }, status=400)


        
    # @http.route("/v1/todo/json", method=["POST"], type="json", auth="none", csrf=False)
    # def post_todo_task_json(self):
    #     args = request.httprequest.data.decode()
    #     vals = json.loads(args)
    #     res = request.env['todo.task'].sudo().create(vals)
    #     if res:
    #         return [{
    #             "error": "Todo task has been created successfully"
    #         }]
        
    @http.route("/v1/todo/<int:todo_task_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_todo_task(self, todo_task_id):
        try:
            todo_task_id = request.env['todo.task'].sudo().search([('id', '=', todo_task_id)])
            if not todo_task_id:
                return request.make_json_response({
                    "error": "ID does not exist", 
                }, status=400)
            print(todo_task_id)    
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            print(vals)
            todo_task_id.write(vals)
            return request.make_json_response({
                        "error": "Todo task has been updated successfully", 
                        "id" : todo_task_id.id,
                        "name" : todo_task_id.name,
                        #201 code mean success for creation operation
                    }, status=200)
        except Exception as error:
                return request.make_json_response({
                    "error": error, 
                }, status=400)
        
    @http.route("/v1/todo/<int:todo_task_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_todo_task(self, todo_task_id):
        try:
            todo_task_id = request.env['todo.task'].sudo().search([('id', '=', todo_task_id)])
            if not todo_task_id:
                return invalid_response("There is no Todo task that match this ID", status=400)
                
            return valid_response({
                      "id": todo_task_id.id ,
                      "name" : todo_task_id.name,
                      "ref" : todo_task_id.ref,
                      "date" : todo_task_id.due_date,
                      "description" : todo_task_id.description,
                      "status" : todo_task_id.status,
                      "sub_tasks" : [{
                      "id": timsheet_line_id.id ,
                      "description" : timsheet_line_id.description,
                      "date" : timsheet_line_id.date,
                      "time" : timsheet_line_id.time
                    } for timsheet_line_id in todo_task_id.timesheet_line_ids]
            }, status=200)
            
        except Exception as error:
                return request.make_json_response({
                    "error": error, 
                }, status=400)


    @http.route("/v1/todos", methods=["GET"], type="http", auth="none", csrf=False)
    def get_todo_task_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            print("\n\n")
            print(params)
            todo_task_domain = []
            page = offset = None
            limit = 5
            if params:   
                if(params.get('limit')):
                    limit = int(params.get('limit')[0])

                if(params.get('page')):
                    page = int(params.get('page')[0])

            if page:
                offset = (page * limit) - limit     
            if params.get('status'):
                todo_task_domain += [('status', '=', params.get('status')[0])]
            print(todo_task_domain)

            todo_task_ids = request.env['todo.task'].sudo().search(todo_task_domain, offset=offset, limit=limit, order='id desc')
            todo_task_count = request.env['todo.task'].sudo().search_count(todo_task_domain)

            if not todo_task_ids:
                return request.make_json_response({
                    "error": "There are not records", 
                }, status=400)
                
            return valid_response([{
                      "id": todo_task_id.id ,
                      "name" : todo_task_id.name,
                      "ref" : todo_task_id.ref,
                      "date" : todo_task_id.due_date,
                      "description" : todo_task_id.description,
                      "status" : todo_task_id.status,
                      "sub_tasks" : [{
                      "id": timsheet_line_id.id ,
                      "description" : timsheet_line_id.description,
                      "date" : timsheet_line_id.date,
                      "time" : timsheet_line_id.time
                    } for timsheet_line_id in todo_task_id.timesheet_line_ids]
            } for todo_task_id in todo_task_ids], pagination_info={
                'page' : page if page else 1,
                'limit' : limit,
                'pages' : math.ceil(todo_task_count / limit) if limit else 1,
                'count' : todo_task_count
            }, status=200)
            
        except Exception as error:
                return request.make_json_response({
                    "error": error, 
                }, status=400)
