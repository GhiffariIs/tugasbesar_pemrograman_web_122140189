# api_demo.py
import requests
import json
import time
import traceback

# Base URL API
BASE_URL = "http://localhost:6543/api/v1"

# Helper untuk mencetak respons dengan format yang rapi
def print_response(response):
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        print(response.text)
    print("-" * 50)

def demo_auth():
    print("\n===== DEMO AUTENTIKASI =====\n")
    
    try:
        # 1. Login dengan admin (user yang sudah ada)
        print("1. LOGIN ADMIN")
        login_data = {
            "username": "admin",
            "password": "adminpassword"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print_response(response)
        
        # Ekstrak token JWT dari respons admin
        admin_token = None
        if response.status_code == 200:
            admin_token = response.json().get("token")
        
        # Dapatkan profil admin
        if admin_token:
            print("\n2. GET ADMIN PROFILE")
            headers = {"Authorization": f"Bearer {admin_token}"}
            response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            print_response(response)
        else:
            print("\nSkipping profile check - login failed")
        
        return admin_token
    except Exception as e:
        print(f"Error in demo_auth: {e}")
        traceback.print_exc()
        return None

def demo_products(token):
    print("\n===== DEMO PRODUK =====\n")
    
    if not token:
        print("Token tidak tersedia. Autentikasi diperlukan.")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # 1. Get semua produk
        print("1. GET ALL PRODUCTS")
        response = requests.get(f"{BASE_URL}/products")
        print_response(response)
        
        # 2. Buat produk baru
        print("\n2. CREATE NEW PRODUCT")
        sku = f"TEST{int(time.time())}"
        new_product = {
            "name": f"Test Product {sku}",
            "sku": sku,
            "description": "Produk untuk demo API",
            "price": 50000,
            "stock": 100
        }
        
        response = requests.post(f"{BASE_URL}/products", json=new_product, headers=headers)
        print_response(response)
        
        # Ekstrak ID produk untuk operasi selanjutnya
        product_id = None
        if response.status_code in [200, 201]:
            try:
                product_id = response.json().get("product", {}).get("id")
            except Exception as e:
                print(f"Failed to get product ID from response: {e}")
        
        # 3. Get detail produk
        if product_id:
            print(f"\n3. GET PRODUCT DETAIL (ID: {product_id})")
            response = requests.get(f"{BASE_URL}/products/{product_id}")
            print_response(response)
            
            # 4. Update produk
            print(f"\n4. UPDATE PRODUCT (ID: {product_id})")
            update_data = {
                "name": f"Updated Product {sku}",
                "price": 75000,
                "stock": 50
            }
            
            response = requests.put(f"{BASE_URL}/products/{product_id}", json=update_data, headers=headers)
            print_response(response)
            
            # 5. Delete produk
            print(f"\n5. DELETE PRODUCT (ID: {product_id})")
            response = requests.delete(f"{BASE_URL}/products/{product_id}", headers=headers)
            print_response(response)
    except Exception as e:
        print(f"Error in demo_products: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    try:
        # Demo autentikasi dan dapatkan token
        token = demo_auth()
        
        # Demo operasi produk
        if token:
            demo_products(token)
        else:
            print("Autentikasi gagal, tidak dapat melanjutkan demo produk.")
    except Exception as e:
        print(f"Unexpected error in main: {e}")
        traceback.print_exc()