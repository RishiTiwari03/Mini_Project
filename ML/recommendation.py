import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data and preprocess
df = pd.read_csv("C:\\Users\\KIIT\\Downloads\\MAIN.csv")

df['productDisplayName'] = df['productDisplayName'].str.lower().fillna('')
df['gender'] = df['gender'].str.lower().fillna('')
df['articleType'] = df['articleType'].str.lower().fillna('')

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['productDisplayName'])

def recommend(query_dict, top_n=7):
    if not query_dict:
        print("Error: Empty query provided.")
        return pd.DataFrame()

    gender_filter = query_dict.get('gender')
    article_type_filter = query_dict.get('articleType')
    description_query = query_dict.get('description', '')  # Default empty string for description

    if not description_query and not gender_filter and not article_type_filter:
        print("Error: No search criteria provided. Provide at least gender, articleType or description")
        return pd.DataFrame()
    
    if gender_filter:
        gender_filter = gender_filter.lower()
        if gender_filter not in df['gender'].unique():
            print(f"Error: Invalid gender: {gender_filter}")
            return pd.DataFrame()

    if article_type_filter:
        article_type_filter = article_type_filter.lower()
        if article_type_filter not in df['articleType'].unique():
            print(f"Error: Invalid article type: {article_type_filter}")
            return pd.DataFrame()

    query_vec = vectorizer.transform([description_query.lower()])
    similarity_scores = cosine_similarity(query_vec, tfidf_matrix)
    similar_indices = similarity_scores.argsort()[0][::-1]

    filtered_indices = []
    for i in similar_indices:
        gender_match = True
        article_type_match = True

        if gender_filter:
            gender_match = df['gender'].iloc[i] == gender_filter
        if article_type_filter:
            article_type_match = df['articleType'].iloc[i] == article_type_filter

        if gender_match and article_type_match:
            filtered_indices.append(i)

    if not filtered_indices:
        print("No results found matching your criteria.")
        return pd.DataFrame()

    return df.iloc[filtered_indices[:top_n]][['id', 'productDisplayName', 'masterCategory', 'subCategory', 'gender', 'articleType']]
