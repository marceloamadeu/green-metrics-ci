#!/usr/bin/env python3
"""
Gera visualizações profissionais para o artigo
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Configurações globais
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['legend.fontsize'] = 10

# Paleta de cores profissional
COLORS = {
    'baseline': '#7fb3d5',  # Azul suave
    'parallel': '#e74c3c',  # Vermelho (alerta)
    'tia': '#27ae60'        # Verde (sucesso)
}

ORDER = ['baseline', 'parallel', 'tia']
LABELS = {
    'baseline': 'Baseline\n(Sequencial)',
    'parallel': 'Paralelo\n(xdist)',
    'tia': 'TIA\n(Testmon)'
}

def load_data(filepath='data/resultados_simple.csv'):
    """Carrega dados"""
    df = pd.read_csv(filepath)
    return df

def create_tempo_plot(df, output_dir='data/plots'):
    """Gráfico de Tempo de Execução"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Criar boxplot com cores customizadas
    bp = ax.boxplot(
        [df[df['estrategia'] == s]['tempo_s'].values for s in ORDER],
        labels=[LABELS[s] for s in ORDER],
        patch_artist=True,
        widths=0.6,
        showmeans=True,
        meanprops=dict(marker='D', markerfacecolor='white', 
                      markeredgecolor='black', markersize=6)
    )
    
    # Colorir boxes
    for patch, estrategia in zip(bp['boxes'], ORDER):
        patch.set_facecolor(COLORS[estrategia])
        patch.set_alpha(0.7)
    
    # Adicionar valores médios como texto
    for i, estrategia in enumerate(ORDER, 1):
        mean_val = df[df['estrategia'] == estrategia]['tempo_s'].mean()
        ax.text(i, mean_val, f'{mean_val:.2f}s', 
               ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Linha de referência do baseline
    baseline_mean = df[df['estrategia'] == 'baseline']['tempo_s'].mean()
    ax.axhline(baseline_mean, color='gray', linestyle='--', 
               alpha=0.5, linewidth=1, label='Baseline médio')
    
    ax.set_ylabel('Tempo de Execução (segundos)', fontweight='bold')
    ax.set_xlabel('Estratégia de Teste', fontweight='bold')
    ax.set_title('Comparação de Tempo de Execução por Estratégia', 
                fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/tempo_profissional.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Gráfico salvo: {output_dir}/tempo_profissional.png")

def create_edp_plot(df, output_dir='data/plots'):
    """Gráfico de Energy-Delay Product (escala log)"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Boxplot
    bp = ax.boxplot(
        [df[df['estrategia'] == s]['edp'].values for s in ORDER],
        labels=[LABELS[s] for s in ORDER],
        patch_artist=True,
        widths=0.6,
        showmeans=True,
        meanprops=dict(marker='D', markerfacecolor='white', 
                      markeredgecolor='black', markersize=6)
    )
    
    # Colorir
    for patch, estrategia in zip(bp['boxes'], ORDER):
        patch.set_facecolor(COLORS[estrategia])
        patch.set_alpha(0.7)
    
    # Valores médios
    for i, estrategia in enumerate(ORDER, 1):
        mean_val = df[df['estrategia'] == estrategia]['edp'].mean()
        ax.text(i, mean_val, f'{mean_val:.1f}', 
               ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Escala logarítmica
    ax.set_yscale('log')
    
    ax.set_ylabel('Energy-Delay Product (J·s) [escala log]', fontweight='bold')
    ax.set_xlabel('Estratégia de Teste', fontweight='bold')
    ax.set_title('Comparação de Energy-Delay Product (EDP)', 
                fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--', which='both')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/edp_profissional.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Gráfico salvo: {output_dir}/edp_profissional.png")

def create_cpu_plot(df, output_dir='data/plots'):
    """Gráfico de Utilização de CPU"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bp = ax.boxplot(
        [df[df['estrategia'] == s]['cpu_pct'].values for s in ORDER],
        labels=[LABELS[s] for s in ORDER],
        patch_artist=True,
        widths=0.6,
        showmeans=True,
        meanprops=dict(marker='D', markerfacecolor='white', 
                      markeredgecolor='black', markersize=6)
    )
    
    for patch, estrategia in zip(bp['boxes'], ORDER):
        patch.set_facecolor(COLORS[estrategia])
        patch.set_alpha(0.7)
    
    for i, estrategia in enumerate(ORDER, 1):
        mean_val = df[df['estrategia'] == estrategia]['cpu_pct'].mean()
        ax.text(i, mean_val, f'{mean_val:.0f}%', 
               ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Linha de 100% (1 core)
    ax.axhline(100, color='orange', linestyle='--', 
               alpha=0.6, linewidth=1.5, label='1 core (100%)')
    
    ax.set_ylabel('Utilização de CPU (%)', fontweight='bold')
    ax.set_xlabel('Estratégia de Teste', fontweight='bold')
    ax.set_title('Comparação de Utilização de CPU', 
                fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/cpu_profissional.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Gráfico salvo: {output_dir}/cpu_profissional.png")

def create_comparison_bars(df, output_dir='data/plots'):
    """Gráfico de barras: Redução/Aumento vs Baseline"""
    baseline_tempo = df[df['estrategia'] == 'baseline']['tempo_s'].mean()
    baseline_energia = df[df['estrategia'] == 'baseline']['energia_estimada_j'].mean()
    baseline_edp = df[df['estrategia'] == 'baseline']['edp'].mean()
    
    estrategias = ['parallel', 'tia']
    labels_estrategias = ['Paralelo', 'TIA']
    
    # Calcular variações percentuais
    tempo_var = []
    energia_var = []
    edp_var = []
    
    for est in estrategias:
        subset = df[df['estrategia'] == est]
        tempo_var.append(((subset['tempo_s'].mean() - baseline_tempo) / baseline_tempo) * 100)
        energia_var.append(((subset['energia_estimada_j'].mean() - baseline_energia) / baseline_energia) * 100)
        edp_var.append(((subset['edp'].mean() - baseline_edp) / baseline_edp) * 100)
    
    # Criar gráfico
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Tempo
    bars1 = axes[0].bar(labels_estrategias, tempo_var, 
                        color=[COLORS['parallel'], COLORS['tia']], alpha=0.7)
    axes[0].axhline(0, color='black', linewidth=0.8)
    axes[0].set_ylabel('Variação vs Baseline (%)', fontweight='bold')
    axes[0].set_title('Tempo de Execução', fontweight='bold')
    axes[0].grid(axis='y', alpha=0.3)
    
    # Adicionar valores
    for bar, val in zip(bars1, tempo_var):
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:+.1f}%', ha='center', 
                    va='bottom' if val > 0 else 'top', fontweight='bold')
    
    # Energia
    bars2 = axes[1].bar(labels_estrategias, energia_var, 
                        color=[COLORS['parallel'], COLORS['tia']], alpha=0.7)
    axes[1].axhline(0, color='black', linewidth=0.8)
    axes[1].set_ylabel('Variação vs Baseline (%)', fontweight='bold')
    axes[1].set_title('Consumo de Energia', fontweight='bold')
    axes[1].grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars2, energia_var):
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:+.1f}%', ha='center', 
                    va='bottom' if val > 0 else 'top', fontweight='bold')
    
    # EDP
    bars3 = axes[2].bar(labels_estrategias, edp_var, 
                        color=[COLORS['parallel'], COLORS['tia']], alpha=0.7)
    axes[2].axhline(0, color='black', linewidth=0.8)
    axes[2].set_ylabel('Variação vs Baseline (%)', fontweight='bold')
    axes[2].set_title('Energy-Delay Product', fontweight='bold')
    axes[2].grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars3, edp_var):
        height = bar.get_height()
        axes[2].text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:+.0f}%', ha='center', 
                    va='bottom' if val > 0 else 'top', fontweight='bold')
    
    plt.suptitle('Variação Percentual em Relação ao Baseline', 
                fontweight='bold', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/comparacao_barras.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Gráfico salvo: {output_dir}/comparacao_barras.png")

def create_summary_table(df, output_dir='data/plots'):
    """Tabela resumo das métricas"""
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('tight')
    ax.axis('off')
    
    # Preparar dados
    data = []
    for estrategia in ORDER:
        subset = df[df['estrategia'] == estrategia]
        data.append([
            LABELS[estrategia].replace('\n', ' '),
            f"{subset['tempo_s'].mean():.3f} ± {subset['tempo_s'].std():.3f}",
            f"{subset['energia_estimada_j'].mean():.1f} ± {subset['energia_estimada_j'].std():.1f}",
            f"{subset['edp'].mean():.1f} ± {subset['edp'].std():.1f}",
            f"{subset['cpu_pct'].mean():.0f} ± {subset['cpu_pct'].std():.0f}",
            f"{subset['mem_max_mb'].mean():.1f} ± {subset['mem_max_mb'].std():.1f}"
        ])
    
    columns = ['Estratégia', 'Tempo (s)', 'Energia (J)', 'EDP (J·s)', 'CPU (%)', 'Memória (MB)']
    
    table = ax.table(cellText=data, colLabels=columns, 
                    cellLoc='center', loc='center',
                    colWidths=[0.2, 0.16, 0.16, 0.16, 0.16, 0.16])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Colorir cabeçalho
    for i in range(len(columns)):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Colorir linhas
    for i, estrategia in enumerate(ORDER, 1):
        table[(i, 0)].set_facecolor(COLORS[estrategia])
        table[(i, 0)].set_text_props(weight='bold', color='white')
        table[(i, 0)].set_alpha(0.7)
    
    plt.title('Resumo das Métricas Coletadas (n=10)', 
             fontweight='bold', fontsize=14, pad=20)
    plt.savefig(f'{output_dir}/tabela_resumo.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Tabela salva: {output_dir}/tabela_resumo.png")

def main():
    print("📊 Gerando Visualizações Profissionais...")
    print("")
    
    # Criar diretório de saída
    os.makedirs('data/plots', exist_ok=True)
    
    # Carregar dados
    df = load_data()
    print(f"✅ {len(df)} execuções carregadas")
    print("")
    
    # Gerar todos os gráficos
    create_tempo_plot(df)
    create_edp_plot(df)
    create_cpu_plot(df)
    create_comparison_bars(df)
    create_summary_table(df)
    
    print("")
    print("=" * 60)
    print("✅ Todas as visualizações foram geradas!")
    print("=" * 60)
    print("")
    print("📁 Arquivos criados em data/plots/:")
    print("   • tempo_profissional.png    - Figura principal (tempo)")
    print("   • edp_profissional.png      - Figura principal (EDP)")
    print("   • cpu_profissional.png      - Figura suplementar")
    print("   • comparacao_barras.png     - Análise comparativa")
    print("   • tabela_resumo.png         - Tabela para artigo")
    print("")
    print("🎨 Use estas figuras no artigo!")

if __name__ == "__main__":
    main()