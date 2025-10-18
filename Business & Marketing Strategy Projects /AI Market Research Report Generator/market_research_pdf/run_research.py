#!/usr/bin/env python3
"""
Simple Market Research Report Generator
Run this file to generate a complete 3-4 page PDF report
"""

import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from report_analyzer import MarketResearchAnalyzer
from data_visualizer import ReportVisualizer
from pdf_generator import PDFReportGenerator

def create_sample_report():
    """Create a sample market research report"""
    
    # Ensure output directory exists
    os.makedirs('outputs/reports', exist_ok=True)
    
    print("🔍 Generating Market Research Report...")
    print("=" * 50)
    
    # Sample company analysis
    companies = [
        {
            'name': 'TechVision AI',
            'industry': 'technology',
            'description': """
TechVision AI is a leading artificial intelligence solutions provider specializing in computer vision and machine learning applications for enterprise clients. The company offers innovative AI solutions for quality control, predictive maintenance, and intelligent document processing. With strong R&D capabilities and cloud-native architecture, TechVision serves manufacturing, healthcare, and financial services industries.
"""
        },
        {
            'name': 'HealthSync Solutions', 
            'industry': 'healthcare',
            'description': """
HealthSync Solutions develops integrated telemedicine platforms and patient management systems for healthcare providers. The company's AI-powered solutions enable remote patient monitoring, virtual consultations, and streamlined healthcare operations. HealthSync focuses on improving patient outcomes through technology innovation in the digital health space.
"""
        }
    ]
    
    for company in companies[:1]:  # Generate for first company
        print(f"📊 Analyzing: {company['name']}")
        print(f"🏭 Industry: {company['industry']}")
        
        try:
            # Initialize components
            analyzer = MarketResearchAnalyzer()
            visualizer = ReportVisualizer() 
            pdf_generator = PDFReportGenerator()
            
            # Generate analysis
            analysis = analyzer.generate_comprehensive_report(
                company['name'],
                company['industry'], 
                company['description']
            )
            
            print("✅ Analysis completed")
            
            # Create visualizations
            print("📈 Generating charts...")
            visualizations = {
                'swot_chart': visualizer.create_swot_chart(analysis['swot_analysis'], company['name']),
                'market_growth': visualizer.create_market_growth_chart(analysis['market_analysis']),
                'competitive_analysis': visualizer.create_competitive_analysis_chart(analysis['competitive_landscape'], company['name']),
                'target_audience': visualizer.create_target_audience_chart(analysis['target_audience']),
                'revenue_projections': visualizer.create_revenue_projections_chart(analysis['financial_metrics']),
                'strategic_priority_matrix': visualizer.create_strategic_priority_matrix(analysis['strategic_recommendations'])
            }
            
            # Generate PDF
            print("📄 Creating PDF report...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"outputs/reports/market_research_{company['name'].replace(' ', '_')}_{timestamp}.pdf"
            
            pdf_path = pdf_generator.generate_report(analysis, visualizations, output_path)
            
            print(f"🎉 SUCCESS: Report generated at {pdf_path}")
            print(f"📏 Report: 3-4 pages with 6 detailed charts")
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            return False
    
    return True

if __name__ == "__main__":
    success = create_sample_report()
    if success:
        print("\n✨ Market Research Report completed successfully!")
    else:
        print("\n💥 Report generation failed!")
        sys.exit(1)