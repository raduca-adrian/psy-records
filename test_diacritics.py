#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify diacritics handling in PDF generation
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.pdf_generator import PsychologicalReportGenerator

def test_diacritics():
    """Test PDF generation with Romanian diacritics"""
    
    # Sample data with Romanian characters
    person_data = (1, "Ion Popescu", "1985-03-15", "M", "București, România")
    
    assessments = [(
        1, "2024-01-15", 
        "Dureri de cap frecvente și stări de anxietate", 
        "Istoric de migrene în familie", 
        "Examen neurologic normal, tensiune arterială crescută",
        "Tulburare de anxietate generalizată",
        "Terapie cognitivă comportamentală, relaxare",
        "Observații: Pacientul arată semne de îmbunătățire"
    )]
    
    consultations = [(
        1, "2024-01-22", "Consultație de urmărire",
        "Dureri reduse, stări de anxietate mai rare",
        "Progres vizibil în gestionarea anxietății",
        "Continuarea terapiei, exerciții de respirație",
        "Magneziu 400mg zilnic",
        "2024-02-05",
        "Pacientul este foarte mulțumit de progres"
    )]
    
    try:
        # Test PDF generation in Romanian
        generator = PsychologicalReportGenerator(language_code='ro')
        output_path = os.path.join(os.path.dirname(__file__), 'test_romanian_diacritics.pdf')
        
        generator.generate_psychological_report(
            person_data=person_data,
            assessments=assessments,
            consultations=consultations,
            output_path=output_path
        )
        
        print(f"✅ Romanian PDF generated successfully: {output_path}")
        
        # Test PDF generation in English
        generator_en = PsychologicalReportGenerator(language_code='en')
        output_path_en = os.path.join(os.path.dirname(__file__), 'test_english.pdf')
        
        generator_en.generate_psychological_report(
            person_data=person_data,
            assessments=assessments,
            consultations=consultations,
            output_path=output_path_en
        )
        
        print(f"✅ English PDF generated successfully: {output_path_en}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing diacritics support in PDF generation...")
    success = test_diacritics()
    sys.exit(0 if success else 1)
