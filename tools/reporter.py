from fpdf import FPDF
from datetime import datetime
from loguru import logger

class GEOReporter(FPDF):
    def header(self):
        """Professional Header on every page"""
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "THE GEO AGENCY - CONFIDENTIAL VISIBILITY AUDIT", 0, 1, "C")
        self.ln(5)

    def footer(self):
        """Professional Footer with page numbers"""
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()} | Generated on {datetime.now().strftime('%Y-%m-%d')}", 0, 0, "C")

    def generate_report(self, data, filename):
        """Main method to construct the multi-page report."""
        logger.info(f"Generating PDF report for {data['brand_name']}...")
        
        # --- PAGE 1: EXECUTIVE SUMMARY ---
        self.add_page()
        
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
        self.ln(5)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Strategic Recommendations:", 0, 1, "L")
        self.set_font("Helvetica", "", 12)
        for rec in data.get('recommendations', []):
            self.multi_cell(0, 8, f"- {rec}", border=0, align="L")
            self.ln(2)
        # --- PAGE 2: COMPETITIVE LANDSCAPE ---
        if 'leaderboard' in data and data['leaderboard']:
            self.add_competitor_page(data['leaderboard'])

        # --- PAGE 3: HALLUCINATIONS (IF ANY) ---
        if 'hallucinations' in data and data['hallucinations']:
            self.add_hallucination_page(data['hallucinations'])
            
        # Output the final PDF
        self.output(filename)
        logger.success(f"Report saved as {filename}")

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
        w_brand, w_cite, w_sent = 80, 50, 50
        
        self.cell(w_brand, 12, " Brand Name", 1, 0, "L", fill=True)
        self.cell(w_cite, 12, " Citations", 1, 0, "C", fill=True)
        self.cell(w_sent, 12, " Sentiment Score", 1, 1, "C", fill=True)
        
        # Table Body
        self.set_font("Helvetica", "", 11)
        for brand in leaderboard_data:
            self.cell(w_brand, 10, f" {brand['brand_name']}", 1)
            self.cell(w_cite, 10, str(brand['citation_count']), 1, 0, "C")
            sentiment = brand.get('sentiment_score', 0)
            self.cell(w_sent, 10, f"{int(sentiment * 100)}%", 1, 1, "C")

    def add_hallucination_page(self, errors):
        """Adds a warning page for AI misinformation."""
        self.add_page()
        self.set_text_color(231, 76, 60) # Warning Red
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 15, "CRITICAL: AI Hallucination & Misinformation Alerts", 0, 1, "L")
        self.ln(5)
        
        self.set_font("Helvetica", "", 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 8, "The following inaccuracies were detected in current AI model responses. These represent a high risk to brand trust and customer conversion.")
        self.ln(5)

        for error in errors:
            # Drawing a light red box for each error
            self.set_fill_color(255, 235, 235)
            # rect(x, y, w, h, style)
            current_x, current_y = self.get_x(), self.get_y()
            self.rect(current_x, current_y, 190, 25, "F")
            
            self.set_font("Helvetica", "B", 11)
            self.cell(0, 8, f"  Detected Error: {error['fact']}", 0, 1)
            self.set_font("Helvetica", "I", 10)
            self.cell(0, 8, f"  Correction Needed: {error['correction']}", 0, 1)
            self.ln(9) # Spacing between boxes
            
            #geneerate_battle_report
    def generate_battle_report(self, brand_a_data: dict, brand_b_data: dict, winner_summary: str, output_path: str):
        self.add_page()
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(40, 40, 40)
        
        # Header
        self.cell(0, 20, f"GEO BATTLE: {brand_a_data['brand_name']} vs {brand_b_data['brand_name']}", 0, 1, "C")
        self.ln(5)

        # Winner Summary Box
        self.set_fill_color(240, 245, 255)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "MARKET AUTHORITY SUMMARY", 1, 1, "L", fill=True)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 8, winner_summary, 1, "L", fill=False)
        self.ln(10)

        # Comparison Table
        with self.table(line_height=10, text_align="CENTER", width=190) as table:
            # Header Row
            header = table.row()
            header.cell("METRIC", style={"font_style": "B", "fill_color": (230, 230, 230)})
            header.cell(brand_a_data['brand_name'], style={"font_style": "B", "fill_color": (230, 230, 230)})
            header.cell(brand_b_data['brand_name'], style={"font_style": "B", "fill_color": (230, 230, 230)})

            # Visibility Score Row
            row = table.row()
            row.cell("AI Visibility Score")
            row.cell(f"{brand_a_data['visibility_score']}%")
            row.cell(f"{brand_b_data['visibility_score']}%")

            # Citations Row
            row = table.row()
            row.cell("Verified Citations")
            row.cell(str(len(brand_a_data['citations'])))
            row.cell(str(len(brand_b_data['citations'])))
            
            # Risk/Hallucinations Row
            row = table.row()
            row.cell("AI Brand Risks")
            row.cell(str(len(brand_a_data.get('hallucinations', []))))
            row.cell(str(len(brand_b_data.get('hallucinations', []))))

        self.output(output_path)