import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

from .language_manager import get_text as _t


# --- Font utilities ---------------------------------------------------------

UNICODE_FONT = "Helvetica"
UNICODE_FONT_BOLD = "Helvetica-Bold"
UNICODE_FONT_ITALIC = "Helvetica-Oblique"


def _ensure_unicode_fonts() -> None:
    """
    Register a TrueType font that supports UTF-8 (Romanian diacritics, etc.).

    On Windows this tries the system Arial TTFs; on Linux it falls back to
    DejaVuSans if available. If anything fails we fall back to the built-in
    Helvetica fonts.
    """
    global UNICODE_FONT, UNICODE_FONT_BOLD, UNICODE_FONT_ITALIC

    # Only attempt registration once
    if getattr(_ensure_unicode_fonts, "_done", False):
        return

    regular_path = None
    bold_path = None

    try:
        if os.name == "nt":
            # Common Windows font paths
            fonts_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
            regular_path = os.path.join(fonts_dir, "arial.ttf")
            bold_path = os.path.join(fonts_dir, "arialbd.ttf")
        else:
            # Typical Linux paths for DejaVu
            regular_candidates = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/dejavu/DejaVuSans.ttf",
            ]
            bold_candidates = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
            ]
            regular_path = next((p for p in regular_candidates if os.path.exists(p)), None)
            bold_path = next((p for p in bold_candidates if os.path.exists(p)), None)

        if regular_path and os.path.exists(regular_path):
            pdfmetrics.registerFont(TTFont("AppUnicode", regular_path))
            UNICODE_FONT = "AppUnicode"

        if bold_path and os.path.exists(bold_path):
            pdfmetrics.registerFont(TTFont("AppUnicode-Bold", bold_path))
            UNICODE_FONT_BOLD = "AppUnicode-Bold"
        else:
            # Fallback: synthetic bold if only regular exists
            UNICODE_FONT_BOLD = UNICODE_FONT

        # Italic fallback: use base font if no dedicated italic is registered
        UNICODE_FONT_ITALIC = UNICODE_FONT
    except Exception:
        # Leave defaults (Helvetica family) if anything goes wrong
        UNICODE_FONT = "Helvetica"
        UNICODE_FONT_BOLD = "Helvetica-Bold"
        UNICODE_FONT_ITALIC = "Helvetica-Oblique"
    finally:
        _ensure_unicode_fonts._done = True


class PsychologicalReportGenerator:
    def __init__(self):
        _ensure_unicode_fonts()
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
            fontName=UNICODE_FONT_BOLD,
        )
        
        # Header style
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=HexColor('#34495e'),
            fontName=UNICODE_FONT_BOLD,
        )
        
        # Subheader style
        self.subheader_style = ParagraphStyle(
            'CustomSubHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=15,
            textColor=HexColor('#7f8c8d'),
            fontName=UNICODE_FONT_BOLD,
        )
        
        # Body text style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            spaceBefore=3,
            textColor=black,
            fontName=UNICODE_FONT,
            alignment=TA_JUSTIFY
        )
        
        # Info style for patient details
        self.info_style = ParagraphStyle(
            'InfoStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            textColor=HexColor('#2c3e50'),
            fontName=UNICODE_FONT,
        )
        
        # Date style
        self.date_style = ParagraphStyle(
            'DateStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=HexColor('#7f8c8d'),
            fontName=UNICODE_FONT_ITALIC,
        )
    
    def create_header_footer(self, canvas, doc):
        """Create header and footer for each page."""
        canvas.saveState()
        
        # Header
        canvas.setFont(UNICODE_FONT_BOLD, 12)
        canvas.setFillColor(HexColor('#2c3e50'))
        header_title = _t('pdf.header_title', 'PersonDB Medical Records')
        canvas.drawString(72, letter[1] - 50, header_title)
        
        # Draw header line
        canvas.setStrokeColor(HexColor('#bdc3c7'))
        canvas.setLineWidth(1)
        canvas.line(72, letter[1] - 60, letter[0] - 72, letter[1] - 60)
        
        # Footer
        canvas.setFont(UNICODE_FONT, 9)
        canvas.setFillColor(HexColor('#7f8c8d'))
        generated_on = _t('pdf.generated_on', 'Generated on')
        page_label = _t('pdf.page', 'Page')
        canvas.drawString(72, 50, f"{generated_on} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        canvas.drawRightString(letter[0] - 72, 50, f"{page_label} {doc.page}")
        
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
        title = Paragraph(_t('pdf.report_title', 'Psychological Record Report'), self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Client Information Section
        story.append(Paragraph(_t('pdf.client_information', 'Client Information'), self.header_style))
        
        client_info = [
            [_t('pdf.client_name', 'Client Name:'), person_data[1] if len(person_data) > 1 else "N/A"],
            [_t('pdf.cnp', 'CNP:'), person_data[2] if len(person_data) > 2 else "N/A"],
            [_t('pdf.record_created', 'Record Created:'), person_data[3] if len(person_data) > 3 else "N/A"],
            [_t('pdf.last_updated', 'Last Updated:'), person_data[4] if len(person_data) > 4 else "N/A"],
            [_t('pdf.report_date', 'Report Date:'), datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ]
        
        client_table = Table(client_info, colWidths=[2*inch, 4*inch])
        client_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), UNICODE_FONT_BOLD),
            ('FONTNAME', (1, 0), (-1, -1), UNICODE_FONT),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [white, HexColor('#f8f9fa')])
        ]))
        
        story.append(client_table)
        story.append(Spacer(1, 30))
        
        # Psychological Assessments Section
        if assessments:
            story.append(Paragraph(_t('pdf.psychological_assessments', 'Psychological Assessments'), self.header_style))
            
            for i, assessment in enumerate(assessments):
                assessment_content = self._format_assessment(assessment, i + 1)
                story.append(KeepTogether(assessment_content))
                
                if i < len(assessments) - 1:  # Add spacer between assessments
                    story.append(Spacer(1, 15))
        
        # Therapy Sessions Section
        if consultations:
            story.append(Paragraph(_t('pdf.therapy_sessions', 'Therapy Sessions'), self.header_style))
            
            for i, consultation in enumerate(consultations):
                consultation_content = self._format_consultation(consultation, i + 1)
                story.append(KeepTogether(consultation_content))
                
                if i < len(consultations) - 1:  # Add spacer between consultations
                    story.append(Spacer(1, 15))
        
        # Summary section
        story.append(Spacer(1, 30))
        story.append(Paragraph(_t('pdf.summary', 'Summary'), self.header_style))
        
        summary_template = _t(
            'pdf.summary_text',
            "This medical record contains {assessment_count} assessment(s) and "
            "{consultation_count} consultation(s) for patient {patient_name}. "
            "This report was generated automatically from the PersonDB medical records system.",
        )
        summary_text = summary_template.format(
            assessment_count=len(assessments),
            consultation_count=len(consultations),
            patient_name=person_data[1] if len(person_data) > 1 else 'Unknown',
        )
        
        story.append(Paragraph(summary_text, self.body_style))
        
        # Build the PDF
        doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)
        
        return True
    
    def _format_assessment(self, assessment, number):
        """Format a single assessment for the report."""
        content = []
        
        # Assessment header
        assessment_id, assessment_date, chief_complaint, medical_history, physical_examination, diagnosis, treatment_plan, notes, created_at, updated_at = assessment
        
        header_template = _t('pdf.assessment_number', 'Assessment #{number}')
        header_text = f"{header_template.format(number=number)} - {assessment_date}"
        content.append(Paragraph(header_text, self.subheader_style))
        
        # Create assessment details table
        assessment_data = []
        
        if chief_complaint:
            assessment_data.append([_t('pdf.chief_complaint', 'Chief Complaint:'), chief_complaint])
        
        if medical_history:
            assessment_data.append([_t('pdf.medical_history', 'Medical History:'), medical_history])
        
        if physical_examination:
            assessment_data.append([_t('pdf.physical_examination', 'Physical Examination:'), physical_examination])
        
        if diagnosis:
            assessment_data.append([_t('pdf.diagnosis', 'Diagnosis:'), diagnosis])
        
        if treatment_plan:
            assessment_data.append([_t('pdf.treatment_plan', 'Treatment Plan:'), treatment_plan])
        
        if notes:
            assessment_data.append([_t('pdf.notes', 'Notes:'), notes])
        
        if assessment_data:
            assessment_table = Table(assessment_data, colWidths=[1.5*inch, 4.5*inch])
            assessment_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), HexColor('#e8f4fd')),
                ('TEXTCOLOR', (0, 0), (-1, -1), black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), UNICODE_FONT_BOLD),
                ('FONTNAME', (1, 0), (-1, -1), UNICODE_FONT),
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
        
        header_template = _t('pdf.consultation_number', 'Consultation #{number}')
        header_text = f"{header_template.format(number=number)} - {consultation_date} ({consultation_type})"
        content.append(Paragraph(header_text, self.subheader_style))
        
        # Create consultation details table
        consultation_data = []
        
        if symptoms:
            consultation_data.append([_t('pdf.symptoms', 'Symptoms:'), symptoms])
        
        if examination_findings:
            consultation_data.append([_t('pdf.examination_findings', 'Examination Findings:'), examination_findings])
        
        if recommendations:
            consultation_data.append([_t('pdf.recommendations', 'Recommendations:'), recommendations])
        
        if medications:
            consultation_data.append([_t('pdf.medications', 'Medications:'), medications])
        
        if next_appointment:
            consultation_data.append([_t('pdf.next_appointment', 'Next Appointment:'), next_appointment])
        
        if notes:
            consultation_data.append([_t('pdf.notes', 'Notes:'), notes])
        
        if consultation_data:
            consultation_table = Table(consultation_data, colWidths=[1.5*inch, 4.5*inch])
            consultation_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), HexColor('#fff3cd')),
                ('TEXTCOLOR', (0, 0), (-1, -1), black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), UNICODE_FONT_BOLD),
                ('FONTNAME', (1, 0), (-1, -1), UNICODE_FONT),
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
        _ensure_unicode_fonts()
        self.page_width, self.page_height = A4

    def _labeled_line(self, c, x, y, label, value, width):
        """Draw a label followed by a single-line field."""
        c.setFont(UNICODE_FONT, 9)
        c.drawString(x, y, label)
        label_width = c.stringWidth(label, UNICODE_FONT, 9)
        line_x = x + label_width + 4
        c.line(line_x, y - 2, line_x + width, y - 2)
        if value:
            c.setFont(UNICODE_FONT, 9)
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
        c.setFont(UNICODE_FONT_BOLD, 14)
        header_title = _t('medical_form.title', 'Fișă de Consultații Medicale - Adulți')
        c.drawCentredString(width / 2, y, header_title)
        y -= 30

        # Top row: county, locality
        county = form_data.get("county", "")
        locality = form_data.get("locality", "")
        self._labeled_line(c, margin, y, _t('medical_form.county_label', 'Județul') + ":", county, 140)
        self._labeled_line(c, margin + 220, y, _t('medical_form.locality_label', 'Localitatea') + ":", locality, 150)
        y -= 18

        # Health unit and number
        health_unit = form_data.get("health_unit", "")
        certificate_number = form_data.get("certificate_number", "")
        self._labeled_line(c, margin, y, _t('medical_form.health_unit_label', 'Unitatea sanitară') + ":", health_unit, width - 2 * margin - 150)
        self._labeled_line(c, width - margin - 150, y, _t('medical_form.certificate_label', 'Nr. certificat') + ":", certificate_number, 90)
        y -= 24

        # Patient info block
        name = person_data[1] if len(person_data) > 1 else ""
        cnp = person_data[2] if len(person_data) > 2 else ""
        registration_date = form_data.get("registration_date", "")

        self._labeled_line(c, margin, y, _t('pdf.client_name', 'Nume și prenume:') , name, width - 2 * margin - 160)
        y -= 18
        self._labeled_line(c, margin, y, _t('pdf.cnp', 'CNP:'), cnp, 180)
        self._labeled_line(c, margin + 260, y, _t('medical_form.registration_date_label', 'Data înregistrării'), registration_date, 120)
        y -= 22

        # Occupational info
        occupation = form_data.get("occupation", "")
        workplace = form_data.get("workplace", "")
        work_address = form_data.get("work_address", "")
        work_conditions = form_data.get("work_conditions", "")

        self._labeled_line(c, margin, y, _t('medical_form.occupation_label', 'Ocupația') + ":", occupation, 200)
        y -= 18
        self._labeled_line(c, margin, y, _t('medical_form.workplace_label', 'Locul de muncă') + ":", workplace, width - 2 * margin - 60)
        y -= 18
        self._labeled_line(c, margin, y, _t('medical_form.work_address_label', 'Adresa locului de muncă') + ":", work_address, width - 2 * margin - 120)
        y -= 18
        self._labeled_line(c, margin, y, _t('medical_form.work_conditions_label', 'Condiții de muncă') + ":", work_conditions, width - 2 * margin - 120)
        y -= 26

        # Antecedents block
        hereditary = form_data.get("hereditary_history", "")
        personal = form_data.get("personal_history", "")

        c.setFont(UNICODE_FONT_BOLD, 9)
        c.drawString(margin, y, _t('medical_form.hereditary_history_label', 'Antecedente heredo-colaterale'))
        y -= 14
        c.rect(margin, y - 40, width - 2 * margin, 40, stroke=1, fill=0)
        if hereditary:
            text = c.beginText(margin + 4, y - 4)
            text.setFont("Helvetica", 9)
            for line in str(hereditary).splitlines():
                text.textLine(line)
            c.drawText(text)
        y -= 50

        c.setFont(UNICODE_FONT_BOLD, 9)
        c.drawString(margin, y, _t('medical_form.personal_history_label', 'Antecedente personale fiziologice și patologice'))
        y -= 14
        c.rect(margin, y - 40, width - 2 * margin, 40, stroke=1, fill=0)
        if personal:
            text = c.beginText(margin + 4, y - 4)
            text.setFont("Helvetica", 9)
            for line in str(personal).splitlines():
                text.textLine(line)
            c.drawText(text)
        y -= 60

        # Consultations / investigations grid – mimic MED form with header + multiple rows
        c.setFont(UNICODE_FONT_BOLD, 10)
        c.drawString(margin, y, _t('medical_form.consultations_header', 'CONSULTAȚII, INVESTIGAȚII'))
        y -= 18

        table_top = y
        header_height = 16
        body_row_height = 18
        num_body_rows = 12  # visual grid similar to original sheet
        table_width = width - 2 * margin
        table_height = header_height + num_body_rows * body_row_height

        # Column relative widths (summing to 1.0)
        col_widths = [
            0.10,  # Data
            0.20,  # Simptome
            0.20,  # Diagnostic
            0.07,  # Cod
            0.28,  # Prescrieri / Recomandări
            0.07,  # Zile C.M.
            0.08,  # Nr. certificat
        ]

        # Outer border
        c.rect(margin, table_top - table_height, table_width, table_height, stroke=1, fill=0)

        # Vertical grid lines
        x = margin
        xs = [x]
        for frac in col_widths:
            x += table_width * frac
            xs.append(x)
            c.line(x, table_top, x, table_top - table_height)

        # Horizontal grid lines (header separator + body rows)
        header_y = table_top - header_height
        c.line(margin, header_y, margin + table_width, header_y)
        row_y = header_y
        for _ in range(num_body_rows):
            row_y -= body_row_height
            c.line(margin, row_y, margin + table_width, row_y)

        # Header labels
        headers = [
            _t('medical_form.col_date', 'Data'),
            _t('medical_form.col_symptoms', 'Simptome'),
            _t('medical_form.col_diagnosis', 'Diagnostic'),
            _t('medical_form.col_icd', 'Cod'),
            _t('medical_form.col_prescriptions', 'Prescrieri / Recomandări'),
            _t('medical_form.col_sick_days', 'Zile C.M.'),
            _t('medical_form.col_certificate', 'Nr. certificat'),
        ]

        c.setFont(UNICODE_FONT, 7.5)
        for i, header in enumerate(headers):
            col_x = xs[i] + 2
            # place text roughly centered vertically in header band
            c.drawString(col_x, table_top - header_height + 4, header)

        # First data row (rest remain blank lines)
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

        c.setFont(UNICODE_FONT, 8)
        first_row_top = header_y
        text_y = first_row_top - body_row_height + 4
        for i, value in enumerate(values):
            if not value:
                continue
            col_x = xs[i] + 2
            max_width = xs[i + 1] - xs[i] - 4
            # Simple wrapping for longer text inside the first data row
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
