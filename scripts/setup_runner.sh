#!/bin/bash
# Script de preparação do ambiente do self-hosted runner
# Execute este script UMA VEZ antes de iniciar os experimentos

set -e  # Para em caso de erro

echo "============================================================"
echo "🔧 Preparação do Ambiente - Green Metrics CI"
echo "============================================================"
echo ""

# Função para perguntar sim/não
ask_yes_no() {
    while true; do
        read -p "$1 (s/n): " yn
        case $yn in
            [Ss]* ) return 0;;
            [Nn]* ) return 1;;
            * ) echo "Por favor, responda s ou n.";;
        esac
    done
}

# 1. Verificar se é Linux
echo "📋 Verificando sistema operacional..."
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Erro: Este script é apenas para Linux"
    exit 1
fi
echo "✅ Sistema: Linux"
echo ""

# 2. Verificar se tem permissões de sudo
echo "🔐 Verificando permissões sudo..."
if ! sudo -v; then
    echo "❌ Erro: Este script precisa de permissões sudo"
    exit 1
fi
echo "✅ Permissões OK"
echo ""

# 3. Instalar dependências do sistema
if ask_yes_no "📦 Deseja instalar dependências do sistema (lm-sensors, cpufrequtils)?"; then
    echo "⏳ Instalando dependências..."
    sudo apt-get update -qq
    sudo apt-get install -y lm-sensors cpufrequtils python3-venv python3-pip
    echo "✅ Dependências instaladas"
else
    echo "⏭️  Pulando instalação de dependências"
fi
echo ""

# 4. Configurar CPU Governor
if ask_yes_no "⚡ Deseja configurar CPU para modo 'performance'?"; then
    echo "⏳ Configurando CPU governor..."
    echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null
    echo "✅ CPU configurada para performance"
else
    echo "⏭️  Mantendo configuração atual da CPU"
fi
echo ""

# 5. Verificar temperatura da CPU (se lm-sensors instalado)
if command -v sensors &> /dev/null; then
    echo "🌡️  Temperatura atual da CPU:"
    sensors 2>/dev/null | grep "Core" || echo "   (Não foi possível ler temperatura)"
else
    echo "⚠️  lm-sensors não instalado, não é possível verificar temperatura"
fi
echo ""

# 6. Limpar cache
if ask_yes_no "🧹 Deseja limpar caches?"; then
    echo "⏳ Limpando caches..."
    pip cache purge 2>/dev/null || true
    rm -rf ~/.cache/pytest 2>/dev/null || true
    rm -f .testmondata* 2>/dev/null || true
    echo "✅ Caches limpos"
else
    echo "⏭️  Mantendo caches"
fi
echo ""

# 7. Verificar GitHub CLI
echo "🔍 Verificando GitHub CLI (gh)..."
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI já instalado: $(gh --version | head -n1)"
else
    if ask_yes_no "⚠️  GitHub CLI não encontrado. Deseja instalar?"; then
        echo "⏳ Instalando GitHub CLI..."
        type -p curl >/dev/null || sudo apt install curl -y
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg 2>/dev/null
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
        sudo apt update -qq
        sudo apt install gh -y
        echo "✅ GitHub CLI instalado"
    else
        echo "⚠️  ATENÇÃO: Você precisará do GitHub CLI para rodar o experimento!"
    fi
fi
echo ""

# 8. Autenticar GitHub CLI
if command -v gh &> /dev/null; then
    echo "🔐 Verificando autenticação do GitHub CLI..."
    if gh auth status &> /dev/null; then
        echo "✅ GitHub CLI já autenticado"
    else
        if ask_yes_no "⚠️  GitHub CLI não autenticado. Deseja autenticar agora?"; then
            gh auth login
        else
            echo "⚠️  ATENÇÃO: Você precisará autenticar antes de rodar o experimento!"
            echo "   Execute: gh auth login"
        fi
    fi
fi
echo ""

# 9. Informações do sistema
echo "============================================================"
echo "📊 Informações do Sistema"
echo "============================================================"
echo "CPU:    $(lscpu | grep 'Model name' | cut -d':' -f2 | xargs)"
echo "Cores:  $(nproc) núcleos"
echo "RAM:    $(free -h | awk '/^Mem:/ {print $2}')"
echo "OS:     $(lsb_release -d 2>/dev/null | cut -f2 || echo 'Desconhecido')"
echo "Python: $(python3 --version 2>/dev/null || echo 'Não encontrado')"
echo ""
echo "============================================================"
echo "✅ Setup Concluído!"
echo "============================================================"
echo ""
echo "📍 Próximos passos:"
echo "   1. cd $(pwd)"
echo "   2. touch src/__init__.py"
echo "   3. python3 -m venv venv"
echo "   4. source venv/bin/activate"
echo "   5. pip install -r requirements.txt"
echo "   6. python3 scripts/orchestrator.py"
echo ""