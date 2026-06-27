import os
import time
import random
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, InvalidSessionIdException

# Inicialização do suporte a cores ANSI no terminal do Windows
os.system('')


class Cores:
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    CIANO = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def carregar_whitelist(nome_arquivo="whitelist.txt"):
    whitelist = set()
    if not os.path.exists(nome_arquivo):
        return whitelist
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                linha_limpa = linha.strip().lower()
                if not linha_limpa or linha_limpa.startswith("#") or "source:" in linha_limpa:
                    continue
                whitelist.add(linha_limpa)
        print(f"{Cores.VERDE}[+] Whitelist carregada: {len(whitelist)} contas protegidas.{Cores.RESET}")
    except Exception as e:
        print(f"{Cores.VERMELHO}[-] Erro na whitelist: {e}{Cores.RESET}")
    return whitelist


def obter_limite_valido(prompt):
    while True:
        try:
            limite = int(input(prompt))
            if limite > 0:
                return limite
        except ValueError:
            print(f"{Cores.VERMELHO}[-] Entrada inválida. Introduza um número inteiro.{Cores.RESET}")


def contagem_decrescente(segundos):
    for i in range(segundos, 0, -1):
        minutos = i // 60
        seg = i % 60
        sys.stdout.write(
            f"{Cores.AMARELO}[*]{Cores.RESET} Pausa de mitigação: {Cores.BOLD}{minutos:02d}:{seg:02d}{Cores.RESET}...")
        sys.stdout.flush()
        time.sleep(1)
        sys.stdout.write('\r')
    print(f"\n{Cores.VERDE}[+]{Cores.RESET} Pausa concluída!")


def executar_limpeza_hibrida():
    print(f"{Cores.BOLD}{Cores.CIANO}=== INSTAGRAM UNFOLLOW BOT (MULTI-ROUND ARCHITECTURE) ==={Cores.RESET}")

    LISTA_BRANCA = carregar_whitelist()
    username = input("Introduza o seu utilizador do Instagram: ").strip().lower()

    print(f"\n{Cores.CIANO}[*]{Cores.RESET} A abrir instância do Google Chrome...")
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--start-maximized")
    opcoes.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=opcoes)
    wait = WebDriverWait(driver, 15)

    BLACKLIST_SISTEMA = {
        "about", "meta", "blog", "jobs", "help", "api", "privacy", "terms", "locations",
        "instagram lite", "threads", "contact uploading & non-users", "meta verified",
        "edit profile", "view archive", "posts", "followers", "following", "home", "search",
        "explore", "reels", "messages", "notifications", "create", "profile", "log in", "sign up"
    }

    try:
        driver.get("https://www.instagram.com/")
        print(f"{Cores.AMARELO}[!] Intervenção Necessária: Faz login na tua conta no browser aberto.{Cores.RESET}")
        input(f"{Cores.BOLD}[?]{Cores.RESET} Quando estiveres logado e vires o feed principal, prime [ENTER] aqui...")

        executar_rondas = True
        total_geral_unfollows = 0
        contagem_lote = 0
        delay_min, delay_max = 15, 35

        while executar_rondas:
            print(f"\n{Cores.BOLD}{Cores.CIANO}--- NOVA RONDA DE UNFOLLOWS ---{Cores.RESET}")
            limite_ronda = obter_limite_valido(
                f"{Cores.CIANO}[*]{Cores.RESET} Quantos unfollows queres realizar nesta ronda? ")

            print(f"{Cores.CIANO}[*]{Cores.RESET} A navegar até ao teu perfil para atualizar mapeamento...")
            driver.get(f"https://www.instagram.com/{username}/")
            time.sleep(5)

            print(f"{Cores.CIANO}[*]{Cores.RESET} A abrir a janela popup 'A seguir'...")
            try:
                link_modal = wait.until(EC.element_to_be_clickable((
                    By.XPATH,
                    "//a[contains(text(), 'following') or contains(text(), 'seguindo') or contains(., 'following')]"
                )))
                driver.execute_script("arguments[0].click();", link_modal)
            except Exception:
                link_modal = wait.until(EC.element_to_be_clickable((
                    By.XPATH,
                    "//*[contains(text(), 'following') or contains(text(), 'seguindo') or contains(text(), 'a seguir')]/ancestor::a"
                )))
                driver.execute_script("arguments[0].click();", link_modal)

            time.sleep(4)

            contas_a_seguir = []
            processados = set()

            print(f"{Cores.CIANO}[*]{Cores.RESET} A mapear alvos a partir do popup ativo...")
            for i in range(5):
                try:
                    elementos_link = driver.find_elements(By.XPATH,
                                                          "//div[@role='dialog']//a[contains(@href, '/') and @role='link']")
                    if not elementos_link:
                        elementos_link = driver.find_elements(By.XPATH,
                                                              "//div[@role='dialog']//a[contains(@href, '/')]")

                    for elem in elementos_link:
                        try:
                            target_user = elem.text.strip().lower()
                            if target_user and target_user != username and len(
                                    target_user) > 2 and '\n' not in target_user:
                                if target_user in BLACKLIST_SISTEMA or any(
                                        term in target_user for term in ["edit", "archive", "profile"]):
                                    continue
                                if target_user not in processados:
                                    processados.add(target_user)
                                    contas_a_seguir.append(target_user)
                        except:
                            continue

                    if elementos_link:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elementos_link[-1])
                        time.sleep(2.5)
                except (InvalidSessionIdException, WebDriverException):
                    print(f"\n{Cores.VERMELHO}[-]{Cores.RESET} Conexão com o browser perdida durante o mapeamento.")
                    return

            total_mapeado = len(contas_a_seguir)
            if total_mapeado == 0:
                print(
                    f"{Cores.VERMELHO}[-]{Cores.RESET} Não foi possível extrair a lista. Tenta iniciar uma nova ronda.")
                continue

            print(f"{Cores.VERDE}[+]{Cores.RESET} Mapeamento concluído! {total_mapeado} contas em fila.")

            unfollows_ronda_feitos = 0

            for target_username in contas_a_seguir:
                if unfollows_ronda_feitos >= limite_ronda:
                    break

                if target_username in LISTA_BRANCA:
                    print(f"{Cores.AMARELO}[#] [PROTEGIDO]{Cores.RESET} {target_username} ignorado devido à Whitelist.")
                    continue

                print(
                    f"\n{Cores.CIANO}[*]{Cores.RESET} [{unfollows_ronda_feitos + 1}/{limite_ronda}] (Total sessão: {total_geral_unfollows + 1}). A abrir: {Cores.BOLD}{target_username}{Cores.RESET}")

                # CATCH CRÍTICO: Evita a quebra do programa se o browser fechar ou crashar a meio da ronda
                try:
                    driver.get(f"https://www.instagram.com/{target_username}/")
                except (InvalidSessionIdException, WebDriverException):
                    print(
                        f"\n{Cores.VERMELHO}[-]{Cores.RESET} Erro: O browser foi fechado ou a sessão crashou inesperadamente.")
                    print(
                        f"{Cores.AMARELO}[*]{Cores.RESET} Execução interrompida. Total de ações guardadas nesta sessão: {total_geral_unfollows}")
                    return

                time.sleep(random.uniform(4, 6))

                try:
                    botao = wait.until(EC.element_to_be_clickable((
                        By.XPATH,
                        "//button[contains(., 'A seguir') or contains(., 'Following') or contains(., 'Requested') or @aria-label='A seguir']"
                    )))
                    driver.execute_script("arguments[0].click();", botao)
                    time.sleep(random.uniform(2.0, 3.0))

                    try:
                        botao_confirmar = wait.until(EC.element_to_be_clickable((
                            By.XPATH,
                            "//span[text()='Unfollow' or text()='Deixar de seguir'] | //button[text()='Unfollow' or text()='Deixar de seguir' or contains(., 'Unfollow') or contains(., 'Deixar de seguir')]"
                        )))
                        driver.execute_script("arguments[0].click();", botao_confirmar)
                    except Exception:
                        botao_confirmar = wait.until(EC.element_to_be_clickable((
                            By.XPATH, "//div[@role='dialog']//button[last()]"
                        )))
                        driver.execute_script("arguments[0].click();", botao_confirmar)

                    unfollows_ronda_feitos += 1
                    total_geral_unfollows += 1
                    contagem_lote += 1
                    print(f"{Cores.VERDE}[+]{Cores.RESET} Sucesso! Deixaste de seguir {target_username}.")

                    if unfollows_ronda_feitos < limite_ronda:
                        tempo_entre = random.randint(delay_min, delay_max)
                        print(f"{Cores.CIANO}[*]{Cores.RESET} Aguardando {tempo_entre}s...")
                        time.sleep(tempo_entre)

                    if contagem_lote == 30:
                        tempo_lote = 300 + random.randint(10, 90)
                        print(
                            f"\n{Cores.AMARELO}[!] Bloco global de 30 atingido. Ativando pausa de {tempo_lote}s...{Cores.RESET}")
                        contagem_decrescente(tempo_lote)
                        contagem_lote = 0

                except Exception:
                    print(
                        f"{Cores.AMARELO}[!] Elemento indisponível no perfil de {target_username}. Passando...{Cores.RESET}")
                    continue

            print(
                f"\n{Cores.VERDE}[+]{Cores.RESET} Ronda terminada! Concluídos {unfollows_ronda_feitos} unfollows nesta volta.")

            try:
                resposta = input(
                    f"\n{Cores.BOLD}{Cores.AMARELO}[?]{Cores.RESET} Desejas iniciar uma nova ronda de unfollows? (s/N): ").strip().lower()
                if resposta != 's':
                    executar_rondas = False
            except (KeyboardInterrupt, EOFError):
                executar_rondas = False

        print(
            f"\n{Cores.VERDE}{Cores.BOLD}[+] Processo encerrado pelo utilizador! Total global realizado nesta sessão: {total_geral_unfollows}{Cores.RESET}")

    except Exception as e:
        print(f"{Cores.VERMELHO}[-]{Cores.RESET} Erro crítico inesperado: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass


if __name__ == "__main__":
    executar_limpeza_hibrida()
