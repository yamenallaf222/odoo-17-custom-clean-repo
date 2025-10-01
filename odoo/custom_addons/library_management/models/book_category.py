from odoo import models, fields


class BookCategory(models.Model):
    _name = 'book.category'
    _description = 'Book Category'

    name = fields.Char(required=True, default='New')
    description = fields.Text()
    parent_id = fields.Many2one('book.category', string='Parent category', ondelete='set null')
    child_ids = fields.One2many('book.category', inverse_name='parent_id', string= 'Child categories')
    active = fields.Boolean(string='Active', default=True,readonly=True, help='if unchecked, the record will be archived')