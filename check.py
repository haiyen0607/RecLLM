import google.generativeai as genai

genai.configure(api_key="AIzaSyA93XSciP3OjTS6dCB_QuB9mGmqWNEVVsQ")

for model in genai.list_models():
    print("Model:", model.name)
    print("Supported methods:", model.supported_generation_methods)
    print("---")
