#/usr/bin/env python
# -*- coding: utf-8 -*-

# code inspired by claude

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def extract_citation_info(url):
    """
    Extract citation information from a Frontiers article URL
    """
    try:
        # Send GET request to the URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract information
        citation_info = {}
        
        # Title
        title_tag = soup.find('h1', class_='JournalFullText') or soup.find('h1')
        citation_info['title'] = title_tag.get_text(strip=True) if title_tag else "Title not found"
        
        # Authors
        authors = []
        author_tags = soup.find_all('span', class_='author-name') or soup.find_all('a', class_='author-name')
        for author_tag in author_tags:
            authors.append(author_tag.get_text(strip=True))
        citation_info['authors'] = authors
        
        # Journal name
        journal_tag = soup.find('meta', {'name': 'citation_journal_title'})
        if journal_tag:
            citation_info['journal'] = journal_tag.get('content')
        else:
            citation_info['journal'] = "Frontiers"
        
        # Publication year
        year_tag = soup.find('meta', {'name': 'citation_publication_date'})
        if year_tag:
            date_str = year_tag.get('content')
            citation_info['year'] = date_str.split('-')[0] if date_str else "Year not found"
        else:
            citation_info['year'] = "Year not found"
        
        # Volume and issue
        volume_tag = soup.find('meta', {'name': 'citation_volume'})
        citation_info['volume'] = volume_tag.get('content') if volume_tag else None
        
        # DOI
        doi_tag = soup.find('meta', {'name': 'citation_doi'})
        citation_info['doi'] = doi_tag.get('content') if doi_tag else None
        
        # Page numbers or article ID
        page_tag = soup.find('meta', {'name': 'citation_firstpage'})
        citation_info['pages'] = page_tag.get('content') if page_tag else None
        
        return citation_info
        
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
    except Exception as e:
        print(f"Error parsing the content: {e}")
        return None

def format_apa_citation(citation_info):
    """
    Format citation information in APA style
    """
    if not citation_info:
        return "Could not generate citation"
    
    # Format authors
    authors = citation_info.get('authors', [])
    if len(authors) == 0:
        author_str = "Author not found"
    elif len(authors) == 1:
        author_str = authors[0]
    elif len(authors) == 2:
        author_str = f"{authors[0]} & {authors[1]}"
    else:
        author_str = ", ".join(authors[:-1]) + f", & {authors[-1]}"
    
    # Build citation
    citation = f"{author_str} ({citation_info['year']}). {citation_info['title']}. "
    citation += f"{citation_info['journal']}"
    
    if citation_info.get('volume'):
        citation += f", {citation_info['volume']}"
    
    if citation_info.get('pages'):
        citation += f", {citation_info['pages']}"
    
    citation += "."
    
    if citation_info.get('doi'):
        citation += f" https://doi.org/{citation_info['doi']}"
    
    return citation

