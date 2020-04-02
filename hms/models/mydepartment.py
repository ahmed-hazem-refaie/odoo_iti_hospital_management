from odoo import  models,fields

class Department (models.Model):
    _name='hms.department'

    name=fields.Char()
    capacity=fields.Integer()
    is_open=fields.Boolean()
    patient_ids=fields.One2many('hms.patient','department_id')





class Doctor(models.Model):
    _name="hms.doctor"
    _rec_name = 'f_name'
    f_name=fields.Char()
    l_name=fields.Char()
    image=fields.Binary()
    patients_ids=fields.Many2many("hms.patient")

