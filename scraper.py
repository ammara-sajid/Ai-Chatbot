import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import time
from config import PINECONE_API_KEY

# Initialize embedding model (free from HuggingFace)
model = SentenceTransformer("all-MiniLM-L6-v2")  # ~384-dim vectors

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("company-knowledge")

# ---------------------------
# Helper: Chunk paragraphs
# ---------------------------
def chunk_paragraphs(paragraphs, chunk_size=5):
    """Group paragraphs into chunks for better context."""
    for i in range(0, len(paragraphs), chunk_size):
        yield " ".join(paragraphs[i:i+chunk_size])

# ---------------------------
# Scraper function
# ---------------------------
def scrape_page(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print(f"❌ Failed to fetch {url}, status: {r.status_code}")
            return []
        soup = BeautifulSoup(r.text, "html.parser")
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        return [p for p in paragraphs if p]  # remove empty ones
    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")
        return []

# ---------------------------
# Target URLs
# ---------------------------
urls = [
    "https://www.parco.com.pk/",
    "https://www.parco.com.pk/about-us/",
    "https://www.parco.com.pk/our-business/",
    "https://www.parco.com.pk/hseq/",
    "https://www.parco.com.pk/csr/",
    "https://www.parco.com.pk/sustainability/",
    "https://www.parco.com.pk/media/",
    "https://www.parco.com.pk/career/",
    "https://www.parco.com.pk/tenders/",
    "https://www.parco.com.pk/contact-us/",
]

# ---------------------------
# Main loop: Scrape + Upload
# ---------------------------
for i, url in enumerate(urls):
    print(f"📄 Scraping: {url}")
    paragraphs = scrape_page(url)

    if not paragraphs:
        continue

    # Chunk paragraphs for better embeddings
    for chunk_id, chunk in enumerate(chunk_paragraphs(paragraphs, chunk_size=5)):
        try:
            vector = model.encode(chunk).tolist()
            index.upsert(vectors=[{
                "id": f"doc-{i}-{chunk_id}",
                "values": vector,
                "metadata": {"text": chunk, "url": url}
            }])
            time.sleep(0.2)  # to avoid rate limits
        except Exception as e:
            print(f"⚠️ Error uploading chunk {chunk_id} from {url}: {e}")

print("✅ Scraping + Pinecone upload complete (free embeddings)!")
