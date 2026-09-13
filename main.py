from src.tools.tools import scrape_url

results = scrape_url.invoke("https://en.wikipedia.org/wiki/Artificial_intelligence")
print(results)