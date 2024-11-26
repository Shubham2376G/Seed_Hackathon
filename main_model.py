
import aisuite as ai

def main_inference(model_name,symptoms,cbc_report,xray):
  client = ai.Client()

  if model_name == "gemma:2b":
    models = ["ollama:gemma:2b"]
  elif model_name == "Mistral:7b":
    models = ["ollama:mistral:7b"]
  elif model_name == "Medllama2:7b":
    models = ["ollama:medllama2:7b"]
  elif model_name == "Meditron:7b":
    models = ["ollama:meditron:7b"]
  elif model_name == "GPT4":
    models = ["gpt-4"]
  else model_name == "GPT3.5":
    models = ["gpt-3.5-turbo"]


  messages = [
      {"role": "system", "content": "You are a doctor, I have provided you patient history, his blood test result (if any) and x ray result (if any), using this information , identify which disease the patient might be suffering from, give response in following dictionary format {response: your response , logs: here you will give explaination of why you gave this result } "},
      {"role": "user", "content": f"patient history are {symptoms} , blood test report is {cbc_report} , and xray result {xray} "},
  ]


  response = client.chat.completions.create(
      model=model,
      messages=messages,
      temperature=0.1
  )
  return response.choices[0].message.content

