import frappe
from frappe.utils import today, add_days

def send_rent_reminders():
    settings = frappe.get_single("Shop Settings")
    if not settings.enable_rent_reminders:
        return

    shops = frappe.get_all("Airport Shop", filters={"status": "Occupied"}, fields=["name", "tenant", "rent_amount"])

    for shop in shops:
        tenant = frappe.get_doc("Tenant", shop.tenant)
        frappe.sendmail(
            recipients=[tenant.email],
            subject="Monthly Rent Reminder",
            message=f"Dear {tenant.tenant_name},<br>Your rent of ₹{shop.rent_amount} is due for shop {shop.name}.<br>Regards,<br>Airport Authority"
        )