import frappe
import random
import string
import requests
from frappe.exceptions import DoesNotExistError
from frappe.core.doctype.user.user import User

@frappe.whitelist()
def my_whitelisted_method(arg1,arg2):
    result = arg1 + arg2
    return {"message":"success","data":result}

@frappe.whitelist()
def get_logged_user():
 return frappe.session.user


@frappe.whitelist(allow_guest=True)
def get_otp(phone_number):
 #otp = ''.join(random.choices(string.digits,k=4))
 otp =5000
 frappe.cache().set(f"otp_{phone_number}",otp,ex=60*60)
#  send_sms(phone_number,otp)
 return {"message":"OTP Sent Successfully"}

@frappe.whitelist(allow_guest=True)
def verify_otp(phone_number,otp_entered):
  otp_verify = frappe.cache().get(f"otp_{phone_number}")

  if otp_verify:
        otp_verify = otp_verify.decode()
        otp_match = int(otp_verify)
  
  print(otp_verify,"otp_verify")
  
  if not otp_match or otp_match!=otp_entered:
    return {"success":False, "message": "Invalid or Expired OTP"}
  
  frappe.cache.delete(f"otp_{phone_number}")

  user =None
  user_created =False

  try:
     user: User = frappe.get_doc("User",{"phone":phone_number})
     
     if not user.phone:
       raise frappe.DoesNotExistError
     if not user.enabled:
       return {"success":False, "message":"User account is disabled"}
     
  except DoesNotExistError:
    try:
       new_user =frappe.get_doc({
         "doctype":"User",
         "phone_number":phone_number,
         "enabled":1,
       })
       new_user.insert(ignore_permissions=True)
       user = new_user
       user_created = True
    except Exception as e:
      frappe.log_error(title="User creation failed",message=f"Failed to create user for phone number {phone_number}:{e}")
      return {"success":False,"message":"User creation failed, Please try again"}
  
  try:
    api_key_data = frappe.core.doctype.user.user.generate_keys(user.name)
    api_key = api_key_data.get("api_key")
    api_secret = api_key_data.get("api_secret")

    if not api_key or api_secret:
      raise Exception("Failed to generate api key and secret")
    
    token =f"{api_key}:{api_secret}"
    response_message ="User created and authenticated successfully." if user_created else "User authenticated Successfully."
    return{"success":True,"message":response_message, "token": token}
  
  except Exception as e:
    frappe.log_error(title="Token generation failed.", message=f"Failed to generate token for user {user.name}:{e}")



def send_sms(phone_number,otp):
  try:
    twilio_url = frappe.conf.twilio_url
    api_key = frappe.conf.twilio_api_key
    sender_id = frappe.conf.twilio_sender_id
    headers ={"Authorization": f"Bearer {api_key}"}

    payload={
      "to":phone_number,
      "message": f"Your OTP is:{otp}",
      "sender_id": sender_id
    }

    response = requests.post(twilio_url, headers= headers, json= payload)
    response.raise_for_status()

    frappe.log_error(f"OTP {otp} sent successfully to {phone_number}","SMS Send Success")
  except requests.exceptions.RequestException as e:
    frappe.log_error(f"Failed to send SMS to {phone_number}:{e}","SMS Send Failure")
  except Exception as e:
    frappe.log_error(f"An unexpected error occurred during sms sending: {e}","SMS send error")