import urllib.parse
import hmac
import hashlib
from datetime import datetime

# --- CẤU HÌNH ---
VNPAY_URL = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'
VNP_TMN_CODE = 'IQRCRXK8'
VNP_HASH_SECRET = 'STDTDERBNDXT2LRBW1U4B59N72ZWWXDF'
VNP_RETURN_URL = 'http://localhost:5000/vnpay_return'

# --- INPUT GIẢ LẬP ---
amount_vnd = 100000  # 100,000 VND

# --- TẠO THÔNG TIN GIAO DỊCH ---
order_id = 'ORDER' + datetime.now().strftime('%Y%m%d%H%M%S')
# Dùng tiếng Anh để tránh lỗi encode
order_desc = f"Payment for order {order_id}"
user_ip = '127.0.0.1'

vnp_params = {
    'vnp_Version': '2.1.0',
    'vnp_Command': 'pay',
    'vnp_TmnCode': VNP_TMN_CODE,
    'vnp_Amount': str(amount_vnd * 100),  # nhân 100 theo yêu cầu VNPay
    'vnp_CurrCode': 'VND',
    'vnp_TxnRef': order_id,
    'vnp_OrderInfo': order_desc,
    'vnp_OrderType': 'other',
    'vnp_Locale': 'vn',
    'vnp_ReturnUrl': VNP_RETURN_URL,
    'vnp_IpAddr': user_ip,
    'vnp_CreateDate': datetime.now().strftime('%Y%m%d%H%M%S'),
    'vnp_SecureHashType': 'SHA512'
}

# --- TẠO CHUỖI HASH ---
sorted_params = sorted(vnp_params.items())
hash_data = '&'.join(f"{k}={v}" for k, v in sorted_params)

secure_hash = hmac.new(
    VNP_HASH_SECRET.encode('utf-8'),
    hash_data.encode('utf-8'),
    hashlib.sha512
).hexdigest()

# --- TẠO URL THANH TOÁN ---
vnp_params['vnp_SecureHash'] = secure_hash
query_string = '&'.join(f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in vnp_params.items())
payment_url = f"{VNPAY_URL}?{query_string}"

# --- IN RA KẾT QUẢ AN TOÀN ---
def safe_print(label, content):
    try:
        print(label, content)
    except UnicodeEncodeError:
        print(label, content.encode('utf-8', errors='replace').decode('utf-8'))

print("\n=== VNPay Test ===")
safe_print("Hash Data:\n", hash_data)
safe_print("Secure Hash:\n", secure_hash)
safe_print("Payment URL:\n", payment_url)
print("\n✅ Copy URL lên trình duyệt để test VNPay sandbox.")
