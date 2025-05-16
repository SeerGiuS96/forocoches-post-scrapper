from bs4 import BeautifulSoup
from .models import Post, User
from typing import List, Optional

class PostExtractor:
    @staticmethod
    def extract_posts(html: str) -> List[Post]:
        soup = BeautifulSoup(html, 'html.parser')
        return [
            post for post_element in soup.select('.post')
            if (post := PostExtractor._parse_post(post_element))
        ]

    @staticmethod
    def _parse_post(element) -> Optional[Post]:
        try:
            return Post(
                id=element.get('id', ''),
                user=User(username=element.select_one('.username').text.strip()),
                content=element.select_one('.post-content').text.strip(),
                timestamp=datetime.now(),  # Implementar parser real
                quotes=[q.text.strip() for q in element.select('.quote')],
                replies_to=[r.text.strip() for r in element.select('.reply-to')]
            )
        except Exception as e:
            print(f"Error parsing post: {e}")
            return None