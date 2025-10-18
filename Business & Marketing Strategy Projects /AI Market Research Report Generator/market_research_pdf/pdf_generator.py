from fpdf import FPDF
import base64
from datetime import datetime
import os
import textwrap

class MarketResearchPDF(FPDF):
    def __init__(self):
        super().__init__()
        # Set larger margins to ensure text fits
        self.set_margins(left=15, top=15, right=15)
        self.set_auto_page_break(auto=True, margin=15)
        self.set_title("Market Research Report")
        self.set_author("AI Market Research Analyzer")
        
    def header(self):
        if self.page_no() == 1:
            return  # No header on cover page
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 10, 'Market Research Report', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, title, 0, 1, 'L', 1)
        self.ln(3)
    
    def safe_multi_cell(self, text, line_height=5, max_width=180):
        """Safely add text with proper width calculation"""
        effective_width = self.w - self.l_margin - self.r_margin
        if max_width < effective_width:
            effective_width = max_width
        
        # Split text into manageable chunks
        lines = text.split('\n')
        for line in lines:
            if len(line) > 0:
                # Use textwrap to break long lines
                wrapped_lines = textwrap.wrap(line, width=100)  # Conservative width
                for wrapped_line in wrapped_lines:
                    self.multi_cell(effective_width, line_height, wrapped_line)
            else:
                self.ln(line_height)
    
    def add_image(self, image_data, title=None, description=None, width=160):
        """Add base64 image to PDF with error handling"""
        try:
            # Save image temporarily
            temp_path = f"temp_image_{datetime.now().timestamp()}.png"
            with open(temp_path, "wb") as f:
                f.write(base64.b64decode(image_data))
            
            # Add image with centered alignment
            x_position = (self.w - width) / 2
            self.image(temp_path, x=x_position, w=width)
            
            # Add title if provided
            if title:
                self.set_font('helvetica', 'B', 10)
                self.ln(2)
                self.cell(0, 5, title, 0, 1, 'C')
            
            # Add description if provided
            if description:
                self.set_font('helvetica', 'I', 8)
                self.cell(0, 4, description, 0, 1, 'C')
                self.ln(2)
            else:
                self.ln(5)
            
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
        except Exception as e:
            print(f"Warning: Could not add image: {str(e)}")
            self.ln(10)
    
    def add_bullet_list(self, items, indent=5):
        """Add bullet point list with safe text handling"""
        self.set_font('helvetica', '', 9)
        for item in items:
            self.cell(indent)
            self.cell(5, 4, '-', 0, 0)
            self.safe_multi_cell(f' {item}', line_height=4, max_width=170)
            self.ln(1)
        self.ln(2)
    
    def add_numbered_list(self, items, indent=5):
        """Add numbered list with safe text handling"""
        self.set_font('helvetica', '', 9)
        for i, item in enumerate(items, 1):
            self.cell(indent)
            self.cell(8, 4, f'{i}.', 0, 0)
            self.safe_multi_cell(f' {item}', line_height=4, max_width=167)
            self.ln(1)
        self.ln(2)

class PDFReportGenerator:
    def __init__(self):
        self.pdf = MarketResearchPDF()
        
    def generate_report(self, analysis_data, visualizations, output_path):
        """Generate complete PDF report with comprehensive error handling"""
        try:
            # Add cover page
            self._add_cover_page(analysis_data)
            
            # Table of contents
            self._add_table_of_contents()
            
            # Executive Summary
            self._add_executive_summary(analysis_data)
            
            # Market Overview
            self._add_market_overview(analysis_data, visualizations)
            
            # SWOT Analysis
            self._add_swot_analysis(analysis_data, visualizations)
            
            # Competitive Analysis
            self._add_competitive_analysis(analysis_data, visualizations)
            
            # Target Audience
            self._add_target_audience(analysis_data, visualizations)
            
            # Strategic Recommendations
            self._add_strategic_recommendations(analysis_data, visualizations)
            
            # Save PDF
            self.pdf.output(output_path)
            print(f"✅ PDF successfully generated: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ PDF generation failed: {str(e)}")
            raise
    
    def _add_cover_page(self, analysis_data):
        self.pdf.add_page()
        
        # Title
        self.pdf.set_font('helvetica', 'B', 20)
        self.pdf.cell(0, 30, 'MARKET RESEARCH REPORT', 0, 1, 'C')
        
        # Company Name
        self.pdf.set_font('helvetica', 'B', 16)
        self.pdf.cell(0, 20, analysis_data['metadata']['company_name'], 0, 1, 'C')
        
        # Industry
        self.pdf.set_font('helvetica', 'I', 14)
        self.pdf.cell(0, 15, f"Industry: {analysis_data['metadata']['industry'].title()}", 0, 1, 'C')
        
        # Report Date
        self.pdf.set_font('helvetica', '', 12)
        self.pdf.cell(0, 10, f"Report Date: {analysis_data['metadata']['report_date']}", 0, 1, 'C')
        
        # Add some spacing
        self.pdf.ln(30)
        
        # Confidential notice
        self.pdf.set_font('helvetica', 'I', 9)
        self.pdf.cell(0, 10, 'CONFIDENTIAL - For Internal Use Only', 0, 1, 'C')
    
    def _add_table_of_contents(self):
        self.pdf.add_page()
        self.pdf.chapter_title('TABLE OF CONTENTS')
        self.pdf.ln(8)
        
        sections = [
            '1. Executive Summary...........................3',
            '2. Market Overview.............................4',
            '3. SWOT Analysis...............................5',
            '4. Competitive Landscape......................6',
            '5. Target Audience Analysis...................7',
            '6. Strategic Recommendations.................8'
        ]
        
        self.pdf.set_font('helvetica', '', 10)
        for section in sections:
            self.pdf.cell(0, 6, section, 0, 1)
            self.pdf.ln(1)
    
    def _add_executive_summary(self, analysis_data):
        self.pdf.add_page()
        self.pdf.chapter_title('1. EXECUTIVE SUMMARY')
        self.pdf.ln(3)
        
        summary = analysis_data['executive_summary']
        
        # Overview
        self.pdf.set_font('helvetica', 'B', 10)
        self.pdf.cell(0, 5, 'Overview', 0, 1)
        self.pdf.set_font('helvetica', '', 9)
        self.pdf.safe_multi_cell(summary['overview'], line_height=4)
        self.pdf.ln(2)
        
        # Market Position
        self.pdf.set_font('helvetica', 'B', 10)
        self.pdf.cell(0, 5, 'Market Position', 0, 1)
        self.pdf.set_font('helvetica', '', 9)
        self.pdf.safe_multi_cell(summary['market_position'], line_height=4)
        self.pdf.ln(2)
        
        # Growth Potential
        self.pdf.set_font('helvetica', 'B', 10)
        self.pdf.cell(0, 5, 'Growth Potential', 0, 1)
        self.pdf.set_font('helvetica', '', 9)
        self.pdf.safe_multi_cell(summary['growth_potential'], line_height=4)
        self.pdf.ln(2)
        
        # Key Findings
        self.pdf.set_font('helvetica', 'B', 10)
        self.pdf.cell(0, 5, 'Key Findings', 0, 1)
        self.pdf.add_bullet_list(summary['key_findings'])
    
    def _add_market_overview(self, analysis_data, visualizations):
        self.pdf.add_page()
        self.pdf.chapter_title('2. MARKET OVERVIEW')
        self.pdf.ln(3)
        
        market_data = analysis_data['market_analysis']
        financial_data = analysis_data['financial_metrics']
        
        # Market size information
        self.pdf.set_font('helvetica', 'B', 10)
        self.pdf.cell(0, 5, 'Market Size and Growth', 0, 1)
        self.pdf.set_font('helvetica', '', 9)
        
        market_size_text = f"Current market size: ${market_data['market_size']['2024']:.0f}B | "
        market_size_text += f"Growth rate: {market_data['market_size']['growth_rate']:.1f}% annually"
        self.pdf.safe_multi_cell(market_size_text, line_height=4)
        self.pdf.ln(2)
        
        # Add market growth chart
        if 'market_growth' in visualizations:
            self.pdf.add_image(visualizations['market_growth'], 
                             "Market Size Projection 2023-2025")
        
        # Key trends
        self.pdf.set_font('helvetica', 'B', 10)
        self.pdf.cell(0, 5, 'Key Market Trends', 0, 1)
        self.pdf.add_bullet_list(market_data['key_trends'][:3])  # Limit to 3 items
        
        # Financial metrics
        self.pdf.set_font('helvetica', 'B', 10)
        self.pdf.cell(0, 5, 'Financial Projections', 0, 1)
        self.pdf.set_font('helvetica', '', 9)
        
        revenue_text = f"2025 Projected Revenue: ${financial_data['projected_revenue']['2025']:.0f}M | "
        revenue_text += f"Profit Margin: {financial_data['profit_margins']:.1f}%"
        self.pdf.safe_multi_cell(revenue_text, line_height=4)
        
        # Add revenue chart
        if 'revenue_projections' in visualizations:
            self.pdf.add_image(visualizations['revenue_projections'], 
                             "Revenue Growth Projection")
    
    def _add_swot_analysis(self, analysis_data, visualizations):
        self.pdf.add_page()
        self.pdf.chapter_title('3. SWOT ANALYSIS')
        self.pdf.ln(3)
        
        swot_data = analysis_data['swot_analysis']
        
        # Add SWOT chart
        if 'swot_chart' in visualizations:
            self.pdf.add_image(visualizations['swot_chart'], 
                             "SWOT Analysis Matrix")
        
        # Detailed SWOT points - limit items to prevent overflow
        categories = [
            ('STRENGTHS', swot_data['strengths'][:2]),  # Limit to 2 items each
            ('WEAKNESSES', swot_data['weaknesses'][:2]),
            ('OPPORTUNITIES', swot_data['opportunities'][:2]),
            ('THREATS', swot_data['threats'][:2])
        ]
        
        for title, items in categories:
            self.pdf.set_font('helvetica', 'B', 10)
            self.pdf.cell(0, 5, title, 0, 1)
            self.pdf.add_bullet_list(items)
    
    def _add_competitive_analysis(self, analysis_data, visualizations):
        self.pdf.add_page()
        self.pdf.chapter_title('4. COMPETITIVE LANDSCAPE')
        self.pdf.ln(3)
        
        competition_data = analysis_data['competitive_landscape']
        
        # Add competitive analysis chart
        if 'competitive_analysis' in visualizations:
            self.pdf.add_image(visualizations['competitive_analysis'], 
                             "Market Share Distribution")
        
        # Competitive advantages
        self.pdf.set_font('helvetica', 'B', 10)
        self.pdf.cell(0, 5, 'Competitive Advantages', 0, 1)
        self.pdf.add_bullet_list(competition_data['competitive_advantage'][:3])  # Limit items
        
        # Key competitors
        self.pdf.set_font('helvetica', 'B', 10)
        self.pdf.cell(0, 5, 'Key Competitors', 0, 1)
        self.pdf.set_font('helvetica', '', 9)
        
        for comp in competition_data['competitors'][:3]:  # Limit to 3 competitors
            competitor_text = f"{comp['name']}: {comp['market_share']}% market share"
            self.pdf.safe_multi_cell(competitor_text, line_height=4)
            self.pdf.ln(1)  # Fixed: Use self.pdf.ln() instead of self.ln()
    
    def _add_target_audience(self, analysis_data, visualizations):
        self.pdf.add_page()
        self.pdf.chapter_title('5. TARGET AUDIENCE ANALYSIS')
        self.pdf.ln(3)
        
        audience_data = analysis_data['target_audience']
        
        # Add audience chart
        if 'target_audience' in visualizations:
            self.pdf.add_image(visualizations['target_audience'], 
                             "Target Audience Segments")
        
        # Key customer segments
        self.pdf.set_font('helvetica', 'B', 10)
        self.pdf.cell(0, 5, 'Primary Customer Segments', 0, 1)
        self.pdf.set_font('helvetica', '', 9)
        
        for segment in audience_data['primary_segments'][:3]:  # Limit to 3 segments
            segment_text = f"{segment['segment']} ({segment['size_estimate']:.1f}M customers)"
            self.pdf.safe_multi_cell(segment_text, line_height=4)
            self.pdf.ln(1)  # Fixed: Use self.pdf.ln() instead of self.ln()
        
        # Customer needs
        self.pdf.set_font('helvetica', 'B', 10)
        self.pdf.cell(0, 5, 'Key Customer Needs', 0, 1)
        self.pdf.add_bullet_list(audience_data['customer_needs'][:3])  # Limit items
    
    def _add_strategic_recommendations(self, analysis_data, visualizations):
        self.pdf.add_page()
        self.pdf.chapter_title('6. STRATEGIC RECOMMENDATIONS')
        self.pdf.ln(3)
        
        recommendations = analysis_data['strategic_recommendations']
        
        # Add priority matrix
        if 'strategic_priority_matrix' in visualizations:
            self.pdf.add_image(visualizations['strategic_priority_matrix'], 
                             "Recommendations Priority Matrix")
        
        # Detailed recommendations
        self.pdf.set_font('helvetica', 'B', 10)
        self.pdf.cell(0, 5, 'Actionable Recommendations', 0, 1)
        
        for i, rec in enumerate(recommendations[:4], 1):  # Limit to 4 recommendations
            self.pdf.set_font('helvetica', 'B', 9)
            rec_title = f'{i}. {rec["category"]}'
            self.pdf.safe_multi_cell(rec_title, line_height=4)
            
            self.pdf.set_font('helvetica', '', 8)
            self.pdf.safe_multi_cell(rec['recommendation'], line_height=3)
            
            self.pdf.set_font('helvetica', 'I', 8)
            priority_text = f'Priority: {rec["priority"]} | Timeline: {rec["timeline"]}'
            self.pdf.safe_multi_cell(priority_text, line_height=3)
            self.pdf.ln(2)