
import aisuite as ai

def main_inference(model_name,symptoms,cbc_report,xray):
  client = ai.Client()

  if model_name == "Gemma:2b":
    models = "ollama:gemma:2b"
  elif model_name == "Mistral:7b":
    models = "ollama:mistral:7b"
  elif model_name == "Medllama2:7b":
    models = "ollama:medllama2:7b"
  elif model_name == "Meditron:7b":
    models = "ollama:meditron:7b"
  elif model_name == "GPT4":
    models = "gpt-4"
  else :
    models = "ollama:gemma:2b"


  messages = [
      {"role": "system", "content": "You are a doctor, I have provided you patient symptoms {symptoms} , tell the potential disease patient might be suffering from."},
      {"role": "user", "content": f"patient history are {symptoms} tell me which diagnosis to do "},
      # {"role": "user", "content": f"patient history are {symptoms} , blood test report is {cbc_report} , and xray result {xray} "},
  ]


  response = client.chat.completions.create(
      model=models,
      messages=messages,
      temperature=0.1
  )
  return response.choices[0].message.content

