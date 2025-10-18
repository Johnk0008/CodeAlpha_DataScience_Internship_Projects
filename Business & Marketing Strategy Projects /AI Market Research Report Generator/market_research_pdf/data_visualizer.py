import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from io import BytesIO
import base64

class ReportVisualizer:
    def __init__(self):
        # Set available style - using basic matplotlib style
        plt.style.use('default')  # Fallback to default style
        try:
            # Try to use seaborn style if available
            plt.style.use('seaborn-v0_8-whitegrid')
        except:
            try:
                plt.style.use('seaborn-whitegrid')
            except:
                try:
                    plt.style.use('ggplot')
                except:
                    # Use basic matplotlib grid
                    plt.rcParams['grid.alpha'] = 0.3
                    plt.rcParams['grid.linestyle'] = '--'
        
        self.colors = {
            'primary': '#2C3E50',
            'secondary': '#3498DB',
            'accent': '#E74C3C',
            'success': '#27AE60',
            'warning': '#F39C12',
            'info': '#2980B9'
        }
    
    def create_swot_chart(self, swot_data, company_name):
        """Create SWOT analysis visualization"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f'SWOT Analysis - {company_name}', fontsize=16, fontweight='bold')
        
        categories = [
            ('Strengths', swot_data['strengths'], '#27AE60', axes[0, 0]),
            ('Weaknesses', swot_data['weaknesses'], '#E74C3C', axes[0, 1]),
            ('Opportunities', swot_data['opportunities'], '#3498DB', axes[1, 0]),
            ('Threats', swot_data['threats'], '#F39C12', axes[1, 1])
        ]
        
        for title, items, color, ax in categories:
            if items:  # Check if items list is not empty
                y_pos = np.arange(len(items))
                ax.barh(y_pos, [1] * len(items), color=color, alpha=0.7)
                ax.set_yticks(y_pos)
                ax.set_yticklabels([f'{i+1}. {item[:60]}...' if len(item) > 60 else f'{i+1}. {item}' 
                                  for i, item in enumerate(items)], fontsize=9)
                ax.set_title(title, fontweight='bold', color=color)
                ax.set_xlim(0, 1)
                ax.set_xticks([])
                
                # Add value labels
                for i, v in enumerate([1] * len(items)):
                    ax.text(v + 0.01, i, f'{i+1}', va='center', fontweight='bold')
            else:
                ax.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax.transAxes)
                ax.set_title(title, fontweight='bold', color=color)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_market_growth_chart(self, market_data):
        """Create market growth trajectory chart"""
        years = ['2023', '2024', '2025']
        values = [market_data['market_size'].get(year, 0) for year in years]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(years, values, color=self.colors['secondary'], alpha=0.8)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                   f'${value:.0f}B', ha='center', va='bottom', fontweight='bold')
        
        ax.set_title('Market Size Projection (2023-2025)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Market Size ($ Billions)')
        ax.set_xlabel('Year')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_competitive_analysis_chart(self, competition_data, company_name):
        """Create competitive landscape chart"""
        competitors = [comp['name'] for comp in competition_data['competitors']]
        market_shares = [comp['market_share'] for comp in competition_data['competitors']]
        
        # Highlight the analyzed company
        colors = [self.colors['accent'] if comp['name'] == company_name 
                 else self.colors['primary'] for comp in competition_data['competitors']]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(competitors, market_shares, color=colors, alpha=0.8)
        
        # Add percentage labels
        for bar, share in zip(bars, market_shares):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                   f'{share}%', ha='center', va='bottom', fontweight='bold')
        
        ax.set_title('Competitive Landscape - Market Share Distribution', 
                    fontsize=14, fontweight='bold')
        ax.set_ylabel('Market Share (%)')
        ax.set_xlabel('Competitors')
        plt.xticks(rotation=45, ha='right')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_target_audience_chart(self, audience_data):
        """Create target audience analysis chart"""
        segments = [seg['segment'] for seg in audience_data['primary_segments']]
        sizes = [seg['size_estimate'] for seg in audience_data['primary_segments']]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        y_pos = np.arange(len(segments))
        
        bars = ax.barh(y_pos, sizes, color=self.colors['info'], alpha=0.8)
        
        # Add value labels
        for bar, size in zip(bars, sizes):
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                   f'{size:.1f}M', va='center', fontweight='bold')
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(segments)
        ax.set_title('Target Audience Segment Sizes', fontsize=14, fontweight='bold')
        ax.set_xlabel('Estimated Market Size (Millions)')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_revenue_projections_chart(self, financial_data):
        """Create revenue projection chart"""
        years = list(financial_data['projected_revenue'].keys())
        revenues = list(financial_data['projected_revenue'].values())
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Line plot for revenue trend
        ax.plot(years, revenues, marker='o', linewidth=3, 
                color=self.colors['success'], markersize=8)
        
        # Fill under the line
        ax.fill_between(years, revenues, alpha=0.3, color=self.colors['success'])
        
        # Add value annotations
        for year, revenue in zip(years, revenues):
            ax.annotate(f'${revenue:.0f}M', 
                       xy=(year, revenue),
                       xytext=(0, 10),
                       textcoords='offset points',
                       ha='center', fontweight='bold')
        
        ax.set_title('Projected Revenue Growth', fontsize=14, fontweight='bold')
        ax.set_ylabel('Revenue ($ Millions)')
        ax.set_xlabel('Year')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def create_strategic_priority_matrix(self, recommendations):
        """Create strategic priority matrix"""
        if not recommendations:
            # Return a placeholder image if no recommendations
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.text(0.5, 0.5, 'No recommendations available', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)
            ax.set_title('Strategic Recommendations Priority Matrix', fontsize=14, fontweight='bold')
            return self._fig_to_base64(fig)
        
        # Categorize recommendations by priority and timeline
        priority_map = {'High': 3, 'Medium': 2, 'Low': 1}
        timeline_map = {'0-3 months': 1, '3-6 months': 2, '6-12 months': 3, '12+ months': 4}
        
        categories = []
        priorities = []
        timelines = []
        
        for rec in recommendations:
            categories.append(rec['category'])
            priorities.append(priority_map.get(rec['priority'], 2))
            timelines.append(timeline_map.get(rec['timeline'], 3))
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        scatter = ax.scatter(timelines, priorities, s=200, alpha=0.7, 
                           c=priorities, cmap='RdYlGn')
        
        # Add labels
        for i, category in enumerate(categories):
            ax.annotate(category, (timelines[i], priorities[i]),
                       xytext=(10, 5), textcoords='offset points',
                       fontsize=9, fontweight='bold')
        
        ax.set_xlabel('Implementation Timeline (Months)')
        ax.set_ylabel('Strategic Priority')
        ax.set_title('Strategic Recommendations - Priority Matrix', 
                    fontsize=14, fontweight='bold')
        
        # Set axis labels
        ax.set_yticks([1, 2, 3])
        ax.set_yticklabels(['Low', 'Medium', 'High'])
        ax.set_xticks([1, 2, 3, 4])
        ax.set_xticklabels(['0-3', '3-6', '6-12', '12+'])
        
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def _fig_to_base64(self, fig):
        """Convert matplotlib figure to base64 string"""
        try:
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode()
            plt.close(fig)  # Close the figure to free memory
            return img_str
        except Exception as e:
            print(f"Error creating chart: {e}")
            # Return a placeholder image in case of error
            return self._create_placeholder_image()
    
    def _create_placeholder_image(self):
        """Create a placeholder image when chart generation fails"""
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, 'Chart unavailable\nPlease check data', 
               ha='center', va='center', transform=ax.transAxes, fontsize=12)
        ax.set_facecolor('#f8f9fa')
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        return img_str