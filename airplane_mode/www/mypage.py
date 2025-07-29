import frappe

def get_context(context):
    context.my_secret_msg = "secret message from context/mypage.py"