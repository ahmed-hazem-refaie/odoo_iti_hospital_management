

from  odoo import  models,fields
class Hms (models.Model):
    _name = 'hms.hms'
    f_name=fields.Char()
    l_name=fields.Char()
    BD=fields.Datetime()
    age=fields.Integer()
    CR=fields.Float()
    x = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready for next stage'),
        ('blocked', 'Blocked')], string='State')
    img=fields.Binary()