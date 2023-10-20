import json
import os
from dotenv import load_dotenv
from llama_index import (LLMPredictor, SimpleDirectoryReader, ServiceContext)
from langchain.llms import AzureOpenAI
from langchain.embeddings import OpenAIEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.indices.prompt_helper import PromptHelper
from llama_index.indices.vector_store.base import VectorStoreIndex
from flask import Flask, request
import requests
from llama_index.memory import ChatMemoryBuffer

class MyApp:

    def __init__(self):

        load_dotenv()
        
        self.app = Flask(__name__)
        self.data = []
        self.memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
        self.load_data()
        self.app.route('/query', methods=['GET'])(self.query_data)
        self.template = '''Answer the given prompt with MS Graph API endpoint. The answer should be strictly in following form:
            HTTP METHOD 

            HTTP ENDPOINT URL

            HTTP REQUEST PAYLOAD
            {}'''
        self.response = ''

    def load_data(self):
        try:
            # USe this to connect to Azure Open AI and train your model further
            # Create an instance of Azure OpenAI
            # Replace the deployment name with your own
            llm = AzureOpenAI(
                deployment_name="azure_davinci",
                model_name="text-davinci-003",
                temperature=0,
                max_tokens=500,
                top_p=1,
                n=1,
            )



            llm_predictor = LLMPredictor(llm=llm)
            embedding_llm = LangchainEmbedding(OpenAIEmbeddings(), embed_batch_size=1)

            max_input_size = 1000
            num_output = 256
            chunk_size_limit = 1000

            prompt_helper = PromptHelper(context_window=max_input_size,num_output=num_output, chunk_size_limit=chunk_size_limit)
            service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, embed_model=embedding_llm, prompt_helper=prompt_helper)

            docs_path = "data"
            documents = SimpleDirectoryReader("./data/", required_exts=".md").load_data()
            index = VectorStoreIndex.from_documents(documents, service_context=service_context)
            #self.query_engine = index.as_query_engine()
            self.chat_engine = index.as_chat_engine(
                            chat_mode="context",
                            memory=self.memory,
                            system_prompt="You are a chatbot, able to have normal interactions, answert the question in the given context also help with some c# scripts..",
                        )
            print("Docs Laoded")
            
            
           
        except Exception as e:
            print(e)
            return e

    def query_data(self):
            prompt = request.args.get('question')
            query = self.template.format(prompt)
            response = self.chat_engine.chat(query)
            print(f"Question: {prompt}")
            print(response)
            output = self.execute_request(response)
            output['Endpoint'] = str(response)
            jsonOutput = json.dumps(output, indent=4)
            return jsonOutput 

    def execute_request(self, response):
            responseArr = response.response.split()
            headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJub25jZSI6IkFiRThCQVJzSEotc1gxc1Rabm5OSUJ1WURTYjliZk5CYm5hSXIzWTYxYmsiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8yNDMyYjU3Yi0wYWJkLTQzZGItYWE3Yi0xNmVhZGQxMTVkMzQvIiwiaWF0IjoxNjk1MDQ0MjM5LCJuYmYiOjE2OTUwNDQyMzksImV4cCI6MTY5NTEzMDkzOSwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFUUUF5LzhVQUFBQTZ1cGpYRUh4djJwaUxPU0szNVlVRUVpdUxmYnhwcy83ZmVOSHhudGFkVlFrSFBFUmlyMXV5K1U0MEpsZk5yNnciLCJhbXIiOlsicHdkIl0sImFwcF9kaXNwbGF5bmFtZSI6IkdyYXBoIEV4cGxvcmVyIiwiYXBwaWQiOiJkZThiYzhiNS1kOWY5LTQ4YjEtYThhZC1iNzQ4ZGE3MjUwNjQiLCJhcHBpZGFjciI6IjAiLCJmYW1pbHlfbmFtZSI6IlRlc3RpbmdVc2VyIiwiZ2l2ZW5fbmFtZSI6IkdyYXBoIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMjQwNDpmODAxOjgwMjg6MzpkOGI4OjIzMmM6ZmJlMzoyMGVkIiwibmFtZSI6IkdyYXBoIFRlc3RpbmdVc2VyIiwib2lkIjoiOTc2ZjRiMzEtZmQwMS00ZTBiLTkxNzgtMjljYzQwYzE0NDM4IiwicGxhdGYiOiIzIiwicHVpZCI6IjEwMDMyMDAwRjA3N0Y3RUEiLCJyaCI6IjAuQVZjQWU3VXlKTDBLMjBPcWV4YnEzUkZkTkFNQUFBQUFBQUFBd0FBQUFBQUFBQURiQUpnLiIsInNjcCI6IkFwcGxpY2F0aW9uLlJlYWQuQWxsIEFwcGxpY2F0aW9uLlJlYWRXcml0ZS5BbGwgQXBwUm9sZUFzc2lnbm1lbnQuUmVhZFdyaXRlLkFsbCBDYWxlbmRhcnMuUmVhZFdyaXRlIENoYW5uZWwuUmVhZEJhc2ljLkFsbCBDaGFubmVsTWVtYmVyLlJlYWQuQWxsIENoYW5uZWxNZW1iZXIuUmVhZFdyaXRlLkFsbCBDaGFubmVsTWVzc2FnZS5SZWFkLkFsbCBDaGFubmVsTWVzc2FnZS5SZWFkV3JpdGUgQ2hhdC5NYW5hZ2VEZWxldGlvbi5BbGwgQ2hhdC5SZWFkIENoYXQuUmVhZEJhc2ljIENoYXQuUmVhZFdyaXRlIENvbnRhY3RzLlJlYWRXcml0ZSBEZWxlZ2F0ZWRQZXJtaXNzaW9uR3JhbnQuUmVhZFdyaXRlLkFsbCBEZXZpY2VNYW5hZ2VtZW50UkJBQy5SZWFkLkFsbCBEZXZpY2VNYW5hZ2VtZW50U2VydmljZUNvbmZpZy5SZWFkLkFsbCBEaXJlY3RvcnkuUmVhZC5BbGwgRGlyZWN0b3J5LlJlYWRXcml0ZS5BbGwgRWR1QXNzaWdubWVudHMuUmVhZCBGaWxlcy5SZWFkV3JpdGUuQWxsIEdyb3VwLlJlYWQuQWxsIEdyb3VwLlJlYWRXcml0ZS5BbGwgSWRlbnRpdHlSaXNrRXZlbnQuUmVhZC5BbGwgSW5mb3JtYXRpb25Qcm90ZWN0aW9uUG9saWN5LlJlYWQgTWFpbC5SZWFkIE1haWwuUmVhZFdyaXRlIE1haWxib3hTZXR0aW5ncy5SZWFkV3JpdGUgTm90ZXMuUmVhZFdyaXRlLkFsbCBPbmxpbmVNZWV0aW5nUmVjb3JkaW5nLlJlYWQuQWxsIE9ubGluZU1lZXRpbmdzLlJlYWQgT25saW5lTWVldGluZ1RyYW5zY3JpcHQuUmVhZC5BbGwgb3BlbmlkIFBlb3BsZS5SZWFkIFBlb3BsZS5SZWFkLkFsbCBQbGFjZS5SZWFkIFBvbGljeS5SZWFkLkFsbCBQb2xpY3kuUmVhZC5QZXJtaXNzaW9uR3JhbnQgUG9saWN5LlJlYWRXcml0ZS5BdXRob3JpemF0aW9uIFBvbGljeS5SZWFkV3JpdGUuUGVybWlzc2lvbkdyYW50IFByZXNlbmNlLlJlYWQgUHJlc2VuY2UuUmVhZC5BbGwgUHJpbnRlclNoYXJlLlJlYWRCYXNpYy5BbGwgUHJpbnRKb2IuQ3JlYXRlIFByaW50Sm9iLlJlYWRCYXNpYyBwcm9maWxlIFJlcG9ydHMuUmVhZC5BbGwgU2l0ZXMuUmVhZFdyaXRlLkFsbCBUYXNrcy5SZWFkV3JpdGUgVGVhbS5DcmVhdGUgVGVhbS5SZWFkQmFzaWMuQWxsIFRlYW1NZW1iZXIuUmVhZC5BbGwgVGVhbU1lbWJlci5SZWFkV3JpdGUuQWxsIFRlYW1zQWN0aXZpdHkuU2VuZCBUZWFtc0FwcEluc3RhbGxhdGlvbi5SZWFkRm9yQ2hhdCBUZWFtc0FwcEluc3RhbGxhdGlvbi5SZWFkRm9yVGVhbSBUZWFtc0FwcEluc3RhbGxhdGlvbi5SZWFkRm9yVXNlciBUZWFtc0FwcEluc3RhbGxhdGlvbi5SZWFkV3JpdGVGb3JDaGF0IFRlYW1zQXBwSW5zdGFsbGF0aW9uLlJlYWRXcml0ZUZvclRlYW0gVGVhbXNBcHBJbnN0YWxsYXRpb24uUmVhZFdyaXRlRm9yVXNlciBUZWFtc0FwcEluc3RhbGxhdGlvbi5SZWFkV3JpdGVTZWxmRm9yVGVhbSBUZWFtU2V0dGluZ3MuUmVhZC5BbGwgVGVhbVNldHRpbmdzLlJlYWRXcml0ZS5BbGwgVGVhbXNUYWIuUmVhZFdyaXRlRm9yQ2hhdCBUZWFtc1RhYi5SZWFkV3JpdGVGb3JVc2VyIFRlYW13b3JrQXBwU2V0dGluZ3MuUmVhZC5BbGwgVGVhbXdvcmtBcHBTZXR0aW5ncy5SZWFkV3JpdGUuQWxsIFRlYW13b3JrRGV2aWNlLlJlYWQuQWxsIFRlYW13b3JrVGFnLlJlYWQgVGVhbXdvcmtUYWcuUmVhZFdyaXRlIFVzZXIuUmVhZCBVc2VyLlJlYWQuQWxsIFVzZXIuUmVhZEJhc2ljLkFsbCBVc2VyLlJlYWRXcml0ZSBVc2VyLlJlYWRXcml0ZS5BbGwgVXNlckFjdGl2aXR5LlJlYWRXcml0ZS5DcmVhdGVkQnlBcHAgVXNlck5vdGlmaWNhdGlvbi5SZWFkV3JpdGUuQ3JlYXRlZEJ5QXBwIFVzZXJUaW1lbGluZUFjdGl2aXR5LldyaXRlLkNyZWF0ZWRCeUFwcCBXb3JrZm9yY2VJbnRlZ3JhdGlvbi5SZWFkLkFsbCBXb3JrZm9yY2VJbnRlZ3JhdGlvbi5SZWFkV3JpdGUuQWxsIGVtYWlsIiwic2lnbmluX3N0YXRlIjpbImttc2kiXSwic3ViIjoieEE2QURPSlRpYWVWOXJzWXRmM2hubWN0ZlBqQW15UGJPdkdGYTFvODlUbyIsInRlbmFudF9yZWdpb25fc2NvcGUiOiJOQSIsInRpZCI6IjI0MzJiNTdiLTBhYmQtNDNkYi1hYTdiLTE2ZWFkZDExNWQzNCIsInVuaXF1ZV9uYW1lIjoiZ3JhcGh0ZXN0aW5ndXNlckB0ZWFtc2dyYXBoLm9ubWljcm9zb2Z0LmNvbSIsInVwbiI6ImdyYXBodGVzdGluZ3VzZXJAdGVhbXNncmFwaC5vbm1pY3Jvc29mdC5jb20iLCJ1dGkiOiJyeFR5Q3pRSzdVMml1c0kyZ3lrNUFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX2NjIjpbIkNQMSJdLCJ4bXNfc3NtIjoiMSIsInhtc19zdCI6eyJzdWIiOiJydUlXbTA5M3NPM05CVEpIWWFKODhXbEtXTW9ZbXFoOTJhUjlfVy1wV2ZFIn0sInhtc190Y2R0IjoxNTc3MTQyNzQ2fQ.kk-A8VIOKwkse3RjTa3AaBfZZpoMmx1UJ7cErEpzM1Jz5_lOfOw7PM3pbVsTlWi6QquLlru8TdL5tfkw85j5gsRPzdVuh0YuDDNNvjxqj5LiDv44lpco8631xcYahiKGHwk51AhgP4gEQtQFrA7b5v66jxuqEcfiAywJ-9ZXH1u9wo6jB17IFS_1sO32YBYSF595dAQBSS6FfcmQqw-AJUU0mJQS0sCIUMCKCsVfOx6kUZK8sEU9MM9YtJbcfm-UGqo7-byAZ3FlObIi8Zs1fwXpWqqdjRtWQ75-FD6wEKyeV9X5n2nVI05QMIoQUnhd8PkWxDn_mQCxErYmX1ND7w"}

            idx = 0
            httpMethodFound = False

            for responseStr in responseArr:
                if (responseStr in ["GET", "POST", "PUT", "DELETE"]):
                    httpMethodFound = True
                    break
                else:
                    idx = idx + 1
            output = {}
            if httpMethodFound:
                if responseArr[idx] == "GET":
                    apiresponse = requests.get(responseArr[idx + 1], headers=headers)
                    json_api_response = apiresponse.json()
                    parsed = json.dumps(json_api_response, indent=4)
                    output["Content"] = parsed
                    output["Header"] = str(apiresponse.headers)
                    return output
                elif responseArr[idx] == "POST":
                    responseStr = response.response 
                    startIndex = responseStr.find('{')
                    requestBody = responseStr[startIndex:]
                    jsonBody = json.loads(requestBody)
                    apiresponse = requests.post(responseArr[idx + 1], headers=headers, json=jsonBody)
                    output["Content"] = apiresponse.content.decode()
                    output["Header"] = str(apiresponse.headers)
                    return output
                else:
                    print("Method not supported")
            else:
                print("Sorry, was not able to parse the response properly from the response prompt! Please try asking the question differently.")
            return None

    def run(self):
        if __name__ == '__main__':
            self.app.run(debug=True, port=5000)

# Initialize the application
my_app = MyApp()
my_app.run()
