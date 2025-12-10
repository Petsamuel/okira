import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import re
import time
from urllib.parse import quote_plus

def scrape_gmb_data(query: str, location: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """
    Scrapes business data from Google Search using BeautifulSoup4.
    Lightweight alternative to Playwright - no browser needed!
    
    Args:
        query: Search query (e.g., 'restaurants', 'tech companies')
        location: Location to search (e.g., 'Lagos, Nigeria')
        max_results: Maximum number of results to return
        
    Returns:
        List of business lead dictionaries
    """
    businesses = []
    
    # Build search query
    search_query = f"{query} in {location}"
    encoded_query = quote_plus(search_query)
    
    print(f"🔍 Searching Google: {search_query}")
    
    # Google Search URL
    url = f"https://www.google.com/search?q={encoded_query}"
    
    # Headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        # Make request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract business listings from Google Search results
        # Google Search has different selectors for business results
        businesses = extract_businesses_from_search(soup, max_results)
        
        if not businesses:
            # Try alternative extraction method
            print("⚠️ Primary extraction failed, trying alternative method...")
            businesses = extract_businesses_alternative(soup, max_results)
        
        print(f"✨ Successfully scraped {len(businesses)} businesses")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {str(e)}")
        raise Exception(f"Failed to fetch Google results: {str(e)}")
    except Exception as e:
        print(f"❌ Parsing error: {str(e)}")
        raise
    
    return businesses


def extract_businesses_from_search(soup: BeautifulSoup, max_results: int) -> List[Dict[str, Any]]:
    """
    Extracts business data from Google Search results.
    """
    businesses = []
    
    # Look for business cards in search results
    # These are common Google Search result structures
    result_divs = soup.find_all('div', class_='g')
    
    for div in result_divs[:max_results * 2]:  # Check more than needed
        if len(businesses) >= max_results:
            break
            
        try:
            business = {}
            
            # Extract title/name
            title_elem = div.find('h3')
            if title_elem:
                business['name'] = title_elem.get_text(strip=True)
            else:
                continue  # Skip if no title
            
            # Extract URL/website
            link_elem = div.find('a')
            if link_elem and link_elem.get('href'):
                business['website'] = link_elem['href']
                # Clean up Google redirect URLs
                if business['website'].startswith('/url?q='):
                    business['website'] = business['website'].split('/url?q=')[1].split('&')[0]
            
            # Extract snippet/description
            snippet_elem = div.find('div', class_='VwiC3b')
            if not snippet_elem:
                snippet_elem = div.find('span', class_='aCOpRe')
            if snippet_elem:
                snippet_text = snippet_elem.get_text(strip=True)
                
                # Try to extract phone from snippet
                phone_match = re.search(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', snippet_text)
                if phone_match:
                    business['phone'] = phone_match.group()
                
                # Try to extract address (Nigerian locations)
                address_patterns = [
                    r'(.*?(?:Lagos|Abuja|Port Harcourt|Kano|Ibadan|Kaduna|Enugu|Benin City).*?Nigeria)',
                    r'(\d+.*?(?:Street|Road|Avenue|Way|Close|Boulevard|Lane).*?)',
                ]
                for pattern in address_patterns:
                    addr_match = re.search(pattern, snippet_text, re.IGNORECASE)
                    if addr_match:
                        business['address'] = addr_match.group(1).strip()
                        break
            
            # Try to extract rating
            rating_elem = div.find('span', string=re.compile(r'\d+\.\d+'))
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                rating_match = re.search(r'(\d+\.\d+)', rating_text)
                if rating_match:
                    business['rating'] = float(rating_match.group(1))
            
            # Extract reviews count
            reviews_elem = div.find('span', string=re.compile(r'\d+.*?reviews?', re.IGNORECASE))
            if reviews_elem:
                reviews_text = reviews_elem.get_text(strip=True)
                reviews_match = re.search(r'(\d+)', reviews_text)
                if reviews_match:
                    business['reviews_count'] = int(reviews_match.group(1))
            
            # Set GMB URL to the search result link
            business['gmb_url'] = business.get('website', '')
            
            if business.get('name'):
                businesses.append(business)
                print(f"✅ Extracted: {business['name']}")
                
        except Exception as e:
            print(f"⚠️ Error extracting business: {str(e)}")
            continue
    
    return businesses


def extract_businesses_alternative(soup: BeautifulSoup, max_results: int) -> List[Dict[str, Any]]:
    """
    Alternative extraction method using different selectors.
    """
    businesses = []
    
    # Try finding all links with business-like patterns
    all_links = soup.find_all('a', href=True)
    
    seen_names = set()
    
    for link in all_links:
        if len(businesses) >= max_results:
            break
        
        try:
            # Look for links that might be businesses
            text = link.get_text(strip=True)
            href = link.get('href', '')
            
            # Skip Google internal links and too short texts
            if not text or len(text) < 5:
                continue
            if 'google.com' in href or href.startswith('#'):
                continue
            
            # Avoid duplicates
            if text in seen_names:
                continue
            
            # Basic business data
            business = {
                'name': text,
                'website': href if href.startswith('http') else None,
                'gmb_url': href if href.startswith('http') else None
            }
            
            # Try to find associated data in parent elements
            parent = link.find_parent('div', class_='g')
            if parent:
                parent_text = parent.get_text()
                
                # Extract phone
                phone_match = re.search(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', parent_text)
                if phone_match:
                    business['phone'] = phone_match.group()
                
                # Extract rating
                rating_match = re.search(r'(\d+\.\d+)', parent_text)
                if rating_match:
                    try:
                        business['rating'] = float(rating_match.group(1))
                    except:
                        pass
            
            businesses.append(business)
            seen_names.add(text)
            print(f"✅ Extracted (alt): {business['name']}")
            
        except Exception as e:
            continue
    
    return businesses
