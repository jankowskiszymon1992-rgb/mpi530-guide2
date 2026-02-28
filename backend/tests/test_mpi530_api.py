"""
Backend API tests for Sonel MPI-530 Interactive Guide Application
Tests all API endpoints including:
- Measurement functions (10 functions)
- Tools (Calculator, Cable, Checklists, Quiz)
- Protocols (Guides, Templates, Examples)
- Search functionality
"""

import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# ============================================
# ROOT AND FUNCTIONS API TESTS
# ============================================

class TestRootAPI:
    """Test root API endpoint"""
    
    def test_root_endpoint_returns_success(self):
        """Test that root API returns version info"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Sonel MPI-530" in data["message"]
        print(f"✓ Root API: {data['message']}")


class TestFunctionsAPI:
    """Test measurement functions endpoints"""
    
    def test_get_all_functions_returns_10_items(self):
        """Test that /functions returns 10 measurement functions"""
        response = requests.get(f"{BASE_URL}/api/functions")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10, f"Expected 10 functions, got {len(data)}"
        print(f"✓ Functions API: {len(data)} functions returned")
    
    def test_all_functions_have_required_fields(self):
        """Test that all functions have required fields"""
        response = requests.get(f"{BASE_URL}/api/functions")
        assert response.status_code == 200
        data = response.json()
        
        required_fields = ["id", "name", "icon", "description", "category", "color", "steps", "parameters", "safety_notes", "expected_results", "main_image"]
        
        for func in data:
            for field in required_fields:
                assert field in func, f"Function {func.get('id', 'unknown')} missing field: {field}"
        print("✓ All functions have required fields")
    
    def test_functions_are_in_polish(self):
        """Test that function names are in Polish"""
        response = requests.get(f"{BASE_URL}/api/functions")
        assert response.status_code == 200
        data = response.json()
        
        # Check for Polish characters or known Polish words
        polish_indicators = ["Wyłącznik", "Pętl", "Rezystanc", "Uziemien", "Napięc", "Ciągłość", "Kolej", "Kierun", "Oświetl", "Cęgow"]
        found_polish = False
        for func in data:
            for indicator in polish_indicators:
                if indicator in func["name"]:
                    found_polish = True
                    break
        
        assert found_polish, "Functions should be in Polish"
        print("✓ Functions are in Polish")
    
    def test_get_rcd_function_by_id(self):
        """Test getting RCD function by ID"""
        response = requests.get(f"{BASE_URL}/api/functions/rcd")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "rcd"
        assert "RCD" in data["name"]
        assert len(data["steps"]) >= 4
        print(f"✓ RCD function: {data['name'][:50]}...")
    
    def test_get_loop_function_by_id(self):
        """Test getting Loop (Zs) function by ID"""
        response = requests.get(f"{BASE_URL}/api/functions/loop")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "loop"
        assert "Pętl" in data["name"] or "Impedanc" in data["name"]
        print(f"✓ Loop function: {data['name'][:50]}...")
    
    def test_get_nonexistent_function_returns_404(self):
        """Test that nonexistent function ID returns 404"""
        response = requests.get(f"{BASE_URL}/api/functions/nonexistent")
        assert response.status_code == 404


# ============================================
# TOOLS API TESTS
# ============================================

class TestCalculatorAPI:
    """Test Zs Calculator endpoint"""
    
    def test_calculator_basic_calculation(self):
        """Test Zs Calculator with basic values: Zs=0.45, Voltage=230"""
        response = requests.get(f"{BASE_URL}/api/tools/calculator", params={"zs": 0.45, "voltage": 230})
        assert response.status_code == 200
        data = response.json()
        
        assert "input" in data
        assert "result" in data
        assert "recommendations" in data
        
        # Verify calculation: Ik = Uo / Zs = 230 / 0.45 ≈ 511.1 A
        assert abs(data["result"]["Ik"] - 511.1) < 1, f"Expected Ik ≈ 511.1, got {data['result']['Ik']}"
        print(f"✓ Calculator: Zs=0.45Ω, Uo=230V → Ik={data['result']['Ik']}A")
    
    def test_calculator_recommendations_provided(self):
        """Test that calculator provides circuit breaker recommendations"""
        response = requests.get(f"{BASE_URL}/api/tools/calculator", params={"zs": 0.45, "voltage": 230})
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["recommendations"]) > 0, "Should provide recommendations"
        rec = data["recommendations"][0]
        assert "type" in rec
        assert "Zs_max" in rec
        print(f"✓ Calculator recommendations: {len(data['recommendations'])} options")


class TestCableCalculatorAPI:
    """Test Cable Calculator endpoint"""
    
    def test_cable_calculator_basic(self):
        """Test cable calculator with: 3.5kW, 230V, 10m, 3% drop, 1 phase"""
        response = requests.get(f"{BASE_URL}/api/tools/cable-calculator", params={
            "power_kw": 3.5,
            "voltage": 230,
            "length_m": 10,
            "max_drop_percent": 3,
            "phases": 1,
            "cable_type": "cu_pvc"
        })
        assert response.status_code == 200
        data = response.json()
        
        assert "input" in data
        assert "calculated" in data
        assert "recommended" in data
        assert "all_suitable" in data
        
        # Verify a section is recommended
        assert "section_mm2" in data["recommended"]
        print(f"✓ Cable Calculator: 3.5kW → {data['recommended']['section_mm2']} mm²")
    
    def test_cable_calculator_returns_suitable_options(self):
        """Test that cable calculator returns multiple suitable options"""
        response = requests.get(f"{BASE_URL}/api/tools/cable-calculator", params={
            "power_kw": 3.5,
            "voltage": 230,
            "length_m": 10,
            "max_drop_percent": 3,
            "phases": 1,
            "cable_type": "cu_pvc"
        })
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["all_suitable"]) > 0, "Should provide suitable cable options"
        print(f"✓ Cable Calculator: {len(data['all_suitable'])} suitable options")


class TestChecklistsAPI:
    """Test Safety Checklists endpoint"""
    
    def test_get_all_checklists(self):
        """Test that checklists endpoint returns data"""
        response = requests.get(f"{BASE_URL}/api/tools/checklists")
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, dict)
        assert len(data) >= 6, f"Expected at least 6 checklists, got {len(data)}"
        print(f"✓ Checklists: {len(data)} checklists returned")
    
    def test_checklists_have_items(self):
        """Test that each checklist has items"""
        response = requests.get(f"{BASE_URL}/api/tools/checklists")
        assert response.status_code == 200
        data = response.json()
        
        for key, checklist in data.items():
            assert "name" in checklist
            assert "items" in checklist
            assert len(checklist["items"]) > 0
        print("✓ All checklists have items")


class TestQuizAPI:
    """Test Quiz endpoints"""
    
    def test_get_quiz_questions(self):
        """Test that quiz returns questions"""
        response = requests.get(f"{BASE_URL}/api/quiz/questions")
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) == 15, f"Expected 15 questions, got {len(data)}"
        print(f"✓ Quiz: {len(data)} questions returned")
    
    def test_quiz_questions_have_options(self):
        """Test that each question has 4 options (A-D)"""
        response = requests.get(f"{BASE_URL}/api/quiz/questions")
        assert response.status_code == 200
        data = response.json()
        
        for q in data:
            assert "id" in q
            assert "question" in q
            assert "options" in q
            assert len(q["options"]) == 4, f"Question {q['id']} should have 4 options"
        print("✓ All questions have 4 options")
    
    def test_quiz_check_answers(self):
        """Test that quiz can check answers"""
        # First get questions to know valid IDs
        response = requests.get(f"{BASE_URL}/api/quiz/questions")
        questions = response.json()
        
        # Submit dummy answers
        answers = {q["id"]: 0 for q in questions}
        response = requests.post(f"{BASE_URL}/api/quiz/check", json=answers)
        assert response.status_code == 200
        data = response.json()
        
        assert "results" in data
        assert "summary" in data
        assert "correct" in data["summary"]
        assert "total" in data["summary"]
        print(f"✓ Quiz check: {data['summary']['correct']}/{data['summary']['total']} correct")


class TestNormsAPI:
    """Test Norms/Tables endpoint"""
    
    def test_get_all_norms(self):
        """Test that norms endpoint returns all norm tables"""
        response = requests.get(f"{BASE_URL}/api/tools/norms")
        assert response.status_code == 200
        data = response.json()
        
        assert "zs_tables" in data
        assert "insulation" in data
        assert "rcd_times" in data
        assert "lighting" in data
        print("✓ Norms: All norm tables returned")


class TestErrorCodesAPI:
    """Test Error Codes endpoint"""
    
    def test_get_error_codes(self):
        """Test that error codes endpoint returns data"""
        response = requests.get(f"{BASE_URL}/api/tools/error-codes")
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check structure
        for error in data:
            assert "code" in error
            assert "name" in error
            assert "description" in error
            assert "causes" in error
            assert "solutions" in error
        print(f"✓ Error Codes: {len(data)} error codes returned")


class TestDiagramsAPI:
    """Test Connection Diagrams endpoint"""
    
    def test_get_diagrams(self):
        """Test that diagrams endpoint returns data"""
        response = requests.get(f"{BASE_URL}/api/tools/diagrams")
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"✓ Diagrams: {len(data)} connection diagrams returned")


# ============================================
# PROTOCOLS API TESTS
# ============================================

class TestProtocolGuidesAPI:
    """Test Protocol Guides endpoints"""
    
    def test_get_protocol_guides(self):
        """Test that protocol guides endpoint returns data"""
        response = requests.get(f"{BASE_URL}/api/protocols/guides")
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) >= 4, f"Expected at least 4 guides, got {len(data)}"
        print(f"✓ Protocol Guides: {len(data)} guides returned")
    
    def test_guide_has_steps(self):
        """Test that guides have step-by-step instructions"""
        response = requests.get(f"{BASE_URL}/api/protocols/guides")
        assert response.status_code == 200
        data = response.json()
        
        for guide in data:
            assert "id" in guide
            assert "name" in guide
            assert "steps" in guide
            assert len(guide["steps"]) > 0
        print("✓ All protocol guides have steps")


class TestProtocolTemplatesAPI:
    """Test Protocol Templates endpoints"""
    
    def test_get_protocol_templates(self):
        """Test that protocol templates endpoint returns data"""
        response = requests.get(f"{BASE_URL}/api/protocols/templates")
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) >= 3, f"Expected at least 3 templates, got {len(data)}"
        print(f"✓ Protocol Templates: {len(data)} templates returned")


class TestProtocolExamplesAPI:
    """Test Protocol Examples endpoints"""
    
    def test_get_protocol_examples(self):
        """Test that protocol examples endpoint returns data"""
        response = requests.get(f"{BASE_URL}/api/protocols/examples")
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) >= 5, f"Expected at least 5 examples, got {len(data)}"
        print(f"✓ Protocol Examples: {len(data)} examples returned")
    
    def test_example_has_measurements(self):
        """Test that examples have measurements data"""
        response = requests.get(f"{BASE_URL}/api/protocols/examples")
        assert response.status_code == 200
        data = response.json()
        
        for example in data:
            assert "id" in example
            assert "name" in example
            assert "measurements" in example
            assert "conclusion" in example
            assert len(example["measurements"]) > 0
        print("✓ All protocol examples have measurements")


# ============================================
# SEARCH API TESTS
# ============================================

class TestSearchAPI:
    """Test Search functionality"""
    
    def test_search_rcd(self):
        """Test search for 'RCD'"""
        response = requests.get(f"{BASE_URL}/api/search", params={"q": "RCD"})
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) > 0, "Search for 'RCD' should return results"
        print(f"✓ Search 'RCD': {len(data)} results")
    
    def test_search_polish_word(self):
        """Test search for Polish word 'impedancja'"""
        response = requests.get(f"{BASE_URL}/api/search", params={"q": "impedancja"})
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) > 0, "Search for 'impedancja' should return results"
        print(f"✓ Search 'impedancja': {len(data)} results")


# ============================================
# IMAGES API TEST
# ============================================

class TestImagesAPI:
    """Test Images endpoint"""
    
    def test_get_meter_images(self):
        """Test that images endpoint returns Sonel CDN URLs"""
        response = requests.get(f"{BASE_URL}/api/images")
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, dict)
        assert len(data) >= 10, f"Expected at least 10 images, got {len(data)}"
        
        # Check that URLs are from Sonel CDN
        for key, url in data.items():
            assert "cdn.sonel.com" in url, f"Image {key} should be from Sonel CDN"
        print(f"✓ Images: {len(data)} official Sonel CDN images")


# ============================================
# FAQ API TEST
# ============================================

class TestFAQAPI:
    """Test FAQ endpoint"""
    
    def test_get_faq(self):
        """Test that FAQ endpoint returns data"""
        response = requests.get(f"{BASE_URL}/api/faq")
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) > 0
        
        for faq in data:
            assert "question" in faq
            assert "answer" in faq
            assert "category" in faq
        print(f"✓ FAQ: {len(data)} FAQ items returned")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
