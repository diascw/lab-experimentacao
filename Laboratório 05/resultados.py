import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

csv_name = 'experiment_results.csv'
df = pd.read_csv(csv_name)

ok_df = df[(df['ok'] == True) & (df['status_code'] == 200)]

summary = ok_df.groupby('type')[['time_ms','size_bytes']].agg(['count','mean','std','median']).round(3)
print(summary)

# Paired analysis
rest_times = ok_df[ok_df.type == 'REST'].sort_values('id')['time_ms'].values
graphql_times = ok_df[ok_df.type == 'GraphQL'].sort_values('id')['time_ms'].values
rest_sizes = ok_df[ok_df.type == 'REST'].sort_values('id')['size_bytes'].values
graphql_sizes = ok_df[ok_df.type == 'GraphQL'].sort_values('id')['size_bytes'].values

n_pairs = min(len(rest_times), len(graphql_times))
rest_times = rest_times[:n_pairs]
graphql_times = graphql_times[:n_pairs]
rest_sizes = rest_sizes[:n_pairs]
graphql_sizes = graphql_sizes[:n_pairs]

diff_time = graphql_times - rest_times
diff_size = graphql_sizes - rest_sizes

pvals = {}
method = None
try:
    from scipy import stats
    t_time, p_time_two = stats.ttest_rel(graphql_times, rest_times, alternative='less')
    t_size, p_size_two = stats.ttest_rel(graphql_sizes, rest_sizes, alternative='less')
    pvals['time'] = float(p_time_two)
    pvals['size'] = float(p_size_two)
    method = 'paired t-test (SciPy) one-sided (GraphQL < REST)'
except Exception as e:
    import numpy as np
    rng = np.random.default_rng(42)
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

# Plots
sns.set(style='whitegrid')
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

pair_df = ok_df.sort_values(['id','type'])
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

pivot_size = pair_df.pivot(index='id', columns='type', values='size_bytes')
plt.figure(figsize=(8, 6))
for _id, row in pivot_size.iterrows():
    plt.plot(['REST','GraphQL'], [row['REST'], row['GraphQL']], marker='o', color='gray', alpha=0.5)
plt.title('Tamanho por ID (pareado)')
plt.ylabel('bytes')
plt.savefig('paired_size.png', dpi=150)
plt.close()

# Compose report
report = []
report.append('# Lab05 - GraphQL vs REST - Relatório')
report.append('')
report.append('## Sumário descritivo (respostas 200)')
report.append(summary.to_markdown())
report.append('')
report.append('## Testes de hipótese (GraphQL < REST)')
report.append(f'- Método: {method}')
report.append(f'- n_pairs: {n_pairs}')
report.append(f'- Diferença média de tempo (GraphQL-REST): {np.mean(diff_time):.3f} ms, p-valor={pvals["time"]:.5f}')
report.append(f'- Diferença média de tamanho (GraphQL-REST): {np.mean(diff_size):.1f} bytes, p-valor={pvals["size"]:.5f}')

with open('lab05_report.md', 'a', encoding='utf-8') as f:
    f.write('\n'.join(['', '---', ''] + report))

print('Analysis complete and lab05_report.md updated.')