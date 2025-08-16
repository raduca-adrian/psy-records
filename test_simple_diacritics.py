#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test script to verify diacritics handling in PDF generation
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def test_diacritics_simple():
    """Simple test for diacritics in PDF"""
    
    try:
        # Create a simple PDF with Romanian text
        output_path = os.path.join(os.path.dirname(__file__), 'test_simple_diacritics.pdf')
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        
        # Use Times-Roman font which should support diacritics
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=18,
            spaceAfter=20,
            textColor=HexColor('#2c3e50'),
            alignment=TA_CENTER,
            fontName='Times-Bold',
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=3,
            textColor=black,
            fontName='Times-Roman',
            alignment=TA_LEFT
        )
        
        story = []
        
        # Test Romanian text with diacritics
        title_text = "Raport Medical - Test Caractere Diacritice"
        story.append(Paragraph(title_text, title_style))
        story.append(Spacer(1, 0.2*inch))
        
        romanian_text = """
        Pacient: Ion Popescu
        Vârstă: 35 ani
        Adresă: București, România
        
        Simptome: Dureri de cap frecvente și stări de anxietate
        Diagnostic: Tulburare de anxietate generalizată
        Tratament: Terapie cognitivă comportamentală și relaxare
        
        Observații: Pacientul arată semne de îmbunătățire în gestionarea anxietății.
        Recomandări: Continuarea terapiei cu exerciții de respirație.
        """
        
        story.append(Paragraph(romanian_text, body_style))
        
        # Build PDF
        doc.build(story)
        
        print(f"✅ PDF with diacritics generated successfully: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing simple diacritics support in PDF generation...")
    success = test_diacritics_simple()
    print("Test completed.")
