from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibrarySettings(models.Model):
    _name = 'library.settings'

    book_removal_depreciation_threshold = fields.Integer(required=True, default=85)
    
    @api.model
    def create(self, vals):
        if self.search([], limit= 1):
            raise ValidationError('Only one record is allowed for this model')
        super(self).create(vals)