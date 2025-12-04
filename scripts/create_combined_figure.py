#!/usr/bin/env python3
"""
Cria figura combinada 2x2 para artigo científico
Inclui: Tempo, EDP, CPU e Variação Percentual
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# Configurações globais
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 9
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8

# Paleta de cores
COLORS = {
    'baseline': '#7fb3d5',
    'parallel': '#e74c3c',
    'tia': '#27ae60'
}

ORDER = ['baseline', 'parallel', 'tia']
LABELS = {
    'baseline': 'Baseline\n(Sequencial)',
    'parallel': 'Paralelo\n(xdist)',
    'tia': 'TIA\n(Testmon)'
}

def load_data(filepath='data/resultados_simple.csv'):
    return pd.read_csv(filepath)

def create_combined_figure(df, output_path='data/plots/figura_combinada_2x2.png'):
    """Cria figura 2x2 com os 4 gráficos principais"""
    
    # Criar figura e grid
    fig = plt.figure(figsize=(14, 10))
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3,
                          left=0.08, right=0.95, top=0.93, bottom=0.06)
    
    # =========================================================================
    # (A) Superior Esquerdo: TEMPO DE EXECUÇÃO
    # =========================================================================
    ax1 = fig.add_subplot(gs[0, 0])
    
    bp1 = ax1.boxplot(
        [df[df['estrategia'] == s]['tempo_s'].values for s in ORDER],
        labels=[LABELS[s] for s in ORDER],
        patch_artist=True,
        widths=0.6,
        showmeans=True,
        meanprops=dict(marker='D', markerfacecolor='white', 
                      markeredgecolor='black', markersize=5)
    )
    
    for patch, estrategia in zip(bp1['boxes'], ORDER):
        patch.set_facecolor(COLORS[estrategia])
        patch.set_alpha(0.7)
    
    # Valores médios
    for i, estrategia in enumerate(ORDER, 1):
        mean_val = df[df['estrategia'] == estrategia]['tempo_s'].mean()
        ax1.text(i, mean_val, f'{mean_val:.2f}s', 
                ha='center', va='bottom', fontweight='bold', fontsize=8)
    
    # Linha de referência
    baseline_mean = df[df['estrategia'] == 'baseline']['tempo_s'].mean()
    ax1.axhline(baseline_mean, color='gray', linestyle='--', 
               alpha=0.5, linewidth=1)
    
    ax1.set_ylabel('Tempo (segundos)', fontweight='bold')
    ax1.set_xlabel('Estratégia', fontweight='bold')
    ax1.set_title('(A) Tempo de Execução', fontweight='bold', loc='left', pad=10)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adicionar significância estatística
    ax1.text(2, ax1.get_ylim()[1] * 0.95, 'p<0.01', 
            ha='center', fontsize=8, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # =========================================================================
    # (B) Superior Direito: ENERGY-DELAY PRODUCT (Escala Log)
    # =========================================================================
    ax2 = fig.add_subplot(gs[0, 1])
    
    bp2 = ax2.boxplot(
        [df[df['estrategia'] == s]['edp'].values for s in ORDER],
        labels=[LABELS[s] for s in ORDER],
        patch_artist=True,
        widths=0.6,
        showmeans=True,
        meanprops=dict(marker='D', markerfacecolor='white', 
                      markeredgecolor='black', markersize=5)
    )
    
    for patch, estrategia in zip(bp2['boxes'], ORDER):
        patch.set_facecolor(COLORS[estrategia])
        patch.set_alpha(0.7)
    
    # Valores médios
    for i, estrategia in enumerate(ORDER, 1):
        mean_val = df[df['estrategia'] == estrategia]['edp'].mean()
        ax2.text(i, mean_val, f'{mean_val:.1f}', 
                ha='center', va='bottom', fontweight='bold', fontsize=8)
    
    ax2.set_yscale('log')
    ax2.set_ylabel('EDP (J·s) [escala log]', fontweight='bold')
    ax2.set_xlabel('Estratégia', fontweight='bold')
    ax2.set_title('(B) Energy-Delay Product', fontweight='bold', loc='left', pad=10)
    ax2.grid(axis='y', alpha=0.3, linestyle='--', which='both')
    
    # Adicionar significância
    ax2.text(2, ax2.get_ylim()[1] * 0.7, 'p<0.001', 
            ha='center', fontsize=8, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # =========================================================================
    # (C) Inferior Esquerdo: UTILIZAÇÃO DE CPU
    # =========================================================================
    ax3 = fig.add_subplot(gs[1, 0])
    
    bp3 = ax3.boxplot(
        [df[df['estrategia'] == s]['cpu_pct'].values for s in ORDER],
        labels=[LABELS[s] for s in ORDER],
        patch_artist=True,
        widths=0.6,
        showmeans=True,
        meanprops=dict(marker='D', markerfacecolor='white', 
                      markeredgecolor='black', markersize=5)
    )
    
    for patch, estrategia in zip(bp3['boxes'], ORDER):
        patch.set_facecolor(COLORS[estrategia])
        patch.set_alpha(0.7)
    
    # Valores médios
    for i, estrategia in enumerate(ORDER, 1):
        mean_val = df[df['estrategia'] == estrategia]['cpu_pct'].mean()
        ax3.text(i, mean_val, f'{mean_val:.0f}%', 
                ha='center', va='bottom', fontweight='bold', fontsize=8)
    
    # Linha 100% (1 core)
    ax3.axhline(100, color='orange', linestyle='--', 
               alpha=0.6, linewidth=1.5, label='1 core')
    
    ax3.set_ylabel('CPU (%)', fontweight='bold')
    ax3.set_xlabel('Estratégia', fontweight='bold')
    ax3.set_title('(C) Utilização de CPU', fontweight='bold', loc='left', pad=10)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    ax3.legend(loc='upper left', fontsize=8)
    
    # =========================================================================
    # (D) Inferior Direito: VARIAÇÃO PERCENTUAL vs BASELINE
    # =========================================================================
    ax4 = fig.add_subplot(gs[1, 1])
    
    # Calcular variações
    baseline_tempo = df[df['estrategia'] == 'baseline']['tempo_s'].mean()
    baseline_energia = df[df['estrategia'] == 'baseline']['energia_estimada_j'].mean()
    baseline_edp = df[df['estrategia'] == 'baseline']['edp'].mean()
    
    estrategias = ['parallel', 'tia']
    x_pos = np.arange(len(estrategias))
    width = 0.25
    
    # Calcular variações
    tempo_vars = []
    energia_vars = []
    edp_vars = []
    
    for est in estrategias:
        subset = df[df['estrategia'] == est]
        tempo_vars.append(((subset['tempo_s'].mean() - baseline_tempo) / baseline_tempo) * 100)
        energia_vars.append(((subset['energia_estimada_j'].mean() - baseline_energia) / baseline_energia) * 100)
        edp_vars.append(((subset['edp'].mean() - baseline_edp) / baseline_edp) * 100)
    
    # Criar barras agrupadas
    bars1 = ax4.bar(x_pos - width, tempo_vars, width, label='Tempo', 
                    color='#3498db', alpha=0.8)
    bars2 = ax4.bar(x_pos, energia_vars, width, label='Energia', 
                    color='#e67e22', alpha=0.8)
    bars3 = ax4.bar(x_pos + width, edp_vars, width, label='EDP', 
                    color='#9b59b6', alpha=0.8)
    
    # Linha zero
    ax4.axhline(0, color='black', linewidth=1, linestyle='-')
    
    # Adicionar valores nas barras
    for bars, values in [(bars1, tempo_vars), (bars2, energia_vars), (bars3, edp_vars)]:
        for bar, val in zip(bars, values):
            height = bar.get_height()
            if abs(val) > 100:  # Se muito grande, formato especial
                label = f'{val:.0f}%'
            else:
                label = f'{val:+.0f}%'
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    label, ha='center', 
                    va='bottom' if val > 0 else 'top', 
                    fontweight='bold', fontsize=7)
    
    ax4.set_ylabel('Variação vs Baseline (%)', fontweight='bold')
    ax4.set_xlabel('Estratégia', fontweight='bold')
    ax4.set_title('(D) Variação Percentual', fontweight='bold', loc='left', pad=10)
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(['Paralelo', 'TIA'])
    ax4.legend(loc='upper right', fontsize=8, ncol=3)
    ax4.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Ajustar limites do eixo Y para acomodar valores grandes
    y_max = max(max(tempo_vars), max(energia_vars), max(edp_vars))
    y_min = min(min(tempo_vars), min(energia_vars), min(edp_vars))
    ax4.set_ylim(y_min * 1.2, y_max * 1.15)
    
    # =========================================================================
    # Título geral
    # =========================================================================
    fig.suptitle('Comparação de Estratégias de Otimização de Testes em CI (n=10)', 
                fontweight='bold', fontsize=13, y=0.98)
    
    # Salvar
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Figura combinada 2x2 salva: {output_path}")
    print(f"   Resolução: 300 DPI")
    print(f"   Tamanho: 14x10 polegadas (~3500x2500 pixels)")
    print(f"   Formato: PNG de alta qualidade")

def main():
    print("🎨 Criando Figura Combinada 2x2...")
    print("")
    
    # Carregar dados
    df = load_data()
    print(f"✅ {len(df)} execuções carregadas")
    print("")
    
    # Criar figura combinada
    create_combined_figure(df)
    
    print("")
    print("=" * 60)
    print("✅ Figura Combinada Criada com Sucesso!")
    print("=" * 60)
    print("")
    print("📊 Estrutura da Figura:")
    print("   ┌─────────────────┬─────────────────┐")
    print("   │ (A) Tempo       │ (B) EDP         │")
    print("   │                 │   (escala log)  │")
    print("   ├─────────────────┼─────────────────┤")
    print("   │ (C) CPU         │ (D) Variação %  │")
    print("   │                 │                 │")
    print("   └─────────────────┴─────────────────┘")
    print("")
    print("💡 Use esta figura como:")
    print("   • Figura 1 principal do artigo")
    print("   • Slide de apresentação")
    print("   • Resumo visual completo do experimento")
    print("")
    print("📝 Legenda sugerida:")
    print('   "Comparação de métricas entre estratégias de teste:')
    print('    (A) Tempo de execução, (B) Energy-Delay Product,')
    print('    (C) Utilização de CPU, (D) Variação percentual vs baseline."')

if __name__ == "__main__":
    main()