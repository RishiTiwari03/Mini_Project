from flask import Flask, request, jsonify
import pandas as pd
from recommendation import recommend  

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def api_recommend():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided in the request"}), 400 # Return 400 bad request error
        
        recommendations = recommend(data)
        if isinstance(recommendations, pd.DataFrame): #Check if it is a dataframe or not
            recommendations_dict = recommendations.to_dict(orient='records')
            return jsonify(recommendations_dict)
        elif isinstance(recommendations, str):
            return jsonify({"message": recommendations}), 200 #If no results are found then it is a string
        else:
            return jsonify({"error": "Invalid data type returned by recommend function"}), 500 #Handle other unexpected return types
    except Exception as e:
        print(f"An error occurred: {e}") #Print error for debugging
        return jsonify({"error": "An error occurred during processing"}), 500 #Return a 500 error for internal server error

if __name__ == '__main__':
    app.run(debug=True)