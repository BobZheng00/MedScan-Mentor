from pymed import PubMed
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set your API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def compare_bbox(user_bbox, correct_bbox, tolerance=0.25):
    """Compare bounding box coordinates with a tolerance."""
    def within_tolerance(uc, cc, tol):
        return abs(uc - cc) / cc <= tol

    return all(within_tolerance(u, c, tolerance) for u, c in zip(user_bbox, correct_bbox))

def interpret_disease(user_interpretation, correct_disease_type):
    """Judge whether the user interpretation is correct based on the disease type."""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that evaluates the accuracy of medical interpretations."},
            {"role": "user", "content": f"The disease type is '{correct_disease_type}'. Evaluate the following interpretation: '{user_interpretation}'"}
        ],
        max_tokens=3000,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()

def summarize_with_openai(text):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access to GPT-4
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant that summarizes text. Make sure to emphasize key points by making them bold using Markdown syntax."},
            {"role": "user",
             "content": f"Summarize the following article in one sentence. Use Markdown syntax to bold the key points:\n\n{text}"}
        ],
        max_tokens=3000,
        temperature=0.5,
    )

    summarized_text = response.choices[0].message.content.strip()
    return summarized_text

def summarize_articles(articles):
    summary = "### Educational Summary:\n\n"

    if not articles:
        return "No articles found to summarize."

    # Start with an introduction
    summary += "**Here are key insights from recent research:**\n\n"

    for article in articles:
        # Add title for each article
        summary += f"- **{article['title']}**\n"

        # Use OpenAI to generate a brief synthesis of the abstract
        if article['abstract']:
            summarized_text = summarize_with_openai(article['abstract'])
            summary += f"  - {summarized_text}\n"
        else:
            summary += "  - Key Insights: Abstract not available.\n"

        summary += "\n"

    # Add a concluding remark
    summary += "**These articles provide a snapshot of current research, highlighting important findings in the field.**"

    return summary

def fetch_articles(query):
    pubmed = PubMed(tool="MyTool", email="your.email@example.com")
    results = pubmed.query(query, max_results=5)
    articles = []
    for article in results:
        article_dict = article.toDict()
        articles.append({
            'title': article_dict['title'],
            'abstract': article_dict['abstract'],
            'authors': ', '.join([author['lastname'] for author in article_dict['authors']]),
            'doi': article_dict['doi']
        })
    return articles

def simulate_rag_pipeline(user_input_bbox, correct_bbox, user_interpretation, disease_type):
    # 1. Compare Bounding Box Coordinates
    bbox_comparison = compare_bbox(user_input_bbox, correct_bbox)
    bbox_message = "**Bounding box coordinates are correct.**" if bbox_comparison else "**Bounding box coordinates are incorrect.**"

    # 2. Interpret User's Disease Interpretation
    interpretation_message = interpret_disease(user_interpretation, disease_type)

    # 3. Fetch and Summarize PubMed Articles
    articles = fetch_articles(disease_type)
    summary = summarize_articles(articles)

    # Combine all outputs
    full_output = f"{bbox_message}\n\n{interpretation_message}\n\n{summary}"
    return full_output

def main():
    print("MedScan Analysis Report:")

    # Input: User provides the type of brain disease.
    disease_type = input("Enter the type of brain disease (e.g., Glioma, Meningioma): ")

    if not disease_type:
        print("Error: Please provide a valid brain disease type.")
        return

    # Mock inputs for bounding box and interpretation
    user_input_bbox = [100, 150, 200, 250]  # Example user input
    correct_bbox = [102, 148, 198, 252]      # Example correct bbox
    user_interpretation = "I think this is a type of glioma based on the characteristics of the tumor."

    # Simulate RAG pipeline processing
    output = simulate_rag_pipeline(user_input_bbox, correct_bbox, user_interpretation, disease_type)
    print(output)

if __name__ == "__main__":
    main()
