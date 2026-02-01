from fpdf import FPDF
from datetime import datetime

class GEOReporter(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "THE GEO AGENCY - CONFIDENTIAL VISIBILITY AUDIT", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()} | Generated on {datetime.now().strftime('%Y-%m-%d')}", 0, 0, "C")

    def generate_report(self, data, filename):
        self.add_page()
        
        # Brand Title
        self.set_font("Helvetica", "B", 24)
        self.set_text_color(44, 62, 80)
        self.cell(0, 20, f"Audit: {data['brand_name']}", 0, 1, "L")
        
        # Visibility Score
        self.set_font("Helvetica", "B", 16)
        score_color = (46, 204, 113) if data['visibility_score'] > 50 else (231, 76, 60)
        self.set_text_color(*score_color)
        self.cell(0, 10, f"AI Visibility Score: {data['visibility_score']}%", 0, 1, "L")
        
        self.ln(10)
        self.set_text_color(0, 0, 0)
        
        # Recommendations Section
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Strategic Recommendations:", 0, 1, "L")
        self.set_font("Helvetica", "", 11)
        for rec in data['recommendations']:
            self.multi_cell(0, 8, f"- {rec}")
            
        self.output(f"reports/{filename}")