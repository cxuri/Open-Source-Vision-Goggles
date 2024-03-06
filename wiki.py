import wikipediaapi

def get_wikipedia_summary(keyword):
    # Create a Wikipedia object
    wiki = wikipediaapi.Wikipedia('Project', 'en')

    # Get the page object for the given keyword
    page = wiki.page(keyword)

    # Check if the page exists
    if page.exists():
        # Get the summary of the page
        summary = page.summary
        return summary
    else:
        return f"No page found for '{keyword}'"
