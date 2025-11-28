import requests
import time
import pandas as pd
import json

REST_URL = "https://rickandmortyapi.com/api/character/"
GRAPHQL_URL = "https://rickandmortyapi.com/graphql"
NUM_TRIALS = 50  # Quantidade de medições (IDs de 1 a 50)

results = []

def run_rest_request(char_id):
    """Executa a chamada REST e retorna tempo e tamanho."""
    start_time = time.time()
    
    response = requests.get(f"{REST_URL}{char_id}")
    
    end_time = time.time()
    
    duration = (end_time - start_time) * 1000 
    size = len(response.content)
    
    return duration, size

def run_graphql_request(char_id):
    """Executa a chamada GraphQL (apenas campos específicos) e retorna tempo e tamanho."""
    query = """
    query {
      character(id: "%s") {
        name
        species
        status
      }
    }
    """ % char_id
    
    start_time = time.time()
    
    response = requests.post(GRAPHQL_URL, json={'query': query})
    
    end_time = time.time()
    
    duration = (end_time - start_time) * 1000
    size = len(response.content)
    
    return duration, size

print(f"--- Iniciando Experimento com {NUM_TRIALS} iterações ---")

print("Realizando warm-up...")
requests.get(f"{REST_URL}1")
requests.post(GRAPHQL_URL, json={'query': '{ character(id: "1") { name } }'})

for i in range(1, NUM_TRIALS + 1):
    char_id = str(i)
    
    rest_time, rest_size = run_rest_request(char_id)
    results.append({
        "id": char_id,
        "type": "REST",
        "time_ms": rest_time,
        "size_bytes": rest_size
    })
    
    time.sleep(0.1) 
    
    gql_time, gql_size = run_graphql_request(char_id)
    results.append({
        "id": char_id,
        "type": "GraphQL",
        "time_ms": gql_time,
        "size_bytes": gql_size
    })
    
    print(f"Trial {i}/{NUM_TRIALS} completo.")

df = pd.DataFrame(results)
filename = "experiment_results.csv"
df.to_csv(filename, index=False)

print(f"\n--- Experimento Finalizado ---")
print(f"Dados salvos em: {filename}")
print(df.groupby('type').mean())