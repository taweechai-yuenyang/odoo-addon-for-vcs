# -*- coding: utf-8 -*-
{
    'name': "Crypto List",

    'author': "Taweechai Yuenyang",
    "email": "taweechai.yuenyang@outlook.com",
    'website': 'https://abe27.github.io',
    'license': 'Other OSI approved licence',# license คือ หมวดหมู่หน่วยงานของโมดูล
    'summary': 'จัดการข้อมูลรายการ Crypto Currency',# summary คือ คำอธิบายสั้นๆ ของโมดูล
    'description': 'ระบบจัดการข้อมูล Crypto Currency พัฒนาขึ้มมาเพื่อทดลองเขียน Module และความชอบสวนตัวเท่านั้น',# description คือ คำอธิบายยาวของโมดูล

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services',
    'version': '0.1',# version คือ เวอร์ชันของโมดูล

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "application": True,
    'installable': True,# installable คือ ระบุว่าโมดูลสามารถติดตั้งได้หรือไม่
    'auto_install': False,# auto_install คือ ระบุว่าโมดูลจะติดตั้งโดยอัตโนมัติหรือไม่
}