import frappe
from frappe import _
from frappe.utils import nowdate, add_days

@frappe.whitelist()
def send_invitation_emails(meeting):
    meeting = frappe.get_doc("Meeting", meeting)
    meeting.check_permission("email")

    if meeting.status == "Planned":
        frappe.sendmail(
            recipients = [d.attendee for r in meeting.attendees],
            sender = frappe.session.user,
            subject = meeting.title,
            message = meeting.invitation_message,
            reference_doctype = meeting.doctype,
            reference_name = meeting.name,
            # as_bulk = True
        )

        meeting.status = "Invitation Sent"
        meeting.save()

    else:
        frappe.msgprint("Meeting Status must be 'Planned'")

@frappe.whitelist()
def get_meetings(start, end):
    if not frappe.has_permission("Meeting", "read"):
        raise frappe.PermissionError

    return frappe.db.sql(
        """
            select
                timestamp('date', from_date) as start,
                timestamp('date', to_time) as end,
                name,
                title,
                Status
            from 'tabMeeting'
            where 'date' between %(start)s and %(end)s
        """, {
            "start": start,
            "end": end
        }, as_dict=True)

def make_orientation_meeting(doc, method):
    """Create an orientation meeting when a new User is added"""
    meeting = frappe.get_doc({
        "doctype": "Meeting",
        "title": "Orientation for {0}".format(doc.first_name),
        "date": add_days(nowdate(), 1),
        "from_time": "09:00",
        "to_time": "10:00",
        "status": "Planned",
        "attendees": [{
            "attendee": doc.name
        }]
    })

    # the System Manager might not have permission to create a Meeting
    meeting.flags.ignore_permissions = True
    meeting.insert()

    frappe.msgprint(_("Orientation meeting created"))
