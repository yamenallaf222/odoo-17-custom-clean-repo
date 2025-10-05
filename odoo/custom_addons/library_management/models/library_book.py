from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    title = fields.Char(required=True, default='New')
    author = fields.Char(required=True)
    isbn = fields.Text(required=True, help="International Standard Book Number")
    category = fields.Many2one('book.category', string='Book category', ondelete='set null')
    active = fields.Boolean(string='Active', default=True, readonly=True, help='if unchecked, the record will be archived')
    #depreciation controls availability status by rendering the book invaluable if it hits higher or equal to 80 percent thus being Removed
    depreciation = fields.Float(default=0, help='0-100%', readonly=True)
    depreciation_rate = fields.Float(required=True, default=0.0913)
    availability_status = fields.Selection(
        [
            ('available', 'Available'),
            ('borrowed', 'Borrowed'),
            ('reserved', 'Reserved'),
            ('removed', 'Removed')  
        ]
    , default='available', readonly=True)
    acquisition_date = fields.Date(required=True, default=fields.Date.context_today, readonly=True)

    def update_depreciation(self):
        currentDate = fields.Date.context_today()
        daysPassedSinceAcquisition = currentDate - self.acquisition_date
        self.depreciation = min(100, self.depreciation_rate * daysPassedSinceAcquisition)
        library_settings = self.env['library_settings'].search([], limit= 1)
        
        if self.depreciation >= library_settings.book_removal_depreciation_threshold:
            self.availability_status = 'removed'
            self.active = False

    @api.model
    def _create_depreciation_cron(self):
        self.env['ir.cron'].sudo().create({
            'name': 'Update book depreciation',
            'model_id': self.env['ir.model']._get('library.book').id,
            'state': 'code',
            'code': 'model.update_depreciation()',
            'interval_number': 1,
            'interval_type': 'days',
            'numbercall': -1
        })



