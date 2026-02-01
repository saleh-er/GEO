from fpdf import FPDF
from datetime import datetime

class GEOReporter(FPDF):
    def header(self):
        # Professional Header on every page
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "THE GEO AGENCY - CONFIDENTIAL VISIBILITY AUDIT", 0, 1, "C")
        self.ln(5)

    def footer(self):
        # Professional Footer with page numbers
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()} | Generated on {datetime.now().strftime('%Y-%m-%d')}", 0, 0, "C")

    def generate_report(self, data, filename):
        """Main method to construct the multi-page report."""
        self.add_page()
        
        # --- PAGE 1: EXECUTIVE SUMMARY ---
        # Brand Title
        self.set_font("Helvetica", "B", 26)
        self.set_text_color(44, 62, 80) # Dark Blue/Grey
        self.cell(0, 20, f"Audit: {data['brand_name']}", 0, 1, "L")
        
        # Visibility Score Section
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, "Current AI Visibility Status:", 0, 1, "L")
        
        # Color coding for the score
        score = data.get('visibility_score', 0)
        score_color = (46, 204, 113) if score > 50 else (231, 76, 60) # Green vs Red
        self.set_text_color(*score_color)
        self.set_font("Helvetica", "B", 40)
        self.cell(0, 25, f"{score}%", 0, 1, "L")
        
        self.ln(10)
        self.set_text_color(0, 0, 0)
        
        # Recommendations Section
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Strategic Recommendations:", 0, 1, "L")
        self.set_font("Helvetica", "", 11)
        for rec in data.get('recommendations', []):
            self.multi_cell(0, 8, f"- {rec}")
        
        # --- PAGE 2: COMPETITIVE LANDSCAPE ---
        if 'leaderboard' in data:
            self.add_competitor_page(data['leaderboard'])
            
        # Output the final PDF
        self.output(f"reports/{filename}")

    def add_competitor_page(self, leaderboard_data):
        """Adds a dedicated page comparing the client to competitors."""
        self.add_page()
        self.set_text_color(44, 62, 80)
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 15, "Competitive Landscape (AI Share of Voice)", 0, 1, "L")
        self.ln(5)
        
        # Table Header Styling
        self.set_fill_color(240, 240, 240)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "B", 11)
        
        # Column Widths
        w_brand = 80
        w_cite = 50
        w_sent = 50
        
        self.cell(w_brand, 12, " Brand Name", 1, 0, "L", fill=True)
        self.cell(w_cite, 12, " Citations", 1, 0, "C", fill=True)
        self.cell(w_sent, 12, " Sentiment Score", 1, 1, "C", fill=True)
        
        # Table Body
        self.set_font("Helvetica", "", 11)
        for brand in leaderboard_data:
            self.cell(w_brand, 10, f" {brand['brand_name']}", 1)
            self.cell(w_cite, 10, str(brand['citation_count']), 1, 0, "C")
            
            # Sentiment formatting
            sentiment = brand.get('sentiment_score', 0)
            self.cell(w_sent, 10, f"{int(sentiment * 100)}%", 1, 1, "C")