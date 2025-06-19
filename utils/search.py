from typing import List, Dict, Any, Tuple, Callable

def search_keywords(query: str, items: List[Dict[str, Any]], fn: Callable[[Dict[str, Any]], str], limit: int = 3) -> List[Dict[str, Any]]:
    """
    Simple keyword search through a list of items.
    
    Args:
        query: Search query string
        items: List of items to search through
        content: Content in each item
        limit: Maximum number of results to return
        
    Returns:
        List of items that match the search query, sorted by relevance
    """
    if not query.strip():
        return []

    # Split query into terms and convert to lowercase for case insensitive search
    query_terms = query.lower().split()
    results = []

    for item in items:
        content = fn(item)
        # Count matching terms
        score = sum(1 for term in query_terms if term in content.lower())
        
        if score > 0:
            results.append((item, score))

    # Sort by score (descending) and return top matches
    results.sort(key=lambda x: x[1], reverse=True)
    return [item[0] for item in results[:limit]]