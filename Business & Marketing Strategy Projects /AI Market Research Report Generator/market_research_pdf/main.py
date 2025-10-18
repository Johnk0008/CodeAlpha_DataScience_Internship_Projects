from report_analyzer import MarketResearchAnalyzer
from data_visualizer import ReportVisualizer
from pdf_generator import PDFReportGenerator
import os
from datetime import datetime

def ensure_directories():
    """Create necessary directories"""
    os.makedirs('outputs/reports', exist_ok=True)

def main():
    """Main function to generate market research report"""
    ensure_directories()
    
    print("🚀 AI Market Research Report Generator")
    print("=" * 50)
    
    # Sample data - you can modify this or create input system
    company_data = {
        'name': 'TechVision AI',
        'industry': 'technology',
        'description': """
TechVision AI is a leading artificial intelligence solutions provider 
specializing in computer vision and machine learning applications for 
enterprise clients. With a strong R&D team and innovative product suite, 
the company has established itself as a market challenger in the AI 
software sector. TechVision's solutions include automated quality control 
systems, predictive maintenance platforms, and intelligent document 
processing tools that help businesses improve efficiency and reduce costs.

The company leverages cutting-edge deep learning algorithms and cloud 
infrastructure to deliver scalable AI solutions across manufacturing, 
healthcare, and financial services industries. With a growing customer 
base and strategic partnerships with major cloud providers, TechVision 
is well-positioned to capitalize on the rapidly expanding AI market.
"""
    }
    
    # Uncomment below to use healthcare example instead
    """
    company_data = {
        'name': 'HealthSync Solutions',
        'industry': 'healthcare',
        'description': 'HealthSync Solutions is an innovative healthcare technology company developing integrated telemedicine platforms.'
    }
    """
    
    print(f"📊 Analyzing: {company_data['name']}")
    print(f"🏭 Industry: {company_data['industry'].title()}")
    print("⏳ Generating comprehensive market research report...")
    
    try:
        # Initialize components
        analyzer = MarketResearchAnalyzer()
        visualizer = ReportVisualizer()
        pdf_generator = PDFReportGenerator()
        
        # Generate analysis
        analysis = analyzer.generate_comprehensive_report(
            company_data['name'],
            company_data['industry'],
            company_data['description']
        )
        
        print("✅ Analysis completed. Generating visualizations...")
        
        # Generate visualizations
        visualizations = {
            'swot_chart': visualizer.create_swot_chart(
                analysis['swot_analysis'], 
                company_data['name']
            ),
            'market_growth': visualizer.create_market_growth_chart(
                analysis['market_analysis']
            ),
            'competitive_analysis': visualizer.create_competitive_analysis_chart(
                analysis['competitive_landscape'],
                company_data['name']
            ),
            'target_audience': visualizer.create_target_audience_chart(
                analysis['target_audience']
            ),
            'revenue_projections': visualizer.create_revenue_projections_chart(
                analysis['financial_metrics']
            ),
            'strategic_priority_matrix': visualizer.create_strategic_priority_matrix(
                analysis['strategic_recommendations']
            )
        }
        
        print("✅ Visualizations created. Generating PDF report...")
        
        # Generate PDF report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"market_research_{company_data['name'].replace(' ', '_')}_{timestamp}.pdf"
        output_path = f"outputs/reports/{output_filename}"
        
        pdf_path = pdf_generator.generate_report(analysis, visualizations, output_path)
        
        print("🎉 Report generated successfully!")
        print(f"📄 PDF Report: {pdf_path}")
        print(f"📏 Pages: 3-4 pages with comprehensive analysis")
        print("\n📋 Report Includes:")
        print("   • Executive Summary")
        print("   • Market Overview with Charts")
        print("   • Detailed SWOT Analysis")
        print("   • Competitive Landscape")
        print("   • Target Audience Analysis")
        print("   • Strategic Recommendations")
        print("   • Financial Projections")
        
    except Exception as e:
        print(f"❌ Error generating report: {str(e)}")
        raise

def generate_custom_report(company_name, industry, description):
    """Generate report with custom parameters"""
    ensure_directories()
    
    analyzer = MarketResearchAnalyzer()
    visualizer = ReportVisualizer()
    pdf_generator = PDFReportGenerator()
    
    # Generate analysis
    analysis = analyzer.generate_comprehensive_report(
        company_name,
        industry,
        description
    )
    
    # Generate visualizations
    visualizations = {
        'swot_chart': visualizer.create_swot_chart(
            analysis['swot_analysis'], 
            company_name
        ),
        'market_growth': visualizer.create_market_growth_chart(
            analysis['market_analysis']
        ),
        'competitive_analysis': visualizer.create_competitive_analysis_chart(
            analysis['competitive_landscape'],
            company_name
        ),
        'target_audience': visualizer.create_target_audience_chart(
            analysis['target_audience']
        ),
        'revenue_projections': visualizer.create_revenue_projections_chart(
            analysis['financial_metrics']
        ),
        'strategic_priority_matrix': visualizer.create_strategic_priority_matrix(
            analysis['strategic_recommendations']
        )
    }
    
    # Generate PDF
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"market_research_{company_name.replace(' ', '_')}_{timestamp}.pdf"
    output_path = f"outputs/reports/{output_filename}"
    
    pdf_path = pdf_generator.generate_report(analysis, visualizations, output_path)
    return pdf_path

if __name__ == "__main__":
    main()