from odoo import  models,fields,api
from odoo.exceptions import ValidationError,UserError
import re
from datetime import  date
class Hms_patients (models.Model):
    _name = 'hms.patient'
    _rec_name = 'f_name'


    f_name = fields.Char()
    l_name=fields.Char()
    birth_date=fields.Date()
    history=fields.Html()
    CR_ratio=fields.Float()
    blood_type=fields.Selection([('A+','A+'),
                                 ('A-','A-'),
                                 ('B+', 'B+'),
                                 ('B-', 'B-')
                                 ],
                                default="A+")
    PCR=fields.Boolean()
    image=fields.Binary("Image")
    address=fields.Text()
    Age=fields.Integer(compute='compute_age')
    department_id=fields.Many2one('hms.department')
    department_capacity=fields.Integer(related='department_id.capacity')
    doctor_ids=fields.Many2many('hms.doctor')
    stage = fields.Selection([
        ("undetemined", "undetemined"),
        ("serious", "Serious"),
        ("fair", "Fair"),
        ("good", "Good"),
        ], default="undetemined")
    patient_logs_id= fields.One2many('hms.logs','patient_id')
    email=fields.Char()
    crm=fields.Many2many('res.partner')

    def change_state(self):
        print(self._uid,self.env.user.id,'kkkkk',self.id)
        if self.stage == 'undetemined':
            self.stage ='serious'
        elif self.stage == 'serious':
            self.stage = 'fair'
        elif self.stage == 'fair':
            self.stage='good'
        self.env['hms.logs'].create({'description':'nex state','patient_id':self.id})

    @api.onchange('Age')
    def onchange_age(self):
        if self.Age>30 and self.Age==0:
            self.PCR=False
        else:
            self.PCR=True
            return {
                    'warning':{
                        'title':'age change',
                        'message':'PCR has been checked!'
                    }
                }
    @api.depends('birth_date')
    def compute_age(self):
        today = date.today()
        for record in self:
            print(record.birth_date.year)
            record.Age=today.year - record.birth_date.year - ((today.month, today.day) < (record.birth_date.month, record.birth_date.day))



    @api.constrains("email")
    def check_email(self):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        for record in self:
            if not re.search(regex, record.email):
                raise ValidationError("Opps not atrue email pleaze enter some thing like this = ahmed_hazem@yahoo.com")


class Logs(models.Model):
    _name = 'hms.logs'
    description = fields.Char()
    patient_id = fields.Many2one(comodel_name="hms.patient")
    _columns = {
        'create_date': fields.Datetime('Date Created', readonly=True),
        'create_uid': fields.Many2one('res.users', 'by User', readonly=True),
    }

















#