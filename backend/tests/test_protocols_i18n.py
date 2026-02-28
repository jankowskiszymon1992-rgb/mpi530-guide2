"""
Test Protocol Translations (Guides, Templates, Examples) - EN/DE support
Testing iteration 5 - Protocol section translations
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestProtocolGuides:
    """Test /api/protocols/guides endpoints with lang parameter"""
    
    def test_guides_default_returns_polish(self):
        """Default (no lang param) returns Polish guides"""
        response = requests.get(f"{BASE_URL}/api/protocols/guides")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4  # 4 guides
        # First guide in Polish has "Podstawy" in name
        assert "Podstawy" in data[0]["name"]
    
    def test_guides_lang_en_returns_english(self):
        """lang=en returns 4 guides with English names"""
        response = requests.get(f"{BASE_URL}/api/protocols/guides", params={"lang": "en"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4
        # Check English names exist
        guide_names = [g["name"] for g in data]
        assert "Sonel Reports Plus - Basics" in guide_names
        assert "Downloading results from the meter" in guide_names
        assert "Generating a protocol" in guide_names
        assert "Migration from Sonel PE6" in guide_names
    
    def test_guides_lang_de_returns_german(self):
        """lang=de returns 4 guides with German names"""
        response = requests.get(f"{BASE_URL}/api/protocols/guides", params={"lang": "de"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4
        # Check German names exist
        guide_names = [g["name"] for g in data]
        assert "Sonel Reports Plus - Grundlagen" in guide_names
        assert "Ergebnisse vom Messgerät herunterladen" in guide_names
        assert "Protokoll erstellen" in guide_names
        assert "Migration von Sonel PE6" in guide_names
    
    def test_single_guide_en(self):
        """Get single guide by ID in English"""
        response = requests.get(f"{BASE_URL}/api/protocols/guides/reports_plus_basics", params={"lang": "en"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Sonel Reports Plus - Basics"
        assert "How to get started" in data["description"]
        # Check steps are in English
        assert len(data["steps"]) > 0
        assert data["steps"][0]["title"] == "Software installation"
    
    def test_single_guide_de(self):
        """Get single guide by ID in German"""
        response = requests.get(f"{BASE_URL}/api/protocols/guides/generate_protocol", params={"lang": "de"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Protokoll erstellen"
        # Check steps are in German
        assert data["steps"][0]["title"] == "Ergebnisvollständigkeit prüfen"


class TestProtocolTemplates:
    """Test /api/protocols/templates endpoints with lang parameter"""
    
    def test_templates_default_returns_polish(self):
        """Default (no lang param) returns Polish templates"""
        response = requests.get(f"{BASE_URL}/api/protocols/templates")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5  # 5 templates
        # First template in Polish
        assert "Protokół odbioru" in data[0]["name"]
    
    def test_templates_lang_en_returns_english(self):
        """lang=en returns 5 templates with English names and measurements"""
        response = requests.get(f"{BASE_URL}/api/protocols/templates", params={"lang": "en"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        # Check English names
        template_names = [t["name"] for t in data]
        assert "Electrical installation acceptance protocol" in template_names
        assert "Periodic inspection protocol" in template_names
        assert "RCD testing protocol" in template_names
        assert "Earth resistance measurement protocol" in template_names
        assert "Illumination measurement protocol" in template_names
        # Check measurements are in English
        reception = next(t for t in data if t["id"] == "reception")
        assert "Installation visual inspection" in reception["measurements"]
        assert "Protective conductor (PE) continuity" in reception["measurements"]
    
    def test_templates_lang_de_returns_german(self):
        """lang=de returns 5 templates with German names"""
        response = requests.get(f"{BASE_URL}/api/protocols/templates", params={"lang": "de"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        # Check German names
        template_names = [t["name"] for t in data]
        assert "Abnahmeprotokoll Elektroinstallation" in template_names
        assert "Protokoll der periodischen Prüfung" in template_names
        assert "RCD-Prüfprotokoll" in template_names
        # Check measurements are in German
        reception = next(t for t in data if t["id"] == "reception")
        assert "Sichtprüfung der Anlage" in reception["measurements"]
        assert "Durchgängigkeit der Schutzleiter (PE)" in reception["measurements"]


class TestProtocolExamples:
    """Test /api/protocols/examples endpoints with lang parameter"""
    
    def test_examples_default_returns_polish(self):
        """Default (no lang param) returns Polish examples"""
        response = requests.get(f"{BASE_URL}/api/protocols/examples")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5  # 5 examples
        # First example in Polish has "Przykład" in name
        assert "Przykład" in data[0]["name"]
    
    def test_examples_lang_en_returns_english(self):
        """lang=en returns 5 examples with English content"""
        response = requests.get(f"{BASE_URL}/api/protocols/examples", params={"lang": "en"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        # Check English names
        example_names = [e["name"] for e in data]
        assert "Example: Apartment acceptance protocol" in example_names
        assert "Example: Periodic inspection protocol" in example_names
        assert "Example: RCD testing protocol" in example_names
        assert "Example: Earth resistance protocol" in example_names
        assert "Example: Illumination measurement protocol" in example_names
        # Check conclusions have English terms
        for ex in data:
            assert "POSITIVE" in ex["conclusion"] or "NEGATIVE" in ex["conclusion"]
    
    def test_examples_lang_de_returns_german(self):
        """lang=de returns 5 examples with German content"""
        response = requests.get(f"{BASE_URL}/api/protocols/examples", params={"lang": "de"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        # Check German names
        example_names = [e["name"] for e in data]
        assert "Beispiel: Wohnungsabnahmeprotokoll" in example_names
        assert "Beispiel: Periodisches Prüfprotokoll" in example_names
        # Check conclusions have German terms
        for ex in data:
            assert "POSITIV" in ex["conclusion"] or "NEGATIV" in ex["conclusion"]
    
    def test_single_example_en(self):
        """Get single example by ID in English - example_reception"""
        response = requests.get(f"{BASE_URL}/api/protocols/examples/example_reception", params={"lang": "en"})
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "example_reception"
        assert "Example: Apartment acceptance protocol" in data["name"]
        assert "POSITIVE" in data["conclusion"]
        # Check measurements have English content
        assert len(data["measurements"]) > 0
        points = [m["point"] for m in data["measurements"]]
        assert "Living room" in points or "Kitchen" in points
        # Check recommendations are in English
        assert "Periodic inspection recommended" in data["recommendations"][0] or "5 years" in data["recommendations"][0]
    
    def test_single_example_de(self):
        """Get single example by ID in German"""
        response = requests.get(f"{BASE_URL}/api/protocols/examples/example_periodic", params={"lang": "de"})
        assert response.status_code == 200
        data = response.json()
        assert "Beispiel: Periodisches" in data["name"]
        assert "NEGATIV" in data["conclusion"]
        # Check German measurement points
        points = [m["point"] for m in data["measurements"]]
        assert "Hauptverteilung" in points or "Büro" in " ".join(points)
    
    def test_example_with_fail_results_en(self):
        """Verify example with FAIL results shows English content"""
        response = requests.get(f"{BASE_URL}/api/protocols/examples/example_periodic", params={"lang": "en"})
        assert response.status_code == 200
        data = response.json()
        # This example has a FAIL result
        fail_measurements = [m for m in data["measurements"] if m["status"] == "FAIL"]
        assert len(fail_measurements) > 0
        # Conclusion should be NEGATIVE in English
        assert "NEGATIVE" in data["conclusion"]
        # Recommendations should be in English
        assert any("Loop impedance" in r or "Zs" in r for r in data["recommendations"])


class TestInvalidParameters:
    """Test error handling for invalid parameters"""
    
    def test_invalid_lang_rejected(self):
        """Invalid lang parameter should be rejected"""
        response = requests.get(f"{BASE_URL}/api/protocols/guides", params={"lang": "fr"})
        assert response.status_code == 422  # Validation error
    
    def test_nonexistent_guide_404(self):
        """Non-existent guide ID returns 404"""
        response = requests.get(f"{BASE_URL}/api/protocols/guides/nonexistent_guide")
        assert response.status_code == 404
    
    def test_nonexistent_example_404(self):
        """Non-existent example ID returns 404"""
        response = requests.get(f"{BASE_URL}/api/protocols/examples/nonexistent_example")
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
