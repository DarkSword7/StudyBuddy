# search_engine.py
import os
import re
import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class SearchEngine:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        # Replace with your actual YouTube API key
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')

    def generate_google_dorks(self, query):
        """Generate advanced search queries for finding study materials"""
        dorks = [
            f'"{query}" filetype:pdf site:edu',
            f'"{query}" intitle:"lecture notes" site:edu',
            f'"{query}" filetype:ppt site:edu',
            f'"{query}" site:academia.edu',
            f'"{query}" "study guide" site:*.edu'
        ]
        return dorks

    def fetch_overview(self, query):
        """Attempt to generate a comprehensive overview of the query"""
        try:
            encoded_query = urllib.parse.quote(f"{query} overview definition")
            search_url = f"https://www.google.com/search?q={encoded_query}"
            
            response = requests.get(search_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            overview = None
            
            # Try to extract featured snippet
            featured_snippet = soup.select_one('.hgKElc')
            if featured_snippet:
                overview = featured_snippet.get_text()
            
            # If no featured snippet, try other containers
            if not overview:
                descriptions = soup.select('.VwiC3b')
                if descriptions:
                    overview = ' '.join([desc.get_text() for desc in descriptions[:2]])
            
            # Final fallback
            if not overview:
                overview = f"A comprehensive overview of {query} involves understanding its key concepts and applications."
            
            return overview
        
        except Exception as e:
            print(f"Overview generation error: {e}")
            return f"Information about {query} is currently being processed."

    def search_youtube_videos(self, query, max_results=3):
        """Search for relevant educational YouTube videos"""
        try:
            youtube = build('youtube', 'v3', developerKey=self.youtube_api_key)
            
            # Enhance query for educational content
            educational_query = f"{query} tutorial education lecture"
            
            request = youtube.search().list(
                q=educational_query,
                part='snippet',
                type='video',
                maxResults=max_results,
                relevanceLanguage='en',
                safeSearch='moderate'
            )
            response = request.execute()
            
            videos = []
            for item in response['items']:
                video = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'thumbnail': item['snippet']['thumbnails']['high']['url']
                }
                videos.append(video)
            
            return videos
        
        except Exception as e:
            print(f"YouTube search error: {e}")
            return []

    def advanced_web_search(self, query, max_results=5):
        """Perform an advanced web search with multiple techniques"""
        try:
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://www.google.com/search?q={encoded_query}"
            
            response = requests.get(search_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = []
            sources = set()
            
            for result in soup.select('.g'):
                try:
                    link = result.select_one('a')
                    if not link:
                        continue
                    
                    url = link['href']
                    if not url.startswith('http'):
                        continue
                    
                    # Skip if URL is already processed
                    if url in sources:
                        continue
                    sources.add(url)
                    
                    # Extract title
                    title_elem = result.select_one('h3')
                    title = title_elem.get_text() if title_elem else "Untitled"
                    
                    # Extract description
                    desc_elem = result.select_one('.VwiC3b')
                    description = desc_elem.get_text() if desc_elem else "No description available"
                    
                    articles.append({
                        'title': title,
                        'description': description,
                        'url': url
                    })
                    
                    if len(articles) >= max_results:
                        break
                
                except Exception as e:
                    print(f"Error processing search result: {e}")
                    continue
            
            return articles
        
        except Exception as e:
            print(f"Web search error: {e}")
            return []

    def search_study_materials(self, query, max_results=5):
        """Search for study materials including PDFs and educational resources"""
        try:
            dorks = self.generate_google_dorks(query)
            study_materials = []
            sources = set()
            
            for dork in dorks:
                encoded_dork = urllib.parse.quote(dork)
                search_url = f"https://www.google.com/search?q={encoded_dork}"
                
                response = requests.get(search_url, headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for result in soup.select('.g'):
                    try:
                        link = result.select_one('a')
                        if not link:
                            continue
                        
                        url = link['href']
                        if not url.startswith('http'):
                            continue
                        
                        if url in sources:
                            continue
                        sources.add(url)
                        
                        title_elem = result.select_one('h3')
                        title = title_elem.get_text() if title_elem else "Untitled"
                        
                        file_type = "Web Resource"
                        if url.lower().endswith('.pdf'):
                            file_type = "PDF Document"
                        elif url.lower().endswith(('.ppt', '.pptx')):
                            file_type = "Presentation"
                        
                        study_materials.append({
                            'title': title,
                            'url': url,
                            'type': file_type
                        })
                        
                        if len(study_materials) >= max_results:
                            break
                    
                    except Exception as e:
                        print(f"Error processing study material: {e}")
                        continue
                
                if len(study_materials) >= max_results:
                    break
            
            return study_materials
        
        except Exception as e:
            print(f"Study materials search error: {e}")
            return []

    def perform_comprehensive_search(self, query):
        """Perform a comprehensive search across different sources"""
        return {
            'overview': self.fetch_overview(query),
            'youtube_videos': self.search_youtube_videos(query),
            'web_articles': self.advanced_web_search(query),
            'study_materials': self.search_study_materials(query)
        }