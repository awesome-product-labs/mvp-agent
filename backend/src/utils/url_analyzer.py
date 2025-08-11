"""
URL Analysis service for extracting context from reference websites.
"""
import logging
import re
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from pydantic import HttpUrl

from ..api.project_models import URLContext

logger = logging.getLogger(__name__)


class URLAnalyzer:
    """Service for analyzing URLs and extracting contextual information."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Common tech stack indicators
        self.tech_indicators = {
            'react': ['react', 'jsx', 'create-react-app'],
            'vue': ['vue.js', 'vuejs', 'nuxt'],
            'angular': ['angular', 'ng-', '@angular'],
            'bootstrap': ['bootstrap', 'bs-'],
            'tailwind': ['tailwindcss', 'tailwind'],
            'jquery': ['jquery', '$'],
            'wordpress': ['wp-content', 'wordpress'],
            'shopify': ['shopify', 'myshopify'],
            'stripe': ['stripe', 'js.stripe.com'],
            'paypal': ['paypal'],
            'google-analytics': ['google-analytics', 'gtag'],
            'firebase': ['firebase', 'firebaseapp'],
            'aws': ['amazonaws', 'cloudfront'],
            'cloudflare': ['cloudflare'],
        }
        
        # UI pattern indicators
        self.ui_patterns = {
            'navigation': ['navbar', 'nav-', 'menu', 'header'],
            'hero_section': ['hero', 'banner', 'jumbotron'],
            'cards': ['card', 'tile', 'box'],
            'modals': ['modal', 'popup', 'dialog'],
            'forms': ['form', 'input', 'submit'],
            'tables': ['table', 'grid', 'list'],
            'carousel': ['carousel', 'slider', 'swiper'],
            'tabs': ['tab', 'accordion'],
            'sidebar': ['sidebar', 'aside'],
            'footer': ['footer'],
        }
        
        # Business model indicators
        self.business_models = {
            'ecommerce': ['shop', 'cart', 'buy', 'price', 'product', 'checkout'],
            'saas': ['subscription', 'plan', 'pricing', 'trial', 'dashboard'],
            'marketplace': ['seller', 'buyer', 'listing', 'marketplace'],
            'social': ['profile', 'follow', 'like', 'share', 'comment'],
            'content': ['blog', 'article', 'news', 'read'],
            'education': ['course', 'lesson', 'learn', 'tutorial'],
            'booking': ['book', 'reserve', 'appointment', 'schedule'],
        }

    async def analyze_url(self, url: HttpUrl, depth: str = "standard") -> URLContext:
        """
        Analyze a URL and extract contextual information.
        
        Args:
            url: The URL to analyze
            depth: Analysis depth (basic, standard, deep)
            
        Returns:
            URLContext with extracted information
        """
        try:
            logger.info(f"Analyzing URL: {url}")
            
            # Fetch the webpage
            response = self.session.get(str(url), timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic information
            title = self._extract_title(soup)
            description = self._extract_description(soup)
            
            # Extract features and functionality
            extracted_features = self._extract_features(soup, response.text)
            
            # Detect tech stack
            tech_stack = self._detect_tech_stack(response.text, soup)
            
            # Identify UI patterns
            ui_patterns = self._identify_ui_patterns(soup, response.text)
            
            # Determine business model
            business_model = self._determine_business_model(soup, response.text)
            
            # Extract target audience indicators
            target_audience = self._extract_target_audience(soup, response.text)
            
            # Identify key functionality
            key_functionality = self._extract_key_functionality(soup, response.text)
            
            # Find competitive advantages
            competitive_advantages = self._extract_competitive_advantages(soup, response.text)
            
            return URLContext(
                url=url,
                title=title,
                description=description,
                extracted_features=extracted_features,
                tech_stack=tech_stack,
                ui_patterns=ui_patterns,
                business_model=business_model,
                target_audience=target_audience,
                key_functionality=key_functionality,
                competitive_advantages=competitive_advantages,
                extracted_at=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error analyzing URL {url}: {str(e)}")
            # Return minimal context on error
            return URLContext(
                url=url,
                title="Analysis Failed",
                description=f"Could not analyze URL: {str(e)}",
                extracted_features=[],
                tech_stack=[],
                ui_patterns=[],
                business_model="unknown",
                target_audience="unknown",
                key_functionality=[],
                competitive_advantages=[],
                extracted_at=datetime.now()
            )

    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract page title."""
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        
        # Try h1 as fallback
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()
        
        return None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract page description."""
        # Try meta description first
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()
        
        # Try Open Graph description
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        if og_desc and og_desc.get('content'):
            return og_desc['content'].strip()
        
        # Try first paragraph
        first_p = soup.find('p')
        if first_p:
            text = first_p.get_text().strip()
            if len(text) > 50:
                return text[:200] + "..." if len(text) > 200 else text
        
        return None

    def _extract_features(self, soup: BeautifulSoup, html_content: str) -> List[str]:
        """Extract features mentioned on the page."""
        features = []
        
        # Look for feature lists
        feature_indicators = ['feature', 'benefit', 'capability', 'function']
        
        for indicator in feature_indicators:
            # Find elements that might contain features
            elements = soup.find_all(['li', 'div', 'span'], 
                                   class_=re.compile(indicator, re.I))
            
            for element in elements:
                text = element.get_text().strip()
                if 10 < len(text) < 100:  # Reasonable feature description length
                    features.append(text)
        
        # Look for headings that might describe features
        headings = soup.find_all(['h2', 'h3', 'h4'])
        for heading in headings:
            text = heading.get_text().strip()
            if any(word in text.lower() for word in ['feature', 'what', 'how', 'why']):
                if 5 < len(text) < 80:
                    features.append(text)
        
        return list(set(features))[:10]  # Limit to 10 unique features

    def _detect_tech_stack(self, html_content: str, soup: BeautifulSoup) -> List[str]:
        """Detect technology stack used."""
        detected_tech = []
        html_lower = html_content.lower()
        
        for tech, indicators in self.tech_indicators.items():
            if any(indicator in html_lower for indicator in indicators):
                detected_tech.append(tech)
        
        # Check script sources
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            src = script['src'].lower()
            for tech, indicators in self.tech_indicators.items():
                if any(indicator in src for indicator in indicators):
                    if tech not in detected_tech:
                        detected_tech.append(tech)
        
        return detected_tech

    def _identify_ui_patterns(self, soup: BeautifulSoup, html_content: str) -> List[str]:
        """Identify UI patterns used."""
        patterns = []
        html_lower = html_content.lower()
        
        for pattern, indicators in self.ui_patterns.items():
            if any(indicator in html_lower for indicator in indicators):
                patterns.append(pattern)
        
        # Check for specific elements
        if soup.find('nav'):
            patterns.append('navigation')
        if soup.find('form'):
            patterns.append('forms')
        if soup.find('table'):
            patterns.append('tables')
        
        return list(set(patterns))

    def _determine_business_model(self, soup: BeautifulSoup, html_content: str) -> Optional[str]:
        """Determine the business model."""
        html_lower = html_content.lower()
        
        model_scores = {}
        for model, indicators in self.business_models.items():
            score = sum(1 for indicator in indicators if indicator in html_lower)
            if score > 0:
                model_scores[model] = score
        
        if model_scores:
            return max(model_scores, key=model_scores.get)
        
        return "unknown"

    def _extract_target_audience(self, soup: BeautifulSoup, html_content: str) -> Optional[str]:
        """Extract target audience information."""
        # Look for common audience indicators
        audience_indicators = [
            'for businesses', 'for teams', 'for developers', 'for designers',
            'for students', 'for professionals', 'for individuals', 'for enterprises',
            'small business', 'startups', 'freelancers', 'agencies'
        ]
        
        html_lower = html_content.lower()
        for indicator in audience_indicators:
            if indicator in html_lower:
                return indicator
        
        return "general users"

    def _extract_key_functionality(self, soup: BeautifulSoup, html_content: str) -> List[str]:
        """Extract key functionality descriptions."""
        functionality = []
        
        # Look for action words and functionality descriptions
        action_patterns = [
            r'you can \w+', r'allows you to \w+', r'helps you \w+',
            r'enables \w+', r'provides \w+', r'offers \w+'
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            functionality.extend(matches[:3])  # Limit matches per pattern
        
        return functionality[:8]  # Limit total functionality items

    def _extract_competitive_advantages(self, soup: BeautifulSoup, html_content: str) -> List[str]:
        """Extract competitive advantages."""
        advantages = []
        
        # Look for advantage keywords
        advantage_keywords = [
            'faster', 'better', 'easier', 'more secure', 'advanced',
            'innovative', 'unique', 'exclusive', 'premium', 'professional'
        ]
        
        # Find sentences containing advantage keywords
        sentences = re.split(r'[.!?]', html_content)
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            if any(keyword in sentence_lower for keyword in advantage_keywords):
                if 20 < len(sentence) < 150:  # Reasonable sentence length
                    advantages.append(sentence.strip())
        
        return advantages[:5]  # Limit to 5 advantages

    def generate_integration_suggestions(self, url_context: URLContext, project_context: Dict[str, Any]) -> List[str]:
        """Generate suggestions for integrating with the analyzed system."""
        suggestions = []
        
        # Based on detected tech stack
        if 'react' in url_context.tech_stack:
            suggestions.append("Consider using React for consistency with the existing system")
        
        if 'stripe' in url_context.tech_stack:
            suggestions.append("Integrate with existing Stripe payment system")
        
        # Based on business model
        if url_context.business_model == 'ecommerce':
            suggestions.append("Ensure new features support the existing e-commerce workflow")
            suggestions.append("Consider impact on checkout and payment processes")
        
        if url_context.business_model == 'saas':
            suggestions.append("Align with existing subscription and user management systems")
            suggestions.append("Consider feature access controls and user tiers")
        
        # Based on UI patterns
        if 'navigation' in url_context.ui_patterns:
            suggestions.append("Ensure new features integrate with existing navigation structure")
        
        if 'dashboard' in url_context.ui_patterns:
            suggestions.append("Consider adding new features to the existing dashboard")
        
        return suggestions[:6]  # Limit suggestions
