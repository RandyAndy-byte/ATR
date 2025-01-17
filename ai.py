import requests
import openai

def request(question):
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/codegen-350M-mono"
    headers = {"Authorization": "Bearer hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": question,
    })
    
    return output


def get_codex_completion(prompt, api_key, engine="code-davinci-002", max_tokens=150, temperature=0.5, top_p=1.0, n=1):
    """
    Makes a request to OpenAI Codex and returns the generated code or answer as a string.
    
    Parameters:
    - prompt (str): The prompt to send to Codex.
    - api_key (str): Your OpenAI API key.
    - engine (str): The Codex model to use (default is "code-davinci-002").
    - max_tokens (int): The maximum number of tokens to generate (default is 150).
    - temperature (float): Controls the randomness of the output (default is 0.5).
    - top_p (float): Controls the diversity of the output (default is 1.0).
    - n (int): The number of completions to generate (default is 1).

    Returns:
    - str: The relevant code or answer generated by Codex.
    """
    openai.api_key = api_key

    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        n=n,
        stop=None
    )

    # Extract the generated code or answer from the response
    generated_text = response.choices[0].text.strip()
    
    return generated_text
