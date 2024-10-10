# -*- coding: utf-8 -*-
{
    'name': "teaching_performance",

    'summary': """
        Module for grading teachers.""",

    'description': """
        Module that records the annual grades of teachers.
    """,

    'author': "Atos",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Teaching Performance',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/teaching_employee_view.xml',
        'views/teaching_record_view.xml',
        'views/teaching_teaching_view.xml',
        'views/teaching_observation_view.xml',
        'wizard/score_wizard_views.xml',
        'views/teaching_degree_view.xml',
    ],

    # only loaded in demonstration mode for data
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    }
}
