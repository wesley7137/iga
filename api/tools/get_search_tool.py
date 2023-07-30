from langchain.utilities import GoogleSerperAPIWrapper
#GoogleSerperAPIWrapper.serper_api_key =  "12791d683d28e8c5f696fa10ac9687c7fe73e315"

query = "info on string theory"

search = GoogleSerperAPIWrapper()
response = search.run(query)

print(response)