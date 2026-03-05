import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib import colors

class PsychologicalReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Set up custom styles for the psychological report."""
        
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=20,
            spaceAfter=30,
            textColor=HexColor('#2c3e50'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Header style
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=HexColor('#34495e'),
            fontName='Helvetica-Bold'
        )
        
        # Subheader style
        self.subheader_style = ParagraphStyle(
            'CustomSubHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=15,
            textColor=HexColor('#7f8c8d'),
            fontName='Helvetica-Bold'
        )
        
        # Body text style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            spaceBefore=3,
            textColor=black,
            fontName='Helvetica',
            alignment=TA_JUSTIFY
        )
        
        # Info style for patient details
        self.info_style = ParagraphStyle(
            'InfoStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            textColor=HexColor('#2c3e50'),
            fontName='Helvetica'
        )
        
        # Date style
        self.date_style = ParagraphStyle(
            'DateStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=HexColor('#7f8c8d'),
            fontName='Helvetica-Oblique'
        )
    
    def create_header_footer(self, canvas, doc):
        """Create header and footer for each page."""
        canvas.saveState()
        
        # Header
        canvas.setFont('Helvetica-Bold', 12)
        canvas.setFillColor(HexColor('#2c3e50'))
        canvas.drawString(72, letter[1] - 50, "PersonDB Medical Records")
        
        # Draw header line
        canvas.setStrokeColor(HexColor('#bdc3c7'))
        canvas.setLineWidth(1)
        canvas.line(72, letter[1] - 60, letter[0] - 72, letter[1] - 60)
        
        # Footer
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(HexColor('#7f8c8d'))
        canvas.drawString(72, 50, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        canvas.drawRightString(letter[0] - 72, 50, f"Page {doc.page}")
        
        # Draw footer line
        canvas.line(72, 60, letter[0] - 72, 60)
        
        canvas.restoreState()
    
    def generate_client_report(self, person_data, assessments, consultations, output_path):
        """Generate a comprehensive psychological report for a client."""
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=100,
            bottomMargin=72
        )
        
        # Build the story (content)
        story = []
        
        # Title
        title = Paragraph("Psychological Record Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Client Information Section
        story.append(Paragraph("Client Information", self.header_style))
        
        client_info = [
            ["Client Name:", person_data[1] if len(person_data) > 1 else "N/A"],
            ["CNP:", person_data[2] if len(person_data) > 2 else "N/A"],
            ["Record Created:", person_data[3] if len(person_data) > 3 else "N/A"],
            ["Last Updated:", person_data[4] if len(person_data) > 4 else "N/A"],
            ["Report Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        ]
        
        client_table = Table(client_info, colWidths=[2*inch, 4*inch])
        client_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [white, HexColor('#f8f9fa')])
        ]))
        
        story.append(client_table)
        story.append(Spacer(1, 30))
        
        # Psychological Assessments Section
        if assessments:
            story.append(Paragraph("Psychological Assessments", self.header_style))
            
            for i, assessment in enumerate(assessments):
                assessment_content = self._format_assessment(assessment, i + 1)
                story.append(KeepTogether(assessment_content))
                
                if i < len(assessments) - 1:  # Add spacer between assessments
                    story.append(Spacer(1, 15))
        
        # Therapy Sessions Section
        if consultations:
            story.append(Paragraph("Therapy Sessions", self.header_style))
            
            for i, consultation in enumerate(consultations):
                consultation_content = self._format_consultation(consultation, i + 1)
                story.append(KeepTogether(consultation_content))
                
                if i < len(consultations) - 1:  # Add spacer between consultations
                    story.append(Spacer(1, 15))
        
        # Summary section
        story.append(Spacer(1, 30))
        story.append(Paragraph("Summary", self.header_style))
        
        summary_text = f"""
        This medical record contains {len(assessments)} assessment(s) and {len(consultations)} consultation(s) 
        for patient {person_data[1] if len(person_data) > 1 else 'Unknown'}. 
        This report was generated automatically from the PersonDB medical records system.
        """
        
        story.append(Paragraph(summary_text, self.body_style))
        
        # Build the PDF
        doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)
        
        return True
    
    def _format_assessment(self, assessment, number):
        """Format a single assessment for the report."""
        content = []
        
        # Assessment header
        assessment_id, assessment_date, chief_complaint, medical_history, physical_examination, diagnosis, treatment_plan, notes, created_at, updated_at = assessment
        
        header_text = f"Assessment #{number} - {assessment_date}"
        content.append(Paragraph(header_text, self.subheader_style))
        
        # Create assessment details table
        assessment_data = []
        
        if chief_complaint:
            assessment_data.append(["Chief Complaint:", chief_complaint])
        
        if medical_history:
            assessment_data.append(["Medical History:", medical_history])
        
        if physical_examination:
            assessment_data.append(["Physical Examination:", physical_examination])
        
        if diagnosis:
            assessment_data.append(["Diagnosis:", diagnosis])
        
        if treatment_plan:
            assessment_data.append(["Treatment Plan:", treatment_plan])
        
        if notes:
            assessment_data.append(["Notes:", notes])
        
        if assessment_data:
            assessment_table = Table(assessment_data, colWidths=[1.5*inch, 4.5*inch])
            assessment_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), HexColor('#e8f4fd')),
                ('TEXTCOLOR', (0, 0), (-1, -1), black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor('#f8f9fa'), white])
            ]))
            content.append(assessment_table)
        
        return content
    
    def _format_consultation(self, consultation, number):
        """Format a single consultation for the report."""
        content = []
        
        # Consultation header
        consultation_id, consultation_date, consultation_type, symptoms, examination_findings, recommendations, medications, next_appointment, notes, created_at, updated_at = consultation
        
        header_text = f"Consultation #{number} - {consultation_date} ({consultation_type})"
        content.append(Paragraph(header_text, self.subheader_style))
        
        # Create consultation details table
        consultation_data = []
        
        if symptoms:
            consultation_data.append(["Symptoms:", symptoms])
        
        if examination_findings:
            consultation_data.append(["Examination Findings:", examination_findings])
        
        if recommendations:
            consultation_data.append(["Recommendations:", recommendations])
        
        if medications:
            consultation_data.append(["Medications:", medications])
        
        if next_appointment:
            consultation_data.append(["Next Appointment:", next_appointment])
        
        if notes:
            consultation_data.append(["Notes:", notes])
        
        if consultation_data:
            consultation_table = Table(consultation_data, colWidths=[1.5*inch, 4.5*inch])
            consultation_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), HexColor('#fff3cd')),
                ('TEXTCOLOR', (0, 0), (-1, -1), black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor('#f8f9fa'), white])
            ]))
            content.append(consultation_table)
        
        return content

def generate_psychological_report(person_data, assessments, consultations, output_path):
    """Convenience function to generate a psychological report."""
    generator = PsychologicalReportGenerator()
    return generator.generate_client_report(person_data, assessments, consultations, output_path)


class MedicalConsultationFormGenerator:
    """
    Generator for adult medical consultation forms similar to the MED-style sheet.
    """

    def __init__(self):
        self.page_width, self.page_height = A4

    def _labeled_line(self, c, x, y, label, value, width):
        """Draw a label followed by a single-line field."""
        c.setFont("Helvetica", 9)
        c.drawString(x, y, label)
        label_width = c.stringWidth(label, "Helvetica", 9)
        line_x = x + label_width + 4
        c.line(line_x, y - 2, line_x + width, y - 2)
        if value:
            c.setFont("Helvetica", 9)
            c.drawString(line_x + 2, y, str(value))

    def generate_adult_form(self, person_data, form_data, output_path):
        """
        Generate an adult medical consultation PDF form.

        person_data: tuple from persons table
        form_data: dict with keys matching adult_medical_consultations columns
        """
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = self.page_width, self.page_height
        margin = 40
        y = height - margin

        # Header
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2, y, "FIȘĂ DE CONSULTAȚII MEDICALE - ADULȚI")
        y -= 30

        # Top row: county, locality
        county = form_data.get("county", "")
        locality = form_data.get("locality", "")
        self._labeled_line(c, margin, y, "Județul:", county, 140)
        self._labeled_line(c, margin + 220, y, "Localitatea:", locality, 150)
        y -= 18

        # Health unit and number
        health_unit = form_data.get("health_unit", "")
        certificate_number = form_data.get("certificate_number", "")
        self._labeled_line(c, margin, y, "Unitatea sanitară:", health_unit, width - 2 * margin - 150)
        self._labeled_line(c, width - margin - 150, y, "Nr.:", certificate_number, 90)
        y -= 24

        # Patient info block
        name = person_data[1] if len(person_data) > 1 else ""
        cnp = person_data[2] if len(person_data) > 2 else ""
        registration_date = form_data.get("registration_date", "")

        self._labeled_line(c, margin, y, "Nume și prenume:", name, width - 2 * margin - 160)
        y -= 18
        self._labeled_line(c, margin, y, "CNP:", cnp, 180)
        self._labeled_line(c, margin + 260, y, "Data înregistrării:", registration_date, 120)
        y -= 22

        # Occupational info
        occupation = form_data.get("occupation", "")
        workplace = form_data.get("workplace", "")
        work_address = form_data.get("work_address", "")
        work_conditions = form_data.get("work_conditions", "")

        self._labeled_line(c, margin, y, "Ocupația:", occupation, 200)
        y -= 18
        self._labeled_line(c, margin, y, "Locul de muncă:", workplace, width - 2 * margin - 60)
        y -= 18
        self._labeled_line(c, margin, y, "Adresa locului de muncă:", work_address, width - 2 * margin - 120)
        y -= 18
        self._labeled_line(c, margin, y, "Condiții de muncă:", work_conditions, width - 2 * margin - 120)
        y -= 26

        # Antecedents block
        hereditary = form_data.get("hereditary_history", "")
        personal = form_data.get("personal_history", "")

        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin, y, "Antecedente heredo-colaterale:")
        y -= 14
        c.rect(margin, y - 40, width - 2 * margin, 40, stroke=1, fill=0)
        if hereditary:
            text = c.beginText(margin + 4, y - 4)
            text.setFont("Helvetica", 9)
            for line in str(hereditary).splitlines():
                text.textLine(line)
            c.drawText(text)
        y -= 50

        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin, y, "Antecedente personale fiziologice și patologice:")
        y -= 14
        c.rect(margin, y - 40, width - 2 * margin, 40, stroke=1, fill=0)
        if personal:
            text = c.beginText(margin + 4, y - 4)
            text.setFont("Helvetica", 9)
            for line in str(personal).splitlines():
                text.textLine(line)
            c.drawText(text)
        y -= 60

        # Consultations table header
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin, y, "CONSULTAȚII, INVESTIGAȚII")
        y -= 18

        table_top = y
        row_height = 36
        table_width = width - 2 * margin

        # Column relative widths (summing to 1.0)
        col_widths = [
            0.10,  # Date
            0.20,  # Simptome
            0.20,  # Diagnostic
            0.07,  # Cod
            0.28,  # Prescrieri / Recomandări
            0.07,  # Zile C.M.
            0.08,  # Nr. certificat
        ]

        # Draw table outline
        c.rect(margin, table_top - row_height, table_width, row_height, stroke=1, fill=0)

        # Vertical lines
        x = margin
        xs = [x]
        for frac in col_widths:
            x += table_width * frac
            xs.append(x)
            c.line(x, table_top, x, table_top - row_height)

        # Header labels
        headers = [
            "Data",
            "Simptome",
            "Diagnostic",
            "Cod",
            "Prescrieri / Recomandări",
            "Zile C.M.",
            "Nr. certificat",
        ]

        c.setFont("Helvetica", 8)
        for i, header in enumerate(headers):
            col_x = xs[i] + 2
            c.drawString(col_x, table_top - 10, header)

        # Single data row
        consult_date = form_data.get("consultation_date", "")
        symptoms = form_data.get("symptoms", "")
        diagnosis = form_data.get("diagnosis", "")
        icd_code = form_data.get("icd_code", "")
        prescriptions = form_data.get("prescriptions", "") or form_data.get("recommendations", "")
        sick_days = form_data.get("sick_leave_days")
        sick_days_str = "" if sick_days is None else str(sick_days)
        cert_no = certificate_number

        values = [
            consult_date,
            symptoms,
            diagnosis,
            icd_code,
            prescriptions,
            sick_days_str,
            cert_no,
        ]

        c.setFont("Helvetica", 8)
        text_y = table_top - 22
        for i, value in enumerate(values):
            if not value:
                continue
            col_x = xs[i] + 2
            max_width = xs[i + 1] - xs[i] - 4
            # Simple wrapping for longer text
            text = c.beginText(col_x, text_y)
            text.setFont("Helvetica", 8)
            remaining = str(value)
            while remaining:
                # naive wrap by character length
                line = remaining[:80]
                remaining = remaining[80:]
                text.textLine(line)
            c.drawText(text)

        c.showPage()
        c.save()
        return True


def generate_medical_consultation_form(person_data, form_data, output_path):
    """Convenience function to generate an adult medical consultation form."""
    generator = MedicalConsultationFormGenerator()
    return generator.generate_adult_form(person_data, form_data, output_path)
