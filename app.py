import os
import json
from trufflepig import Trufflepig
from openai import OpenAI
import gradio as gr

# Initialize clients with error handling
truffle_key = os.getenv('TRUFFLE_KEY')
openai_key = os.getenv('OPEN_AI_KEY')

if not truffle_key:
    raise EnvironmentError("TRUFFLE_KEY environment variable not found")
if not openai_key:
    raise EnvironmentError("OPEN_AI_KEY environment variable not found")

truffle_client = Trufflepig(truffle_key)
index = truffle_client.get_index('truffle-pig-qa')
openai_client = OpenAI(api_key=openai_key)

def get_search_context(query):
    """Retrieve search context for a given query from the TrufflePig API."""
    try:
        search_response = index.search(query_text=query, max_results=3)
        if not search_response:
            raise ValueError("No search results found")
        return search_response[0].content
    except Exception as e:
        return f"Error retrieving search context: {str(e)}"

def augmentation_generation(query, search_context):
    """Generate a response using the OpenAI API based on the query and search context."""
    prompt = f"""
    You are an AI coding assistant designed to answer user queries about the TrufflePig API. Given the user query and context below,
    write a concise, well-written answer to the user's query. Please don't include any code in the answer. Just answer in a concise,
    conversational way.

    <<QUERY>>
    {query}

    <<CONTEXT>>
    {search_context}
    """
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        return response.json()
    except Exception as e:
        return json.dumps({"choices": [{"message": {"content": f"Error generating augmentation: {str(e)}"}}]})

def generate_answer(query):
    """Generate the final answer for the user query."""
    try:
        search_context = get_search_context(query)
        final_answer = augmentation_generation(query, search_context)
        return json.loads(final_answer)['choices'][0]['message']['content']
    except json.JSONDecodeError:
        return "Error decoding JSON response"
    except KeyError:
        return "Unexpected response format"
    except Exception as e:
        return f"Error generating answer: {str(e)}"

# Define the Gradio interface
iface = gr.Interface(
    fn=generate_answer, 
    inputs="text", 
    outputs="text",
    title="RAG Chatbot",
    description="Ask questions about the TrufflePig API and get concise, context-aware answers."
)

# Launch the app
iface.launch()