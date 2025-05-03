import streamlit as st
import pickle
import cohere

# 🔹 Set your Cohere API Key directly here
COHERE_API_KEY = ""  # 🔴 Replace with your actual API key

# Validate API Key
if not COHERE_API_KEY:
    st.error("⚠️ COHERE_API_KEY is missing. Please provide a valid API key.")
    st.stop()

# Load the trained model and vectorizer
with open("sentiment_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("vectorizer.pkl", "rb") as vec_file:
    vectorizer = pickle.load(vec_file)

# Initialize Cohere API
co = cohere.Client(COHERE_API_KEY)

def generate_explanation(tweet, sentiment):
    """ Uses Cohere LLM to generate a human-like sentiment explanation """
    prompt = f"Analyze this tweet: '{tweet}'. It is categorized as {sentiment}. Explain why in simple terms."
    
    try:
        response = co.generate(
            model="command-light",  # ✅ Updated to 'command-light' (valid model)
            prompt=prompt,
            max_tokens=100
        )
        
        # Ensure valid response
        if response and response.generations:
            return response.generations[0].text.strip()
        else:
            return "No explanation generated. Try again later."
    
    except cohere.CohereAPIError as e:
        return f"❌ Error from Cohere API: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}"

# Streamlit App UI
st.title("Twitter Sentiment Analysis with AI Insights (Cohere)")

# User Input
user_input = st.text_area("Enter your tweet:", "")

if st.button("Analyze Sentiment"):
    if user_input:
        # Preprocess input
        input_vector = vectorizer.transform([user_input])
        
        # Predict sentiment
        prediction = model.predict(input_vector)[0]
        
        # Map sentiment labels
        sentiment_map = {0: "Negative", 1: "Positive", 2: "Neutral"}
        sentiment = sentiment_map.get(prediction, "Unknown")

        # LLM-generated Explanation
        explanation = generate_explanation(user_input, sentiment)

        # Display Results
        st.write(f"**Predicted Sentiment:** {sentiment}")
        st.write(f"📖 **AI Explanation:** {explanation}")
    else:
        st.warning("⚠️ Please enter a tweet to analyze.")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Cohere")
