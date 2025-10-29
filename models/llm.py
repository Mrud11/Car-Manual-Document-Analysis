from langchain_perplexity import ChatPerplexity

def get_llm_model(api_key=None):
    return ChatPerplexity(pplx_api_key=api_key, model="sonar")
