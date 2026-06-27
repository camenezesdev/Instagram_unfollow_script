[!["Language: PT-BR/EN"](https://img.shields.io/badge/Language-PT--BR%20%2F%20EN-blue.svg)](#)
[!["Language: Python"](https://img.shields.io/badge/Language-Python-yellow.svg)](#)
[!["License: MIT"](https://img.shields.io/badge/License-MIT-green.svg)](#)

Instagram Unfollow Bot & Automation Suite
Este repositório contém a documentação completa e os scripts operacionais utilizados para gerenciar e mitigar a lista de seguintes do Instagram de forma automatizada e segura em um ambiente controlado. O objetivo desta ferramenta é demonstrar como o uso de engenharia reversa de interface via automação visual (Selenium) pode contornar os rigorosos bloqueios de sessão de firewalls de aplicação web (WAF), mimetizando com precisão o comportamento orgânico de um operador humano para evitar a sinalização da conta.

This repository contains the full documentation and operational scripts used to automatically and safely manage and clean up an Instagram following list within a controlled environment. The goal of this tool is to demonstrate how interface reverse-engineering via visual automation (Selenium) can bypass strict web application firewall (WAF) session locks, precisely mimicking organic human behavior to avoid account flagging.

Explicações e Features / Workflow do Script
Arquitetura Híbrida de Emulação Visual (Selenium): Abordagem que substitui pedidos diretos de API por interações gráficas reais num browser legítimo, eliminando por completo os erros críticos de Login required provocados pelas firewalls e WAFs do Instagram.

[+] Sistema de Rondas Consecutivas e Interativas: Permite ao utilizador definir múltiplos blocos de remoção na mesma sessão através do terminal, reiniciando o mapeamento do popup de forma dinâmica sem necessidade de reiniciar o programa.

[+] Gestão Autónoma de Whitelist: Salvaguarda perfis protegidos através de um ficheiro local (whitelist.txt), cruzando os dados em tempo real e ignorando automaticamente contas críticas antes de qualquer interação de escrita.

[+] Delays Humanos Dinâmicos e Aleatórios: Implementação de temporizadores adaptativos entre ações (ex: 15 a 35 segundos) para quebrar padrões mecânicos de automação.

[+] Mitigação Global Anti-WAF por Lotes: Ativação automática de pausas prolongadas (5 minutos) a cada bloco acumulado de 30 ações, mimetizando a exaustão biológica de um utilizador real para proteger a reputação e integridade da conta.

[+] Resiliência a Falhas e Crashes (Session Catching): Tratamento robusto de exceções estruturais (como InvalidSessionIdException), garantindo que o fecho inesperado do browser ou quedas de sessão não corrompam o terminal ou a stack do utilizador.

Plaintext
## Estrutura do Repositório / Repository Structure

```text
Unfollow_Script
├── .venv/                  # Ambiente virtual do Python / Python Virtual Environment
├── whitelist.txt           # Lista de contas protegidas contra o unfollow / Protected accounts list
├── unfollow_script2.py     # Script principal de automação / Main automation script
└── README.md               # Documentação técnica do projeto / Technical documentation
````

Como Executar o Laboratório / Quick Start Guide
Para executar o script de automação, certifique-se de cumprir os pré-requisitos básicos, que incluem ter o Python 3.10 ou superior instalado no host e o navegador Google Chrome atualizado. Na etapa de instalação, navegue até a pasta do projeto e configure o ambiente instalando a dependência do Selenium executando o comando pip install selenium no terminal do seu ambiente virtual. Para a configuração da whitelist, crie o arquivo whitelist.txt na raiz do diretório e adicione um nome de usuário por linha, omitindo o caractere @. Com a estrutura pronta, inicie a execução com o comando python unfollow_script2.py. O terminal interativo solicitará que insira o seu utilizador e estabeleça o limite de remoções desejado; a instância dedicada do Chrome será aberta de seguida para que faça o login manualmente e, assim que visualizar o feed principal da rede, basta pressionar [ENTER] no terminal para que o bot assuma o fluxo autônomo.

To run this automation script, ensure you meet the prerequisites, which include having Python 3.10 or higher installed on the host and an up-to-date version of Google Chrome. For the installation phase, navigate to your project directory and configure the workspace by installing the Selenium dependency running pip install selenium within your virtual environment. For the whitelist configuration, create a file named whitelist.txt in the root directory and add one username per line, ensuring you omit the @ symbol. To begin execution, launch the script using the command python unfollow_script2.py. The interactive terminal will prompt you to enter your username and specify the session limit; a dedicated Chrome instance will then open for you to log in manually, and once you reach the main feed, simply press the [ENTER] key in your terminal to start the autonomous flow.

Megabytez CyberSec Labs
Este projeto faz parte do meu ecossistema de segurança e portefólio profissional. Para consultar o meu currículo, visite o meu domínio oficial:

This project is part of my secure ecosystem and professional portfolio. To check my CV, please visit my official domain:

🔗 megabytez.pt

Developed by Carlos Alexandre Menezes | Version 1.0 | Confidentiality: Academic & Educational Use only.
