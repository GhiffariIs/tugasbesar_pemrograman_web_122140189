# api_demo.py
import requests
import json
import time
import traceback
from datetime import datetime

# Base URL API
BASE_URL = "http://localhost:6543/api/v1"
REQUEST_TIMEOUT = 10  # Seconds

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

def test_auth():
    print("\n===== TEST AUTENTIKASI =====\n")
    
    results = {
        "admin_login": False,
        "admin_profile": False,
        "staff_login": False,
        "register": False,
    }
    
    try:
        # 1. Login dengan admin
        print("1. LOGIN ADMIN")
        login_data = {
            "username": "admin",
            "password": "adminpassword"
        }
        
        response = requests.post(
            f"{BASE_URL}/auth/login", 
            json=login_data,
            timeout=REQUEST_TIMEOUT
        )
        print_response(response)
        
        # Ekstrak token JWT dari respons admin
        admin_token = None
        if response.status_code == 200:
            admin_token = response.json().get("token")
            results["admin_login"] = True
            print("✓ Admin login successful")
        else:
            print("✗ Admin login failed")
        
        # 2. Dapatkan profil admin
        if admin_token:
            print("\n2. GET ADMIN PROFILE")
            headers = {"Authorization": f"Bearer {admin_token}"}
            response = requests.get(
                f"{BASE_URL}/auth/me", 
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            print_response(response)
            
            if response.status_code == 200:
                results["admin_profile"] = True
                print("✓ Admin profile fetch successful")
            else:
                print("✗ Admin profile fetch failed")
        else:
            print("\nSkipping admin profile check - login failed")
            
        # 3. Login dengan staff
        print("\n3. LOGIN STAFF")
        login_data = {
            "username": "staff",
            "password": "staffpassword"
        }
        
        response = requests.post(
            f"{BASE_URL}/auth/login", 
            json=login_data,
            timeout=REQUEST_TIMEOUT
        )
        print_response(response)
        
        if response.status_code == 200:
            staff_token = response.json().get("token")
            results["staff_login"] = True
            print("✓ Staff login successful")
        else:
            print("✗ Staff login failed")
            
        # 4. Register user baru (optional - uncomment to test)
        timestamp = int(time.time())
        print(f"\n4. REGISTER NEW USER (test{timestamp})")
        register_data = {
            "name": f"Test User {timestamp}",
            "username": f"test{timestamp}",
            "email": f"test{timestamp}@example.com",
            "password": "testpassword"
        }
        response = requests.post(
            f"{BASE_URL}/auth/register", 
            json=register_data,
            timeout=REQUEST_TIMEOUT
        )
        print_response(response) 
        if response.status_code in [200, 201]:
            results["register"] = True
            print("✓ User registration successful")
        else:
            print("✗ User registration failed")
        
        return admin_token, results
        
    except requests.exceptions.RequestException as e:
        print(f"Network error in test_auth: {e}")
        return None, results
    except Exception as e:
        print(f"Error in test_auth: {e}")
        traceback.print_exc()
        return None, results

def test_products(token):
    print("\n===== TEST PRODUK =====\n")
    
    results = {
        "get_all": False,
        "create": False,
        "get_detail": False,
        "update": False,
        "delete": False
    }
    
    if not token:
        print("Token tidak tersedia. Autentikasi diperlukan.")
        return results
    
    headers = {"Authorization": f"Bearer {token}"}
    product_id = None
    
    try:
        # 1. Get semua produk
        print("1. GET ALL PRODUCTS")
        try:
            response = requests.get(
                f"{BASE_URL}/products",
                timeout=REQUEST_TIMEOUT
            )
            print_response(response)
            
            if response.status_code == 200:
                results["get_all"] = True
                print("✓ Get all products successful")
            else:
                print("✗ Get all products failed")
                
        except Exception as e:
            print(f"Error getting products: {e}")
        
        # 2. Buat produk baru
        print("\n2. CREATE NEW PRODUCT")
        timestamp = int(time.time())
        sku = f"TEST{timestamp}"
        new_product = {
            "name": f"Test Product {sku}",
            "sku": sku,
            "description": f"Produk untuk demo API, dibuat pada {datetime.now().isoformat()}",
            "price": 50000,
            "stock": 100
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/products", 
                json=new_product, 
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            print_response(response)
            
            if response.status_code in [200, 201]:
                try:
                    product_id = response.json().get("product", {}).get("id")
                    if product_id:
                        results["create"] = True
                        print(f"✓ Product creation successful (ID: {product_id})")
                    else:
                        print("✗ Product created but no ID returned")
                except Exception as e:
                    print(f"Failed to get product ID: {e}")
            else:
                print("✗ Product creation failed")
                
        except Exception as e:
            print(f"Error creating product: {e}")
            
        # 3. Get detail produk
        if product_id:
            print(f"\n3. GET PRODUCT DETAIL (ID: {product_id})")
            try:
                response = requests.get(
                    f"{BASE_URL}/products/{product_id}",
                    timeout=REQUEST_TIMEOUT
                )
                print_response(response)
                
                if response.status_code == 200:
                    results["get_detail"] = True
                    print("✓ Get product detail successful")
                else:
                    print("✗ Get product detail failed")
                    
            except Exception as e:
                print(f"Error getting product detail: {e}")
                
            # 4. Update produk
            print(f"\n4. UPDATE PRODUCT (ID: {product_id})")
            update_data = {
                "name": f"Updated Product {sku}",
                "price": 75000,
                "stock": 50,
                "description": f"Updated product description at {datetime.now().isoformat()}"
            }
            
            try:
                response = requests.put(
                    f"{BASE_URL}/products/{product_id}", 
                    json=update_data, 
                    headers=headers,
                    timeout=REQUEST_TIMEOUT
                )
                print_response(response)
                
                if response.status_code == 200:
                    results["update"] = True
                    print("✓ Update product successful")
                else:
                    print("✗ Update product failed")
                    
            except Exception as e:
                print(f"Error updating product: {e}")
                
            # 5. Delete produk
            print(f"\n5. DELETE PRODUCT (ID: {product_id})")
            try:
                response = requests.delete(
                    f"{BASE_URL}/products/{product_id}", 
                    headers=headers,
                    timeout=REQUEST_TIMEOUT
                )
                print_response(response)
                
                if response.status_code == 200:
                    results["delete"] = True
                    print("✓ Delete product successful")
                else:
                    print("✗ Delete product failed")
                    
            except Exception as e:
                print(f"Error deleting product: {e}")
        else:
            print("\nSkipping product operations - no product ID")
            
    except Exception as e:
        print(f"Error in test_products: {e}")
        traceback.print_exc()
        
    return results

def print_test_summary(auth_results, product_results):
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    print("\nAUTHENTICATION TESTS:")
    for test, result in auth_results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test:20}: {status}")
        
    print("\nPRODUCT TESTS:")
    for test, result in product_results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test:20}: {status}")
    
    total_tests = len(auth_results) + len(product_results)
    passed_tests = sum(auth_results.values()) + sum(product_results.values())
    
    print("\nOVERALL RESULTS:")
    print(f"Tests passed: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! API is working correctly.")
    elif passed_tests >= total_tests * 0.8:
        print("\n⚠️ Most tests passed, but some issues were detected.")
    else:
        print("\n❌ Several tests failed. API may not be working correctly.")

if __name__ == "__main__":
    print("Starting Aturmation API tests...")
    print(f"Base URL: {BASE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    try:
        # Test autentikasi dan dapatkan token
        token, auth_results = test_auth()
        
        # Test operasi produk
        if token:
            product_results = test_products(token)
        else:
            print("Autentikasi gagal, tidak dapat melanjutkan test produk.")
            product_results = dict.fromkeys(["get_all", "create", "get_detail", "update", "delete"], False)
            
        # Print test summary
        print_test_summary(auth_results, product_results)
        
    except Exception as e:
        print(f"Unexpected error in main: {e}")
        traceback.print_exc()