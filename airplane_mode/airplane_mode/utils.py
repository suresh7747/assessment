import frappe

def update_gate_in_tickets(flight, gate):
    tickets = frappe.get_all("Airplane Ticket", filters={"airplane_flight": flight}, pluck="name")
    for ticket_name in tickets:
        print('something')
        frappe.db.set_value("Airplane Ticket", ticket_name, "gate_number", gate)
