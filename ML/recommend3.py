import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations(df, query, top_n=7):
    """
    Recommends clothes based on a query dictionary.

    Args:
        df: Pandas DataFrame containing product data.
        query: Dictionary containing search criteria (e.g., {"gender": "men", "category": "shirts", "description": "blue cotton shirt"}).
        top_n: Number of recommendations to return.

    Returns:
        Pandas DataFrame with top N recommendations, or a string message if no results or errors.
    """
    try:
        if not query or not isinstance(query, dict) or not any(query.values()): # Handle empty or invalid query
            return "Please provide a valid search query with at least one criteria."

        if df.empty: #Handle empty DataFrame
            return "No products found in the database."

        # 1. Text Preprocessing and TF-IDF (for description)
        df['combined_text'] = df.apply(lambda row: ' '.join(row.dropna().astype(str).values), axis=1) #Combines all text columns
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['combined_text'])

        query_description = query.get('description', '')
        query_vector = tfidf.transform([query_description])
        similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

        df['similarity'] = similarities #Add similarity column to the dataframe

        # 2. Filtering by other attributes
        filtered_df = df.copy()
        for key, value in query.items():
            if key != 'description' and value:
                filtered_df = filtered_df[filtered_df[key].str.lower() == str(value).lower()] #Case insensitive filtering

        if filtered_df.empty:
            return "No products found matching your criteria."

        # 3. Sort by similarity and get top N
        recommended_df = filtered_df.nlargest(top_n, 'similarity')

        recommended_df = recommended_df.drop('combined_text', axis = 1) #Remove the combined text column
        recommended_df = recommended_df.drop('similarity', axis = 1) #Remove the similarity column

        return recommended_df

    except (KeyError, TypeError, AttributeError) as e: #Handle potential errors
        print(f"An error occurred: {e}")
        return "An error occurred during processing."


# Example Usage (assuming you have a DataFrame called 'products_df'):
products_df = pd.read_csv("C:\\Users\\KIIT\\Downloads\\MAIN.csv")
query1 = {"gender": "men", "articleType": "jeans", "description": "slim fit blue jeans"}
recommendations1 = get_recommendations(products_df, query1)
print("Recommendations for query 1:\n", recommendations1)

query2 = {"gender": "women", "description": "red dress"}
recommendations2 = get_recommendations(products_df, query2)
print("\nRecommendations for query 2:\n", recommendations2)

query3 = {"articleType": "shirts", "description": "casual cotton shirt"}
recommendations3 = get_recommendations(products_df, query3)
print("\nRecommendations for query 3:\n", recommendations3)

query4 = {"gender": "invalid_gender"}
recommendations4 = get_recommendations(products_df, query4)
print("\nRecommendations for query 4 (invalid gender):\n", recommendations4)

query5 = {}  # Empty Query
recommendations5 = get_recommendations(products_df, query5)
print("\nRecommendations for query 5 (Empty Query):\n", recommendations5)

query6 = {"description": "xyz"} # totally wrong query
recommendations6 = get_recommendations(products_df, query6)
print("\nRecommendations for query 6 (totally wrong query):\n", recommendations6)

query7 = {"gender": "men", "articleType": "jeans"}  # No description
recommendations7 = get_recommendations(products_df, query7)
print("\nRecommendations for query 7 (No description):\n", recommendations7)