import pandas as pd
import numpy as np
from textblob import TextBlob
from datetime import datetime
import re

class MarketResearchAnalyzer:
    def __init__(self):
        self.industry_data = self._load_industry_templates()
        
    def _load_industry_templates(self):
        """Pre-loaded industry analysis templates"""
        return {
            'technology': {
                'trends': [
                    'Artificial Intelligence and Machine Learning Adoption',
                    'Cloud Computing and SaaS Solutions',
                    'Internet of Things (IoT) Expansion',
                    'Cybersecurity Advancements',
                    '5G and Edge Computing',
                    'Quantum Computing Development'
                ],
                'target_audience': [
                    'Enterprise Businesses (Large Corporations)',
                    'Small and Medium Businesses (SMBs)',
                    'Technology Developers and Engineers',
                    'Government and Public Sector',
                    'Educational Institutions',
                    'Individual Consumers'
                ],
                'common_competitors': [
                    'Established Tech Giants (Google, Microsoft, Amazon)',
                    'Specialized SaaS Companies',
                    'Open Source Alternatives',
                    'Legacy System Providers',
                    'International Competitors'
                ]
            },
            'healthcare': {
                'trends': [
                    'Telemedicine and Remote Healthcare',
                    'AI-Powered Diagnostics',
                    'Personalized Medicine',
                    'Wearable Health Technology',
                    'Electronic Health Records (EHR) Integration',
                    'Value-Based Care Models'
                ],
                'target_audience': [
                    'Hospitals and Healthcare Systems',
                    'Medical Professionals',
                    'Patients and Consumers',
                    'Pharmaceutical Companies',
                    'Insurance Providers',
                    'Research Institutions'
                ],
                'common_competitors': [
                    'Traditional Healthcare Providers',
                    'Pharmaceutical Giants',
                    'Health Tech Startups',
                    'Medical Device Companies',
                    'Telehealth Platforms'
                ]
            },
            'finance': {
                'trends': [
                    'Digital Banking Transformation',
                    'Blockchain and Cryptocurrency',
                    'AI in Fraud Detection',
                    'Robo-Advisors and Automated Investing',
                    'Open Banking APIs',
                    'Sustainable and ESG Investing'
                ],
                'target_audience': [
                    'Retail Banking Customers',
                    'Corporate Clients',
                    'Investment Firms',
                    'Small Business Owners',
                    'High-Net-Worth Individuals',
                    'International Markets'
                ],
                'common_competitors': [
                    'Traditional Banks',
                    'FinTech Startups',
                    'Payment Processors',
                    'Investment Platforms',
                    'International Financial Institutions'
                ]
            },
            'retail': {
                'trends': [
                    'E-commerce and Mobile Shopping',
                    'Personalized Customer Experiences',
                    'Omnichannel Retail Strategies',
                    'Sustainable and Ethical Sourcing',
                    'Augmented Reality Shopping',
                    'Supply Chain Optimization'
                ],
                'target_audience': [
                    'Millennial and Gen Z Consumers',
                    'Urban Professionals',
                    'Families and Households',
                    'Luxury Goods Shoppers',
                    'Value-Conscious Consumers',
                    'International Customers'
                ],
                'common_competitors': [
                    'E-commerce Giants (Amazon, Alibaba)',
                    'Brick-and-Mortar Chains',
                    'Specialty Retailers',
                    'Direct-to-Consumer Brands',
                    'Marketplace Platforms'
                ]
            }
        }
    
    def generate_comprehensive_report(self, company_name, industry, description, custom_data=None):
        """Generate complete market research analysis"""
        
        analysis = {
            'metadata': {
                'company_name': company_name,
                'industry': industry,
                'report_date': datetime.now().strftime("%B %d, %Y"),
                'report_period': 'Q4 2024 - Q1 2025'
            },
            'executive_summary': self._generate_executive_summary(company_name, industry, description),
            'swot_analysis': self._generate_detailed_swot(company_name, industry, description),
            'market_analysis': self._analyze_market(industry, description),
            'competitive_landscape': self._analyze_competition(industry, company_name),
            'target_audience': self._analyze_audience(industry, description),
            'strategic_recommendations': [],
            'financial_metrics': self._generate_financial_metrics(industry)
        }
        
        # Generate recommendations based on analysis
        analysis['strategic_recommendations'] = self._generate_strategic_recommendations(analysis)
        
        return analysis
    
    def _generate_executive_summary(self, company_name, industry, description):
        """Generate executive summary"""
        blob = TextBlob(description)
        sentiment = blob.sentiment.polarity
        
        summary = {
            'overview': f"{company_name} operates in the {industry} sector with a focus on {self._extract_key_themes(description)}.",
            'market_position': self._assess_market_position(description),
            'growth_potential': self._assess_growth_potential(industry, sentiment),
            'key_findings': [
                f"Strong potential in emerging {industry} technologies",
                "Increasing market demand for digital solutions",
                "Competitive landscape requires strategic differentiation"
            ]
        }
        
        return summary
    
    def _generate_detailed_swot(self, company_name, industry, description):
        """Generate comprehensive SWOT analysis"""
        
        # Analyze description for keywords and themes
        description_lower = description.lower()
        
        strengths = [
            "Innovative technology stack and digital capabilities",
            "Strong brand recognition in target markets",
            "Experienced leadership team with industry expertise",
            "Robust financial performance and growth trajectory",
            "Strategic partnerships and ecosystem relationships"
        ]
        
        weaknesses = [
            "Limited market share compared to industry leaders",
            "Dependence on specific customer segments or technologies",
            "Scalability challenges in rapid growth scenarios",
            "Need for continuous innovation to maintain competitiveness"
        ]
        
        opportunities = [
            f"Growing global demand for {industry} solutions",
            "Emerging market expansion possibilities",
            "Technological advancements creating new business models",
            "Changing consumer preferences favoring digital solutions",
            "Strategic acquisitions and partnership opportunities"
        ]
        
        threats = [
            "Intense competition from established players and startups",
            "Regulatory changes and compliance requirements",
            "Economic volatility affecting customer spending",
            "Rapid technological obsolescence risks",
            "Cybersecurity threats and data privacy concerns"
        ]
        
        # Customize based on description analysis
        if 'ai' in description_lower or 'artificial intelligence' in description_lower:
            strengths.append("Advanced AI/ML capabilities providing competitive edge")
            opportunities.append("Growing enterprise adoption of AI solutions")
        
        if 'cloud' in description_lower:
            strengths.append("Cloud-native architecture enabling scalability")
            opportunities.append("Increasing migration to cloud-based solutions")
        
        if 'startup' in description_lower or 'emerging' in description_lower:
            weaknesses.append("Limited resources compared to established competitors")
            opportunities.append("Agility and innovation as key differentiators")
        
        return {
            'strengths': strengths[:5],  # Limit to top 5
            'weaknesses': weaknesses[:4],
            'opportunities': opportunities[:5],
            'threats': threats[:4]
        }
    
    def _analyze_market(self, industry, description):
        """Analyze market trends and dynamics"""
        base_trends = self.industry_data.get(industry, {}).get('trends', [])
        
        # Market size estimates (simulated data)
        market_size = {
            '2023': np.random.uniform(500, 2000),  # $ billions
            '2024': np.random.uniform(550, 2200),
            '2025': np.random.uniform(600, 2500),
            'growth_rate': np.random.uniform(8, 15)  # Percentage
        }
        
        return {
            'market_size': market_size,
            'key_trends': base_trends,
            'growth_drivers': [
                'Digital transformation initiatives',
                'Changing consumer behaviors',
                'Regulatory environment changes',
                'Technological innovation pace',
                'Global economic conditions'
            ],
            'market_segments': [
                'Enterprise Solutions',
                'SMB Market',
                'Consumer Applications',
                'Government Sector',
                'International Markets'
            ]
        }
    
    def _analyze_competition(self, industry, company_name):
        """Analyze competitive landscape"""
        base_competitors = self.industry_data.get(industry, {}).get('common_competitors', [])
        
        # Simulate market share data
        competitors = []
        total_market_share = 100
        remaining_share = total_market_share
        
        for i, competitor in enumerate(base_competitors[:4]):
            share = np.random.uniform(10, min(30, remaining_share - (4-i)*5))
            competitors.append({
                'name': competitor,
                'market_share': round(share, 1),
                'strengths': ['Brand recognition', 'Financial resources', 'Customer base'],
                'weaknesses': ['Legacy systems', 'Slow innovation', 'High costs']
            })
            remaining_share -= share
        
        # Add the analyzed company
        company_share = round(remaining_share, 1)
        competitors.append({
            'name': company_name,
            'market_share': company_share,
            'strengths': ['Innovation', 'Agility', 'Customer focus'],
            'weaknesses': ['Limited scale', 'Brand awareness', 'Resources']
        })
        
        return {
            'competitors': competitors,
            'competitive_advantage': [
                "Superior technology and innovation",
                "Better customer experience and support",
                "Agile development and quick time-to-market",
                "Cost-effective solutions and pricing"
            ],
            'barriers_to_entry': [
                "High capital requirements for technology development",
                "Strong network effects in established platforms",
                "Regulatory compliance and certifications",
                "Customer switching costs and loyalty"
            ]
        }
    
    def _analyze_audience(self, industry, description):
        """Analyze target audience segments"""
        base_audience = self.industry_data.get(industry, {}).get('target_audience', [])
        
        # Simulate audience metrics
        audience_segments = []
        for segment in base_audience[:6]:
            audience_segments.append({
                'segment': segment,
                'size_estimate': np.random.uniform(5, 50),  # Millions
                'growth_rate': np.random.uniform(5, 20),   # Percentage
                'lifetime_value': np.random.uniform(1000, 10000),  # USD
                'acquisition_cost': np.random.uniform(100, 500)   # USD
            })
        
        return {
            'primary_segments': audience_segments,
            'customer_needs': [
                'Cost-effective solutions with clear ROI',
                'Seamless user experience and ease of use',
                'Reliable performance and uptime',
                'Strong security and data protection',
                'Scalability for future growth'
            ],
            'buying_behaviors': [
                'Increasing preference for subscription models',
                'Emphasis on vendor reputation and reviews',
                'Value-based purchasing decisions',
                'Demand for integrated solutions'
            ]
        }
    
    def _generate_financial_metrics(self, industry):
        """Generate simulated financial metrics"""
        base_revenue = {
            'technology': np.random.uniform(50, 500),
            'healthcare': np.random.uniform(30, 300),
            'finance': np.random.uniform(100, 800),
            'retail': np.random.uniform(200, 1000)
        }
        
        revenue = base_revenue.get(industry, 100)
        
        return {
            'projected_revenue': {
                '2024': round(revenue, 2),
                '2025': round(revenue * 1.15, 2),
                '2026': round(revenue * 1.32, 2)
            },
            'profit_margins': round(np.random.uniform(15, 35), 1),
            'customer_acquisition_cost': round(np.random.uniform(500, 2000), 2),
            'lifetime_value': round(np.random.uniform(5000, 20000), 2),
            'growth_metrics': {
                'monthly_growth_rate': round(np.random.uniform(3, 8), 1),
                'market_penetration': round(np.random.uniform(5, 25), 1),
                'customer_retention': round(np.random.uniform(75, 95), 1)
            }
        }
    
    def _generate_strategic_recommendations(self, analysis):
        """Generate strategic recommendations based on analysis"""
        recommendations = []
        
        swot = analysis['swot_analysis']
        market = analysis['market_analysis']
        competition = analysis['competitive_landscape']
        
        # Strength-based recommendations
        if len(swot['strengths']) >= 4:
            recommendations.append({
                'category': 'Growth Strategy',
                'recommendation': 'Leverage core strengths to expand into adjacent markets and customer segments',
                'priority': 'High',
                'timeline': '6-12 months'
            })
        
        # Opportunity-focused recommendations
        recommendations.append({
            'category': 'Market Expansion',
            'recommendation': f"Capitalize on growing {analysis['metadata']['industry']} market through strategic partnerships",
            'priority': 'High',
            'timeline': '3-6 months'
        })
        
        # Competitive positioning
        recommendations.append({
            'category': 'Competitive Advantage',
            'recommendation': 'Differentiate through superior customer experience and innovation',
            'priority': 'Medium',
            'timeline': '6-9 months'
        })
        
        # Technology and innovation
        recommendations.append({
            'category': 'Technology',
            'recommendation': 'Invest in AI and automation to improve efficiency and capabilities',
            'priority': 'High',
            'timeline': '9-12 months'
        })
        
        return recommendations
    
    def _extract_key_themes(self, description):
        """Extract key themes from company description"""
        themes = []
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['ai', 'artificial intelligence', 'machine learning']):
            themes.append('artificial intelligence')
        if any(word in description_lower for word in ['cloud', 'saas', 'software']):
            themes.append('cloud computing')
        if any(word in description_lower for word in ['mobile', 'app', 'application']):
            themes.append('mobile solutions')
        if any(word in description_lower for word in ['data', 'analytics', 'analysis']):
            themes.append('data analytics')
        
        return ', '.join(themes) if themes else 'digital transformation'
    
    def _assess_market_position(self, description):
        """Assess company's market position"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['leader', 'leading', 'dominant', 'top']):
            return "Market Leader"
        elif any(word in description_lower for word in ['challenger', 'emerging', 'growing', 'rapid']):
            return "Market Challenger"
        elif any(word in description_lower for word in ['niche', 'specialized', 'focused']):
            return "Niche Player"
        else:
            return "Emerging Competitor"
    
    def _assess_growth_potential(self, industry, sentiment):
        """Assess growth potential based on industry and sentiment"""
        growth_assessments = {
            'technology': "High growth potential driven by digital transformation",
            'healthcare': "Strong growth with increasing healthcare digitization",
            'finance': "Moderate to high growth with FinTech innovation",
            'retail': "Steady growth with e-commerce expansion"
        }
        
        return growth_assessments.get(industry, "Positive growth outlook")