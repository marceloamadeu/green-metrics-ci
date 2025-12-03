import json
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np

def parse_eco_ci_logs(data_dir="data/raw"):
    """
    Parseia os JSONs do Eco-CI baixados do GitHub Actions.
    Estrutura esperada: data/raw/rodada-X-estrategia-Y/eco-ci-output.json
    """
    results = []
    
    for json_file in glob.glob(f"{data_dir}/**/*output*.json", recursive=True):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                
            # Extrair informações do caminho do arquivo
            path_parts = json_file.split(os.sep)
            rodada = int([p for p in path_parts if 'rodada' in p][0].split('-')[1])
            estrategia = [p for p in path_parts if any(s in p for s in ['baseline', 'parallel', 'tia'])][0]
            
            # Extrair métricas
            results.append({
                'rodada': rodada,
                'estrategia': estrategia,
                'energia_mj': data.get('energy-total', {}).get('value', 0),
                'duracao_s': data.get('duration', {}).get('value', 0) / 1000,  # ms para s
                'co2_g': data.get('co2-total', {}).get('value', 0),
                'cpu_avg': data.get('cpu-avg', {}).get('value', 0)
            })
        except Exception as e:
            print(f"⚠️ Erro ao processar {json_file}: {e}")
    
    return pd.DataFrame(results)

def calcular_edp(df):
    """Calcula o Produto Energia-Atraso (Energy-Delay Product)"""
    df['energia_j'] = df['energia_mj'] / 1000  # mJ para J
    df['edp'] = df['energia_j'] * df['duracao_s']
    return df

def teste_hipoteses(df):
    """
    Testa as hipóteses H1 e H2 do artigo.
    """
    print("\n" + "="*60)
    print("TESTES DE HIPÓTESE")
    print("="*60)
    
    baseline = df[df['estrategia'] == 'baseline']['energia_j']
    tia = df[df['estrategia'] == 'tia']['energia_j']
    paralelo = df[df['estrategia'] == 'parallel']['energia_j']
    
    # H1: TIA reduz energia significativamente vs Baseline
    print("\n📊 H1: TIA vs Baseline (Energia)")
    stat, p_value = stats.wilcoxon(baseline, tia)
    reducao = ((baseline.mean() - tia.mean()) / baseline.mean()) * 100
    print(f"   Redução média: {reducao:.1f}%")
    print(f"   p-value: {p_value:.4f}")
    print(f"   Conclusão: {'✅ Rejeitamos H0' if p_value < 0.05 else '❌ Não rejeitamos H0'}")
    
    # Cohen's d (tamanho do efeito)
    cohens_d = (baseline.mean() - tia.mean()) / np.sqrt((baseline.std()**2 + tia.std()**2) / 2)
    print(f"   Cohen's d: {cohens_d:.2f} ({'Grande' if abs(cohens_d) > 0.8 else 'Médio' if abs(cohens_d) > 0.5 else 'Pequeno'})")
    
    # H2: Paralelo tem EDP maior que Baseline
    print("\n📊 H2: Paralelo vs Baseline (EDP)")
    edp_baseline = df[df['estrategia'] == 'baseline']['edp']
    edp_paralelo = df[df['estrategia'] == 'parallel']['edp']
    
    stat, p_value = stats.mannwhitneyu(edp_baseline, edp_paralelo, alternative='less')
    aumento = ((edp_paralelo.mean() - edp_baseline.mean()) / edp_baseline.mean()) * 100
    print(f"   Aumento médio no EDP: {aumento:.1f}%")
    print(f"   p-value: {p_value:.4f}")
    print(f"   Conclusão: {'✅ Rejeitamos H0' if p_value < 0.05 else '❌ Não rejeitamos H0'}")

def visualizar_resultados(df, output_dir="data/plots"):
    """
    Gera gráficos para o artigo.
    """
    os.makedirs(output_dir, exist_ok=True)
    sns.set_style("whitegrid")
    plt.rcParams['figure.dpi'] = 300
    
    # 1. Boxplot de Energia por Estratégia
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='estrategia', y='energia_j', palette='Set2')
    plt.title('Distribuição do Consumo de Energia por Estratégia')
    plt.xlabel('Estratégia de Teste')
    plt.ylabel('Energia (Joules)')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/energia_boxplot.png")
    plt.close()
    print(f"✅ Gráfico salvo: {output_dir}/energia_boxplot.png")
    
    # 2. Scatter Plot: Energia vs Tempo
    plt.figure(figsize=(10, 6))
    for estrategia in df['estrategia'].unique():
        subset = df[df['estrategia'] == estrategia]
        plt.scatter(subset['duracao_s'], subset['energia_j'], 
                   label=estrategia, alpha=0.7, s=100)
    
    plt.xlabel('Tempo de Execução (s)')
    plt.ylabel('Energia (J)')
    plt.title('Trade-off Energia vs Tempo')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/energia_vs_tempo.png")
    plt.close()
    print(f"✅ Gráfico salvo: {output_dir}/energia_vs_tempo.png")
    
    # 3. Barras de Redução Percentual
    baseline_mean = df[df['estrategia'] == 'baseline']['energia_j'].mean()
    reducoes = []
    
    for estrategia in ['parallel', 'tia']:
        mean_energia = df[df['estrategia'] == estrategia]['energia_j'].mean()
        reducao = ((baseline_mean - mean_energia) / baseline_mean) * 100
        reducoes.append({'Estratégia': estrategia, 'Redução (%)': reducao})
    
    plt.figure(figsize=(8, 6))
    reducoes_df = pd.DataFrame(reducoes)
    sns.barplot(data=reducoes_df, x='Estratégia', y='Redução (%)', palette='coolwarm')
    plt.title('Redução de Energia vs Baseline')
    plt.ylabel('Redução Percentual (%)')
    plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/reducao_energia.png")
    plt.close()
    print(f"✅ Gráfico salvo: {output_dir}/reducao_energia.png")

def gerar_relatorio(df):
    """
    Gera relatório em texto com estatísticas descritivas.
    """
    print("\n" + "="*60)
    print("ESTATÍSTICAS DESCRITIVAS")
    print("="*60)
    
    for estrategia in df['estrategia'].unique():
        subset = df[df['estrategia'] == estrategia]
        print(f"\n📌 {estrategia.upper()}")
        print(f"   Energia (J):  {subset['energia_j'].mean():.2f} ± {subset['energia_j'].std():.2f}")
        print(f"   Tempo (s):    {subset['duracao_s'].mean():.2f} ± {subset['duracao_s'].std():.2f}")
        print(f"   EDP (J·s):    {subset['edp'].mean():.2f} ± {subset['edp'].std():.2f}")
        print(f"   CO2 (g):      {subset['co2_g'].mean():.2f} ± {subset['co2_g'].std():.2f}")

def main():
    print("🔍 Processando Métricas do Experimento Green Metrics...")
    
    # 1. Parsear dados
    df = parse_eco_ci_logs()
    
    if df.empty:
        print("❌ Nenhum dado encontrado em data/raw/")
        print("   Certifique-se de baixar os artifacts do GitHub Actions:")
        print("   gh run list --limit 30")
        print("   gh run download <RUN_ID>")
        return
    
    print(f"✅ {len(df)} execuções carregadas")
    
    # 2. Calcular métricas derivadas
    df = calcular_edp(df)
    
    # 3. Salvar dados consolidados
    df.to_csv('data/resultados_consolidados.csv', index=False)
    print("✅ Dados salvos em: data/resultados_consolidados.csv")
    
    # 4. Estatísticas descritivas
    gerar_relatorio(df)
    
    # 5. Testes de hipótese
    teste_hipoteses(df)
    
    # 6. Visualizações
    visualizar_resultados(df)
    
    print("\n✅ Análise Completa!")

if __name__ == "__main__":
    main()