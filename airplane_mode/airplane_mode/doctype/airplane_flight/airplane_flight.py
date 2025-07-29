# Copyright (c) 2025, suresh and contributors
# For license information, please see license.txt


from frappe.model.document import Document
import frappe
# from airplane_mode.airplane_mode.utils import update_gate_in_tickets


class AirplaneFlight(Document):

        def on_update(self):
                tickets = frappe.get_all("Airplane Ticket", filters={"airplane_flight": self.name}, pluck="name")
                for ticket_name in tickets:
                        frappe.db.set_value("Airplane Ticket", ticket_name, "gate_number", self.gate_number)
        
        def on_submit(self):
                self.status = "Completed"