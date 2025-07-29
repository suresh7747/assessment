# Copyright (c) 2025, suresh and contributors
# For license information, please see license.txt

import frappe
import random
import string
from frappe import throw, _

from frappe.model.document import Document

class AirplaneTicket(Document):

    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw("You can only submit a ticket when the status is 'Boarded'.")

    def validate(self):
        self.remove_duplicate_add_ons()
        self.calculate_total_amount()

    def remove_duplicate_add_ons(self):
        unique_add_ons = {}
        cleaned_add_ons = []

        for add_on in self.add_ons:
            if add_on.add_on_type not in unique_add_ons:
                unique_add_ons[add_on.add_on_type] = True
                cleaned_add_ons.append(add_on)

        self.add_ons = cleaned_add_ons

    def calculate_total_amount(self):
        total = self.flight_price or 0.0
        for add_on in self.add_ons:
            total += add_on.amount or 0.0

        self.total_amount = total

    def before_insert(self):
        seat_number = f"{random.randint(1, 99)}{random.choice(['A', 'B', 'C', 'D', 'E'])}"
        self.seat = seat_number

    def validate(self):
        if not self.airplane_flight:
            return 

        flight = frappe.get_doc('Airplane Flight', self.airplane_flight)

        if not flight.airplane:
            return  

        airplane = frappe.get_doc('Airplane', flight.airplane)

        ticket_count = frappe.db.count('Airplane Ticket', {
            'airplane_flight': self.airplane_flight,
            'docstatus': ['<', 2]  
        })

        if ticket_count >= airplane.capacity:
            throw(_('Cannot create ticket: Airplane is fully booked (Capacity: {0})').format(airplane.capacity))
    
    