#!/usr/bin/env python3
"""
Analisa métricas coletadas com /usr/bin/time -v
"""

import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np

def parse_time_output(filepath):
    """Parse do output do /usr/bin/time -v"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    metrics = {}
    
    # Extrair estratégia e run_id
    estrategia_match = re.search(r'Estratégia:\s+(\w+)', content)
    runid_match = re.search(r'Run ID:\s+(\d+)', content)
    
    if estrategia_match:
        metrics['estrategia'] = estrategia_match.group(1).lower()
    if runid_match:
        metrics['run_id'] = runid_match.group(1)
    
    # Extrair métricas do /usr/bin/time -v
    # Elapsed (wall clock) time (h:mm:ss or m:ss): 0:01.23
    elapsed_match = re.search(r'Elapsed.*?:\s+(\d+):(\d+\.\d+)', content)
    if elapsed_match:
        minutes = int(elapsed_match.group(1))
        seconds = float(elapsed_match.group(2))
        metrics['tempo_s'] = minutes * 60 + seconds
    
    # User time (seconds): 1.23
    user_time_match = re.search(r'User time.*?:\s+(\d+\.\d+)', content)
    if user_time_match:
        metrics['cpu_user_s'] = float(user_time_match.group(1))
    
    # System time (seconds): 0.12
    sys_time_match = re.search(r'System time.*?:\s+(\d+\.\d+)', content)
    if sys_time_match:
        metrics['cpu_sys_s'] = float(sys_time_match.group(1))
    
    # Percent of CPU this job got: 95%
    cpu_pct_match = re.search(r'Percent of CPU.*?:\s+(\d+)%', content)
    if cpu_pct_match:
        metrics['cpu_pct'] = int(cpu_pct_match.group(1))
    
    # Maximum resident set size (kbytes): 12345
    mem_match = re.search(r'Maximum resident set size.*?:\s+(\d+)', content)
    if mem_match:
        metrics['mem_max_kb'] = int(mem_match.group(1))
        metrics['mem_max_mb'] = metrics['mem_max_kb'] / 1024
    
    # Voluntary context switches: 123
    vol_ctx_match = re.search(r'Voluntary context switches.*?:\s+(\d+)', content)
    if vol_ctx_match:
        metrics['ctx_switches_vol'] = int(vol_ctx_match.group(1))
    
    # Involuntary context switches: 45
    invol_ctx_match = re.search(r'Involuntary context switches.*?:\s+(\d+)', content)
    if invol_ctx_match:
        metrics['ctx_switches_invol'] = int(invol_ctx_match.group(1))
    
    # Contar número de testes
    tests_match = re.findall(r'(\d+) passed', content)
    if tests_match:
        metrics['testes_executados'] = int(tests_match[-1])
    
    return metrics

def load_all_metrics(data_dir='data/raw'):
    """Carrega todas as métricas de todos os runs"""
    results = []
    
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file == 'metrics.txt':
                filepath = os.path.join(root, file)
                print(f"📄 Processando: {filepath}")
                
                try:
                    metrics = parse_time_output(filepath)
                    if metrics:
                        results.append(metrics)
                        print(f"   ✅ {metrics.get('estrategia', '?')} - {metrics.get('tempo_s', 0):.2f}s")
                except Exception as e:
                    print(f"   ❌ Erro: {e}")
    
    return pd.DataFrame(results)

def calcular_metricas_derivadas(df):
    """Calcula métricas adicionais"""
    # CPU total
    df['cpu_total_s'] = df['cpu_user_s'] + df['cpu_sys_s']
    
    # Energia estimada (J) = CPU_time × CPU_cores × TDP_estimado
    # Assumindo TDP médio de ~15W por core em uso
    TDP_PER_CORE = 15  # Watts
    df['energia_estimada_j'] = df['cpu_total_s'] * TDP_PER_CORE
    
    # EDP (Energy-Delay Product)
    df['edp'] = df['energia_estimada_j'] * df['tempo_s']
    
    return df

def teste_hipoteses(df):
    """Testa H1 e H2"""
    print("\n" + "="*60)
    print("TESTES DE HIPÓTESE")
    print("="*60)
    
    baseline = df[df['estrategia'] == 'baseline']
    parallel = df[df['estrategia'] == 'parallel']
    tia = df[df['estrategia'] == 'tia']
    
    if len(baseline) == 0 or len(tia) == 0:
        print("⚠️ Dados insuficientes para testes estatísticos")
        return
    
    # H1: TIA reduz tempo vs Baseline
    print("\n📊 H1: TIA vs Baseline (Tempo)")
    if len(baseline) >= 3 and len(tia) >= 3:
        stat, p_value = stats.mannwhitneyu(baseline['tempo_s'], tia['tempo_s'], alternative='greater')
        reducao = ((baseline['tempo_s'].mean() - tia['tempo_s'].mean()) / baseline['tempo_s'].mean()) * 100
        print(f"   Redução média: {reducao:.1f}%")
        print(f"   p-value: {p_value:.4f}")
        print(f"   Conclusão: {'✅ Rejeitamos H0' if p_value < 0.05 else '⚠️ Não rejeitamos H0 (n pequeno?)'}")
    else:
        print(f"   ⚠️ Dados insuficientes (baseline: {len(baseline)}, tia: {len(tia)})")
    
    # H2: Paralelo tem EDP diferente de Baseline
    if len(baseline) >= 3 and len(parallel) >= 3:
        print("\n📊 H2: Paralelo vs Baseline (EDP)")
        stat, p_value = stats.mannwhitneyu(baseline['edp'], parallel['edp'])
        diff = ((parallel['edp'].mean() - baseline['edp'].mean()) / baseline['edp'].mean()) * 100
        print(f"   Diferença no EDP: {diff:+.1f}%")
        print(f"   p-value: {p_value:.4f}")
        print(f"   Conclusão: {'✅ Diferença significativa' if p_value < 0.05 else '⚠️ Sem diferença significativa'}")

def gerar_relatorio(df):
    """Relatório descritivo"""
    print("\n" + "="*60)
    print("ESTATÍSTICAS DESCRITIVAS")
    print("="*60)
    
    for estrategia in ['baseline', 'parallel', 'tia']:
        subset = df[df['estrategia'] == estrategia]
        if len(subset) == 0:
            continue
        
        print(f"\n📌 {estrategia.upper()} (n={len(subset)})")
        print(f"   Tempo (s):        {subset['tempo_s'].mean():.2f} ± {subset['tempo_s'].std():.2f}")
        print(f"   CPU Total (s):    {subset['cpu_total_s'].mean():.2f} ± {subset['cpu_total_s'].std():.2f}")
        print(f"   CPU %:            {subset['cpu_pct'].mean():.0f} ± {subset['cpu_pct'].std():.0f}")
        print(f"   Memória (MB):     {subset['mem_max_mb'].mean():.1f} ± {subset['mem_max_mb'].std():.1f}")
        print(f"   Energia Est. (J): {subset['energia_estimada_j'].mean():.1f} ± {subset['energia_estimada_j'].std():.1f}")
        print(f"   EDP (J·s):        {subset['edp'].mean():.1f} ± {subset['edp'].std():.1f}")
        if 'testes_executados' in subset.columns:
            print(f"   Testes:           {subset['testes_executados'].mean():.0f}")

def visualizar(df, output_dir='data/plots'):
    """Gera gráficos"""
    os.makedirs(output_dir, exist_ok=True)
    sns.set_style("whitegrid")
    
    # 1. Tempo de Execução
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='estrategia', y='tempo_s', palette='Set2')
    plt.title('Tempo de Execução por Estratégia')
    plt.xlabel('Estratégia')
    plt.ylabel('Tempo (segundos)')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/tempo_boxplot.png', dpi=300)
    plt.close()
    print(f"✅ Gráfico salvo: {output_dir}/tempo_boxplot.png")
    
    # 2. Uso de CPU
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='estrategia', y='cpu_pct', palette='Set2')
    plt.title('Utilização de CPU por Estratégia')
    plt.xlabel('Estratégia')
    plt.ylabel('CPU (%)')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/cpu_boxplot.png', dpi=300)
    plt.close()
    print(f"✅ Gráfico salvo: {output_dir}/cpu_boxplot.png")
    
    # 3. EDP
    if 'edp' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x='estrategia', y='edp', palette='Set2')
        plt.title('Energy-Delay Product por Estratégia')
        plt.xlabel('Estratégia')
        plt.ylabel('EDP (J·s)')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/edp_boxplot.png', dpi=300)
        plt.close()
        print(f"✅ Gráfico salvo: {output_dir}/edp_boxplot.png")

def main():
    print("🔍 Analisando Métricas Simples (time -v)...")
    print("")
    
    # Carregar dados
    df = load_all_metrics()
    
    if df.empty:
        print("❌ Nenhum dado encontrado!")
        print("\n📍 Certifique-se de:")
        print("   1. Baixar os artifacts: gh run download <RUN_ID>")
        print("   2. Extrair em data/raw/")
        print("   3. Cada pasta deve ter um arquivo metrics.txt")
        return
    
    print(f"\n✅ {len(df)} execuções carregadas")
    
    # Calcular métricas derivadas
    df = calcular_metricas_derivadas(df)
    
    # Salvar CSV
    df.to_csv('data/resultados_simple.csv', index=False)
    print(f"✅ Dados salvos: data/resultados_simple.csv")
    
    # Relatório
    gerar_relatorio(df)
    
    # Testes estatísticos
    teste_hipoteses(df)
    
    # Gráficos
    visualizar(df)
    
    print("\n✅ Análise Completa!")

if __name__ == "__main__":
    main()