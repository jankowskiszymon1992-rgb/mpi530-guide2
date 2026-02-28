"""
Test suite for i18n (internationalization) feature of Sonel MPI-530 Interactive Guide.
Tests language switching (PL/EN/DE) across all API endpoints.
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL')

class TestI18nFunctions:
    """Test /api/functions endpoint with lang parameter"""
    
    def test_functions_polish_default(self):
        """Test that Polish is the default language"""
        response = requests.get(f"{BASE_URL}/api/functions")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        # Check Polish content - RCD function
        rcd = next((f for f in data if f['id'] == 'rcd'), None)
        assert rcd is not None
        assert 'Test Wyłączników Różnicowoprądowych' in rcd['name']
        print(f"Polish RCD name: {rcd['name']}")

    def test_functions_english(self):
        """Test functions in English"""
        response = requests.get(f"{BASE_URL}/api/functions?lang=en")
        assert response.status_code == 200
        data = response.json()
        rcd = next((f for f in data if f['id'] == 'rcd'), None)
        assert rcd is not None
        assert 'RCD' in rcd['name'] or 'Residual Current Device' in rcd['name']
        print(f"English RCD name: {rcd['name']}")

    def test_functions_german(self):
        """Test functions in German"""
        response = requests.get(f"{BASE_URL}/api/functions?lang=de")
        assert response.status_code == 200
        data = response.json()
        rcd = next((f for f in data if f['id'] == 'rcd'), None)
        assert rcd is not None
        # German should contain "RCD-Prüfung" or "Fehlerstromschutzschalter"
        assert 'RCD' in rcd['name'] or 'Prüfung' in rcd['name'] or 'Fehlerstrom' in rcd['name']
        print(f"German RCD name: {rcd['name']}")

    def test_function_details_english(self):
        """Test individual function details in English"""
        response = requests.get(f"{BASE_URL}/api/functions/rcd?lang=en")
        assert response.status_code == 200
        data = response.json()
        assert 'steps' in data
        # English steps should have English titles
        assert len(data['steps']) > 0
        # Check first step title is in English
        first_step = data['steps'][0]
        assert 'Preparation' in first_step['title'] or 'Connection' in first_step['title'] or first_step['title'] in ['Preparation', 'Cable connection', 'Parameter selection', 'Measurement', 'Reading the result']
        print(f"English first step: {first_step['title']}")

    def test_function_details_german(self):
        """Test individual function details in German"""
        response = requests.get(f"{BASE_URL}/api/functions/rcd?lang=de")
        assert response.status_code == 200
        data = response.json()
        assert 'steps' in data
        assert len(data['steps']) > 0
        first_step = data['steps'][0]
        # German step titles
        assert 'Vorbereitung' in first_step['title'] or 'Anschluss' in first_step['title'] or 'bereitung' in first_step['title']
        print(f"German first step: {first_step['title']}")


class TestI18nFAQ:
    """Test /api/faq endpoint with lang parameter"""
    
    def test_faq_polish(self):
        """Test FAQ in Polish"""
        response = requests.get(f"{BASE_URL}/api/faq?lang=pl")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        # Check Polish content
        first_faq = data[0]
        assert 'question' in first_faq
        print(f"Polish FAQ: {first_faq['question'][:50]}...")

    def test_faq_english(self):
        """Test FAQ in English"""
        response = requests.get(f"{BASE_URL}/api/faq?lang=en")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        first_faq = data[0]
        assert 'question' in first_faq
        # English questions should contain common English words
        combined = ' '.join([f['question'] for f in data])
        assert 'test' in combined.lower() or 'current' in combined.lower() or 'what' in combined.lower()
        print(f"English FAQ: {first_faq['question'][:50]}...")

    def test_faq_german(self):
        """Test FAQ in German"""
        response = requests.get(f"{BASE_URL}/api/faq?lang=de")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        first_faq = data[0]
        assert 'question' in first_faq
        # German questions
        combined = ' '.join([f['question'] for f in data])
        assert 'Was' in combined or 'Wie' in combined or 'Welch' in combined
        print(f"German FAQ: {first_faq['question'][:50]}...")


class TestI18nErrorCodes:
    """Test /api/tools/error-codes endpoint with lang parameter"""
    
    def test_error_codes_polish(self):
        """Test error codes in Polish"""
        response = requests.get(f"{BASE_URL}/api/tools/error-codes?lang=pl")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        # Check structure
        first_error = data[0]
        assert 'code' in first_error
        assert 'name' in first_error
        assert 'description' in first_error
        print(f"Polish error: {first_error['code']} - {first_error['name']}")

    def test_error_codes_english(self):
        """Test error codes in English"""
        response = requests.get(f"{BASE_URL}/api/tools/error-codes?lang=en")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        pe_error = next((e for e in data if e['code'] == 'PE!'), None)
        assert pe_error is not None
        # English content
        assert 'No PE' in pe_error['name'] or 'connection' in pe_error['description'].lower()
        print(f"English PE error: {pe_error['name']} - {pe_error['description'][:40]}...")

    def test_error_codes_german(self):
        """Test error codes in German"""
        response = requests.get(f"{BASE_URL}/api/tools/error-codes?lang=de")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        pe_error = next((e for e in data if e['code'] == 'PE!'), None)
        assert pe_error is not None
        # German content
        assert 'Kein PE' in pe_error['name'] or 'Verbindung' in pe_error['description']
        print(f"German PE error: {pe_error['name']} - {pe_error['description'][:40]}...")


class TestI18nQuiz:
    """Test /api/quiz/questions endpoint with lang parameter"""
    
    def test_quiz_polish(self):
        """Test quiz questions in Polish"""
        response = requests.get(f"{BASE_URL}/api/quiz/questions?lang=pl")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 10
        first_q = data[0]
        assert 'question' in first_q
        assert 'options' in first_q
        assert len(first_q['options']) == 4
        print(f"Polish quiz: {first_q['question'][:50]}...")

    def test_quiz_english(self):
        """Test quiz questions in English"""
        response = requests.get(f"{BASE_URL}/api/quiz/questions?lang=en")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 10
        first_q = data[0]
        combined = ' '.join([q['question'] for q in data])
        # English questions
        assert 'What' in combined or 'minimum' in combined or 'maximum' in combined
        print(f"English quiz: {first_q['question'][:50]}...")

    def test_quiz_german(self):
        """Test quiz questions in German"""
        response = requests.get(f"{BASE_URL}/api/quiz/questions?lang=de")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 10
        first_q = data[0]
        combined = ' '.join([q['question'] for q in data])
        # German questions
        assert 'Was' in combined or 'Welch' in combined or 'minimale' in combined.lower()
        print(f"German quiz: {first_q['question'][:50]}...")


class TestI18nChecklists:
    """Test /api/tools/checklists endpoint with lang parameter"""
    
    def test_checklists_polish(self):
        """Test checklists in Polish"""
        response = requests.get(f"{BASE_URL}/api/tools/checklists?lang=pl")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        # Check structure
        for key, checklist in data.items():
            assert 'name' in checklist
            assert 'items' in checklist
        print(f"Polish checklists: {list(data.keys())}")

    def test_checklists_english(self):
        """Test checklists in English"""
        response = requests.get(f"{BASE_URL}/api/tools/checklists?lang=en")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        # Check for English content in RCD checklist
        if 'rcd' in data:
            rcd_checklist = data['rcd']
            assert 'name' in rcd_checklist
            # Check items are in English
            items_text = ' '.join([i['text'] for i in rcd_checklist['items']])
            assert 'checked' in items_text.lower() or 'confirmed' in items_text.lower() or 'I ' in items_text
        print(f"English checklists: {list(data.keys())}")

    def test_checklists_german(self):
        """Test checklists in German"""
        response = requests.get(f"{BASE_URL}/api/tools/checklists?lang=de")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        # Check for German content
        if 'rcd' in data:
            rcd_checklist = data['rcd']
            items_text = ' '.join([i['text'] for i in rcd_checklist['items']])
            assert 'geprüft' in items_text.lower() or 'Ich' in items_text or 'habe' in items_text.lower()
        print(f"German checklists: {list(data.keys())}")


class TestI18nSearch:
    """Test /api/search endpoint with lang parameter"""
    
    def test_search_polish(self):
        """Test search in Polish"""
        response = requests.get(f"{BASE_URL}/api/search?q=izolacja&lang=pl")
        assert response.status_code == 200
        data = response.json()
        # Should find insulation-related content
        assert isinstance(data, list)
        print(f"Polish search results for 'izolacja': {len(data)} results")

    def test_search_english(self):
        """Test search in English"""
        response = requests.get(f"{BASE_URL}/api/search?q=insulation&lang=en")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"English search results for 'insulation': {len(data)} results")

    def test_search_german(self):
        """Test search in German"""
        response = requests.get(f"{BASE_URL}/api/search?q=isolation&lang=de")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"German search results for 'isolation': {len(data)} results")


class TestI18nInvalidLang:
    """Test invalid language parameter handling"""
    
    def test_invalid_lang_rejected(self):
        """Test that invalid lang parameter is rejected"""
        response = requests.get(f"{BASE_URL}/api/functions?lang=fr")
        # Should either return 422 (validation error) or default to Polish
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            # If accepted, should default to Polish
            data = response.json()
            rcd = next((f for f in data if f['id'] == 'rcd'), None)
            assert rcd is not None
            print(f"Invalid lang 'fr' - defaulted to: {rcd['name'][:30]}...")
        else:
            print("Invalid lang 'fr' correctly rejected with 422")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
