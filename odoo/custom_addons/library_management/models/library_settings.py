from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibrarySettings(models.Model):
    _name = 'library.settings'

    
    @api.model
    def create(self, vals):
        if self.search([], limit= 1):
            raise ValidationError('Only one record is allowed for this model')
        super().create(vals)