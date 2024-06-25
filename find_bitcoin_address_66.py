import random
import threading
from bit import Key
from concurrent.futures import ThreadPoolExecutor

# Define o intervalo de chaves privadas
PRIVATE_KEY_START = int("20000000000000000", 16)
PRIVATE_KEY_END = int("3ffffffffffffffff", 16)

# Endereço Bitcoin alvo
TARGET_ADDRESS = "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"

# Variável compartilhada para contar chaves testadas
keys_tested = 0
lock = threading.Lock()  # Lock para sincronização

# Função para converter chave privada para endereço Bitcoin e verificar
def check_key(private_key_int):
    global keys_tested
    # Converte o inteiro da chave privada para hexadecimal
    private_key_hex = format(private_key_int, 'x')
    
    # Gera a chave a partir do hexadecimal
    key = Key.from_hex(private_key_hex)
    
    # Converte para endereço Bitcoin
    address = key.address
    
    # Atualiza o contador de chaves testadas
    with lock:
        keys_tested += 1
        formatted_count = "{:,}".format(keys_tested).replace(",", ".")
        print(f"Chaves testadas: {formatted_count}", end='\r')
    
    # Verifica se é o endereço alvo
    if address == TARGET_ADDRESS:
        # Exibe a chave privada em WIF
        print(f"\nChave encontrada! WIF: {key.to_wif()}")
        return True
    return False

# Função para gerar e verificar chaves privadas aleatórias
def random_key_check():
    while True:
        # Gera um inteiro aleatório dentro do intervalo
        private_key_int = random.randint(PRIVATE_KEY_START, PRIVATE_KEY_END)
        if check_key(private_key_int):
            break

# Função principal para criar múltiplos threads
def main():
    # Número de threads
    num_threads = 4
    
    # Cria um ThreadPoolExecutor com o número especificado de threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(random_key_check) for _ in range(num_threads)]
        
        # Espera que todos os futuros completem (embora tecnicamente, apenas um futuro precisa encontrar o endereço)
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
