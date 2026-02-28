import requests
import sys
from datetime import datetime

class SonelAPITester:
    def __init__(self, base_url="https://sonel-meter-guide-1.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if endpoint else self.api_url
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response data type: {type(response_data)}")
                    if isinstance(response_data, list):
                        print(f"   Items count: {len(response_data)}")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                self.failed_tests.append({
                    'test': name, 
                    'endpoint': url,
                    'expected': expected_status,
                    'actual': response.status_code,
                    'error': response.text if response.status_code >= 400 else None
                })
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append({
                'test': name,
                'endpoint': url, 
                'error': str(e)
            })
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root API", "GET", "", 200)

    def test_get_all_functions(self):
        """Test /api/functions endpoint - should return 6 functions"""
        success, response = self.run_test("Get All Functions", "GET", "functions", 200)
        if success and isinstance(response, list):
            if len(response) == 6:
                print(f"   ✅ Correct number of functions: {len(response)}")
                # Verify function structure
                expected_ids = ["rcd", "loop", "insulation", "earthing", "voltage", "continuity"]
                actual_ids = [func.get('id') for func in response]
                if set(expected_ids) == set(actual_ids):
                    print(f"   ✅ All expected function IDs found")
                else:
                    print(f"   ⚠️ Function IDs mismatch. Expected: {expected_ids}, Got: {actual_ids}")
                return True, response
            else:
                print(f"   ❌ Expected 6 functions, got {len(response)}")
                return False, response
        return success, response

    def test_get_specific_functions(self, function_ids):
        """Test /api/functions/{id} endpoint for specific functions"""
        results = []
        for func_id in function_ids:
            success, response = self.run_test(
                f"Get Function {func_id}", 
                "GET", 
                f"functions/{func_id}", 
                200
            )
            results.append((func_id, success, response))
            if success and response:
                # Verify function has required fields including main_image
                required_fields = ['id', 'name', 'icon', 'description', 'steps', 'parameters', 'safety_notes', 'main_image']
                missing_fields = [field for field in required_fields if field not in response]
                if not missing_fields:
                    print(f"   ✅ All required fields present for {func_id}")
                else:
                    print(f"   ⚠️ Missing fields in {func_id}: {missing_fields}")
                
                # Check if name is in Polish (should contain Polish characters or specific Polish terms)
                name = response.get('name', '')
                polish_indicators = ['Test', 'Pomiar', 'Rezystancja', 'Impedancja', 'Ciągłość', 'ść', 'ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż']
                if any(indicator in name for indicator in polish_indicators):
                    print(f"   ✅ Function name appears to be in Polish: {name}")
                else:
                    print(f"   ⚠️ Function name may not be in Polish: {name}")
                
                # Check main_image URL (should be from Sonel CDN)
                main_image = response.get('main_image', '')
                if 'cdn.sonel.com' in main_image:
                    print(f"   ✅ Main image from Sonel CDN: {main_image}")
                else:
                    print(f"   ⚠️ Main image not from Sonel CDN: {main_image}")
                    
        return results

    def test_search_api(self):
        """Test /api/search endpoint"""
        search_queries = [
            ("rcd", "RCD search"),
            ("napięcie", "Polish search"),
            ("impedance", "English search"),
            ("test", "General search")
        ]
        
        results = []
        for query, description in search_queries:
            success, response = self.run_test(
                f"Search: {description}", 
                "GET", 
                "search", 
                200, 
                params={"q": query}
            )
            results.append((query, success, response))
            if success and isinstance(response, list):
                print(f"   ✅ Search '{query}' returned {len(response)} results")
        return results

    def test_faq_api(self):
        """Test /api/faq endpoint"""
        success, response = self.run_test("Get FAQ", "GET", "faq", 200)
        if success and isinstance(response, list):
            print(f"   ✅ FAQ returned {len(response)} items")
            # Check FAQ structure
            if response and len(response) > 0:
                faq_item = response[0]
                required_fields = ['id', 'question', 'answer', 'category']
                missing_fields = [field for field in required_fields if field not in faq_item]
                if not missing_fields:
                    print(f"   ✅ FAQ items have correct structure")
                else:
                    print(f"   ⚠️ FAQ missing fields: {missing_fields}")
        return success, response

    def test_categories_api(self):
        """Test /api/categories endpoint"""
        success, response = self.run_test("Get Categories", "GET", "categories", 200)
        if success and isinstance(response, list):
            print(f"   ✅ Categories returned {len(response)} items")
        return success, response

def main():
    print("="*60)
    print("SONEL MPI-530 Interactive Guide - Backend API Testing")
    print("="*60)
    
    # Setup tester
    tester = SonelAPITester()
    
    # Test 1: Root endpoint
    print("\n📍 Testing Root API Endpoint...")
    tester.test_root_endpoint()
    
    # Test 2: Get all functions - must return 6 functions
    print("\n📍 Testing Functions Endpoint...")
    success, functions_data = tester.test_get_all_functions()
    
    # Test 3: Get specific functions
    if success and functions_data:
        function_ids = [func['id'] for func in functions_data[:3]]  # Test first 3
        print(f"\n📍 Testing Individual Function Endpoints...")
        tester.test_get_specific_functions(function_ids)
    
    # Test 4: Search API
    print("\n📍 Testing Search API...")
    tester.test_search_api()
    
    # Test 5: FAQ API
    print("\n📍 Testing FAQ API...")
    tester.test_faq_api()
    
    # Test 6: Categories API (bonus)
    print("\n📍 Testing Categories API...")
    tester.test_categories_api()
    
    # Print results summary
    print("\n" + "="*60)
    print("BACKEND TEST RESULTS")
    print("="*60)
    print(f"📊 Tests Run: {tester.tests_run}")
    print(f"✅ Tests Passed: {tester.tests_passed}")
    print(f"❌ Tests Failed: {tester.tests_run - tester.tests_passed}")
    print(f"📈 Success Rate: {(tester.tests_passed / tester.tests_run * 100):.1f}%")
    
    if tester.failed_tests:
        print("\n🚨 FAILED TESTS:")
        for failure in tester.failed_tests:
            print(f"   - {failure['test']}: {failure.get('error', 'Status code mismatch')}")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())