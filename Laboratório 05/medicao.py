import requests, time, random, csv, json, statistics, os
import pandas as pd
import numpy as np
import math
from datetime import datetime

REST_URL = "https://rickandmortyapi.com/api/character/"
GRAPHQL_URL = "https://rickandmortyapi.com/graphql"
NUM_TRIALS = 50
RANDOM_SEED = 42
TIMEOUT = 20
SLEEP_BETWEEN = 0.1
HEADERS = {"Accept": "application/json", "User-Agent": "Lab05-Experiment/1.0"}

random.seed(RANDOM_SEED)

session = requests.Session()
session.headers.update(HEADERS)

# Warm-up
try:
    session.get(f"{REST_URL}1", timeout=TIMEOUT)
    session.post(GRAPHQL_URL, json={"query": '{ character(id: "1") { name } }'}, timeout=TIMEOUT)
except Exception as e:
    print("Warm-up warning:", e)

ids = list(range(1, NUM_TRIALS + 1))
random.shuffle(ids)

rows = []

def now_iso():
    return datetime.utcnow().isoformat() + "Z"

for idx, char_id in enumerate(ids, 1):
    # REST
    start = time.perf_counter()
    start_ts = now_iso()
    try:
        r = session.get(f"{REST_URL}{char_id}", timeout=TIMEOUT)
        content = r.content or b""
        ok = r.ok
        status = r.status_code
    except Exception as e:
        content = b""
        ok = False
        status = None
    end = time.perf_counter()
    end_ts = now_iso()
    rows.append({
        "id": char_id,
        "type": "REST",
        "time_ms": (end - start) * 1000.0,
        "size_bytes": len(content),
        "status_code": status,
        "ok": ok,
        "start_ts": start_ts,
        "end_ts": end_ts
    })

    time.sleep(SLEEP_BETWEEN)

    # GraphQL
    query = """
    query($id: ID!) {
      character(id: $id) {
        name
        species
        status
      }
    }
    """
    payload = {"query": query, "variables": {"id": str(char_id)}}
    start = time.perf_counter()
    start_ts = now_iso()
    try:
        r = session.post(GRAPHQL_URL, json=payload, timeout=TIMEOUT)
        content = r.content or b""
        ok = r.ok
        status = r.status_code
    except Exception as e:
        content = b""
        ok = False
        status = None
    end = time.perf_counter()
    end_ts = now_iso()
    rows.append({
        "id": char_id,
        "type": "GraphQL",
        "time_ms": (end - start) * 1000.0,
        "size_bytes": len(content),
        "status_code": status,
        "ok": ok,
        "start_ts": start_ts,
        "end_ts": end_ts
    })

    print(f"Trial {idx}/{NUM_TRIALS} (ID {char_id}) done.")

# Save CSV
csv_name = "experiment_results.csv"
pd.DataFrame(rows).to_csv(csv_name, index=False)
print(f"Saved {csv_name} with {len(rows)} rows.")

# Basic analysis

df = pd.DataFrame(rows)
# Keep only successful responses
ok_df = df[(df["ok"] == True) & (df["status_code"] == 200)]

summary = ok_df.groupby("type")["time_ms", "size_bytes"].agg(["count", "mean", "std", "median"]).round(3)
print("\nSuccessful responses summary:\n", summary)

# Paired analysis
rest_times = ok_df[ok_df.type == "REST"].sort_values("id")["time_ms"].values
graphql_times = ok_df[ok_df.type == "GraphQL"].sort_values("id")["time_ms"].values
rest_sizes = ok_df[ok_df.type == "REST"].sort_values("id")["size_bytes"].values
graphql_sizes = ok_df[ok_df.type == "GraphQL"].sort_values("id")["size_bytes"].values

n_pairs = min(len(rest_times), len(graphql_times))
rest_times = rest_times[:n_pairs]
graphql_times = graphql_times[:n_pairs]
rest_sizes = rest_sizes[:n_pairs]
graphql_sizes = graphql_sizes[:n_pairs]

diff_time = graphql_times - rest_times
diff_size = graphql_sizes - rest_sizes

# Try SciPy; if unavailable, fall back to permutation test
pvals = {}
try:
    from scipy import stats
    t_time, p_time_two = stats.ttest_rel(graphql_times, rest_times, alternative='less')
    t_size, p_size_two = stats.ttest_rel(graphql_sizes, rest_sizes, alternative='less')
    pvals['time'] = float(p_time_two)
    pvals['size'] = float(p_size_two)
    method = 'paired t-test (SciPy) one-sided (GraphQL < REST)'
except Exception as e:
    # Permutation test (sign-flip) for mean difference
    rng = np.random.default_rng(RANDOM_SEED)
    B = 20000
    obs_time = np.mean(diff_time)
    obs_size = np.mean(diff_size)
    count_time = 0
    count_size = 0
    for _ in range(B):
        signs = rng.choice([-1, 1], size=n_pairs)
        perm_time = np.mean(diff_time * signs)
        perm_size = np.mean(diff_size * signs)
        if perm_time <= obs_time:
            count_time += 1
        if perm_size <= obs_size:
            count_size += 1
    pvals['time'] = (count_time + 1) / (B + 1)
    pvals['size'] = (count_size + 1) / (B + 1)
    method = f'one-sided sign-flip permutation test (B={B}) for mean difference'

print(f"\nPaired inference method: {method}")
print(f"n_pairs used: {n_pairs}")
print(f"Mean diff time (GraphQL-REST): {np.mean(diff_time):.3f} ms -> p-value={pvals['time']:.5f}")
print(f"Mean diff size (GraphQL-REST): {np.mean(diff_size):.1f} bytes -> p-value={pvals['size']:.5f}")

# Create dashboard plots
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')

# Boxplots
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
sns.boxplot(data=ok_df, x='type', y='time_ms', ax=ax[0])
ax[0].set_title('Tempo de resposta (ms)')
ax[0].set_xlabel('API')
ax[0].set_ylabel('ms')

sns.boxplot(data=ok_df, x='type', y='size_bytes', ax=ax[1])
ax[1].set_title('Tamanho da resposta (bytes)')
ax[1].set_xlabel('API')
ax[1].set_ylabel('bytes')

plt.tight_layout()
plt.savefig('dashboard_boxplots.png', dpi=150)
plt.close()

# Paired lines for time
pair_df = ok_df.sort_values(['id','type'])
# ensure both types per id
ids_with_both = pair_df.groupby('id')['type'].nunique()
ids_with_both = ids_with_both[ids_with_both == 2].index
pair_df = pair_df[pair_df['id'].isin(ids_with_both)]

pivot_time = pair_df.pivot(index='id', columns='type', values='time_ms')
plt.figure(figsize=(8, 6))
for _id, row in pivot_time.iterrows():
    plt.plot(['REST','GraphQL'], [row['REST'], row['GraphQL']], marker='o', color='gray', alpha=0.5)
plt.title('Tempo por ID (pareado)')
plt.ylabel('ms')
plt.savefig('paired_time.png', dpi=150)
plt.close()

# Paired lines for size
pivot_size = pair_df.pivot(index='id', columns='type', values='size_bytes')
plt.figure(figsize=(8, 6))
for _id, row in pivot_size.iterrows():
    plt.plot(['REST','GraphQL'], [row['REST'], row['GraphQL']], marker='o', color='gray', alpha=0.5)
plt.title('Tamanho por ID (pareado)')
plt.ylabel('bytes')
plt.savefig('paired_size.png', dpi=150)
plt.close()

print('Saved dashboard_boxplots.png, paired_time.png, paired_size.png')

# Compose a minimal report.md summarizing
report_lines = []
report_lines.append('# Lab05 - GraphQL vs REST - Relatório')
report_lines.append('')
report_lines.append('## Metodologia')
report_lines.append(f'- Endpoints: REST={REST_URL}{{id}}, GraphQL={GRAPHQL_URL}')
report_lines.append(f'- IDs: {ids[:5]} ... (total {NUM_TRIALS}) [ordem aleatória, seed={RANDOM_SEED}]')
report_lines.append('- Tratamentos: REST (GET objeto completo) vs GraphQL (query com campos name/species/status)')
report_lines.append('- Warm-up: 1 request em cada API descartado')
report_lines.append('- Medições: tempo wall-clock (ms) e tamanho do corpo (bytes)')
report_lines.append('- Design: pareado (mesmo id para ambos)')
report_lines.append('')
report_lines.append('## Resultados (respostas bem-sucedidas)')
report_lines.append('')
report_lines.append(summary.to_markdown())
report_lines.append('')
report_lines.append('## Testes de hipótese (GraphQL < REST)')
report_lines.append(f'- Método: {method}')
report_lines.append(f'- n_pairs: {n_pairs}')
report_lines.append(f'- Diferença média de tempo (GraphQL-REST): {np.mean(diff_time):.3f} ms, p-valor={pvals["time"]:.5f}')
report_lines.append(f'- Diferença média de tamanho (GraphQL-REST): {np.mean(diff_size):.1f} bytes, p-valor={pvals["size"]:.5f}')
report_lines.append('')
report_lines.append('## Figuras')
report_lines.append('![](dashboard_boxplots.png)')
report_lines.append('')
report_lines.append('![](paired_time.png)')
report_lines.append('')
report_lines.append('![](paired_size.png)')

with open('lab05_report.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print('Saved lab05_report.md')