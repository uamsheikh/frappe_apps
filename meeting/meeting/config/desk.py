from __future__ import unicode_literals
import frappe
from frappe import _

def get_data():
	return [
		# Administration
		{
            "label": _("Meeting"),
			"module_name": "Desk",
			"icon": "octicon octicon-calendar",
            "items": [
                {
                    "type": "doctype",
                    "name": "Meeting",
                    "label": _("Meeting"),
                    "description": _("Prepare agenda, invite users and record minutes")
                },
            ]
		},
    ]
