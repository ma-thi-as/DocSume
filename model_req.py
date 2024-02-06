import json
import requests

# NOTE: ollama must be running for this to work, start the ollama app or run `ollama serve`
model = 'mistral' # TODO: update this for whatever model you wish to use

async def generate(prompt, context):
    text = ''
    r = requests.post('http://localhost:11434/api/generate',
                      json={
                          'model': model,
                          'prompt': prompt,
                          'context': context,
                      },
                      stream=True)
    r.raise_for_status()
    
    try:
        for line in r.iter_lines():
            body = json.loads(line)
            response_part = body.get('response', '')
            # the response streams one token at a time, print that as we receive it
            text += response_part
            
            if 'error' in body:
                raise Exception(body['error'])

            if body.get('done', False):
                return text
    except KeyboardInterrupt:
        print("Generation interrupted by user.")
        return None
