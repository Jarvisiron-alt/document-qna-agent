import arxiv
import requests

class ArxivClient:
    def __init__(self):
        self.client = arxiv.Client()

    def search_papers(self, query, max_results=3):
        """
        Searches for papers on Arxiv.
        """
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            papers = []
            for result in self.client.results(search):
                papers.append({
                    "title": result.title,
                    "authors": [author.name for author in result.authors],
                    "summary": result.summary,
                    "published": result.published.strftime('%Y-%m-%d')
                })
            return papers
        except Exception as e:
            print(f"An error occurred while searching Arxiv: {e}")
            return []
