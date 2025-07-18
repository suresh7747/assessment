# Copyright (c) 2025, suresh and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe.query_builder import DocType
from pypika import functions as fn

def execute(filters=None):
    columns = [
        {
            "label": "Airline",
            "fieldname": "airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": 200
        },
        {
            "label": "Revenue",
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 150
        }
    ]

    Ticket = DocType("Airplane Ticket")
    Flight = DocType("Airplane Flight")
    Airplane = DocType("Airplane")
    Airline = DocType("Airline")

    all_airlines = frappe.get_all("Airline", pluck="name")

    qb = (
        frappe.qb.from_(Ticket)
        .inner_join(Flight).on(Flight.name == Ticket.airplane_flight)
        .inner_join(Airplane).on(Airplane.name == Flight.airplane)
        .inner_join(Airline).on(Airline.name == Airplane.airline)
        .groupby(Airline.name)
        .select(
            Airline.name.as_("airline"),
            fn.Sum(Ticket.total_amount).as_("revenue")
        )
    )

    revenue_data = frappe.db.sql(qb, as_dict=True)

    airline_revenue_map = {r["airline"]: r["revenue"] for r in revenue_data}

    data = []
    total_revenue = 0

    for airline in all_airlines:
        revenue = airline_revenue_map.get(airline, 0)
        total_revenue += revenue
        data.append({
            "airline": airline,
            "revenue": revenue
        })

    chart = {
        "data": {
            "labels": [d["airline"] for d in data],
            "datasets": [{"name": "Revenue", "values": [d["revenue"] for d in data]}]
        },
        "type": "donut"
    }

    summary = [
        {
            "label": "Total Revenue",
            "value": total_revenue,
            "indicator": "Green"
        }
    ]

    return columns, data, None, chart, summary
