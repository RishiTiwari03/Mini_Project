import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data and preprocess
df = pd.read_csv("C:\\Users\\KIIT\\Downloads\\MAIN.csv")

# Convert text attributes to lowercase and handle missing values
text_columns = ['productDisplayName', 'gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'usage']
for col in text_columns:
    df[col] = df[col].str.lower().fillna('')

# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['productDisplayName'])

def recommend(query_dict, top_n=7):

    if not query_dict:
        print("Error: Empty query provided.")
        return pd.DataFrame()

    # Extract description and filter criteria
    description_query = query_dict.get('description', '').lower()
    filters = {key: value.lower() for key, value in query_dict.items() if key != 'description' and key in df.columns}

    # Validate filters against unique values in the dataset
    for key, value in filters.items():
        if value not in df[key].unique():
            print(f"Error: Invalid value for {key}: {value}")
            return pd.DataFrame()

    # Compute cosine similarity for description, if provided
    if description_query:
        query_vec = vectorizer.transform([description_query])
        similarity_scores = cosine_similarity(query_vec, tfidf_matrix)
        similar_indices = similarity_scores.argsort()[0][::-1]
    else:
        similar_indices = range(len(df))  # No description provided, consider all rows

    # Apply filters on the dataset
    filtered_indices = []
    for i in similar_indices:
        match = all(df[key].iloc[i] == value for key, value in filters.items())
        if match:
            filtered_indices.append(i)
        if len(filtered_indices) >= top_n:  # Stop when top_n results are collected
            break

    if not filtered_indices:
        print("No results found matching your criteria.")
        return pd.DataFrame()

    # Return filtered and sorted DataFrame
    return df.iloc[filtered_indices][['id', 'productDisplayName', 'masterCategory', 'subCategory', 
                                      'articleType', 'baseColour', 'season', 'usage', 'gender']]

# Example queries
query1 = {'gender': 'men',
          'description': 'puma', 
        #   'masterCategory':'',
        #   'subCategory':'',
          'articleType':'jeans',
          'baseColour':'blue', 
        #   'season':'',
        #   'usage':'', 
          }
recommendations1 = recommend(query1)
print("Recommendations for query 1:")
print(recommendations1)

#     Recommend products based on query_dict and filters.

#     Parameters:
#         query_dict (dict): A dictionary containing query keys and their values.
#             Valid keys: 'gender', 'masterCategory', 'subCategory', 'articleType', 
#                         'baseColour', 'season', 'usage', 'description'
#         top_n (int): Number of top recommendations to return.

#     Returns:
#         pd.DataFrame: DataFrame containing recommended products.