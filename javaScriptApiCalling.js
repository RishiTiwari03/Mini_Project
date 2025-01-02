 async function getRecommendations(queryData) {
    try {
        const response = await fetch('http://127.0.0.1:5000/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(queryData)
        });

        if (!response.ok) {
            const errorData = await response.json();//Try to parse error response from the server
            throw new Error(`API error: ${response.status} - ${errorData.error || response.statusText}`); //Include error message from server if available
        }

        const recommendations = await response.json();
        if (recommendations) {
            return recommendations;
            // console.log(recommendations.message); // Handle message from no results
        } else if (recommendations.error) {
            console.error("Error from server:", recommendations.error);
        }
    } catch (error) {
        console.error("Error fetching recommendations:", error);
        // Handle fetch errors (e.g., display an error message to the user)
    }
}

// Example usage:
const query1 = { gender: 'men', articleType: '', description: 'puma' };
const recommendation = await getRecommendations(query1);
console.log(recommendation);

