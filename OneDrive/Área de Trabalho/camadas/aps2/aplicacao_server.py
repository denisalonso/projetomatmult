#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Projeto 2 - Servidor (Nota A+)
# Conversão manual IEEE-754 32 bits - SEM HEADER
#####################################################

import time
from enlace import *

def ieee_para_float_manual(bytes_data):
    """
    Converte 4 bytes IEEE-754 para float manualmente - NOTA A+
    Retorna o número float reconstruído
    """
    if len(bytes_data) != 4:
        raise ValueError("Precisa de exatamente 4 bytes")
    
    # 1. Extrair os 32 bits dos 4 bytes
    byte1, byte2, byte3, byte4 = bytes_data
    ieee_32bits = (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | byte4
    
    # 2. Extrair sinal (bit mais significativo - bit 31)
    sinal = (ieee_32bits >> 31) & 0x1
    
    # 3. Extrair expoente (bits 30-23)
    expoente_bias = (ieee_32bits >> 23) & 0xFF
    
    # 4. Extrair mantissa (bits 22-0)
    mantissa = ieee_32bits & 0x7FFFFF
    
    # 5. Casos especiais
    if expoente_bias == 0:
        # Zero ou número subnormal
        if mantissa == 0:
            return 0.0 if sinal == 0 else -0.0
        else:
            # Número subnormal (não implementado completamente)
            return 0.0
    
    if expoente_bias == 255:
        # Infinito ou NaN
        if mantissa == 0:
            return float('inf') if sinal == 0 else float('-inf')
        else:
            return float('nan')
    
    # 6. Calcular expoente real (remover bias de 127)
    expoente = expoente_bias - 127
    
    # 7. Calcular valor da mantissa (com bit implícito 1)
    valor_mantissa = 1.0  # Bit implícito sempre 1 para números normais
    bit_valor = 0.5  # Valor do primeiro bit da mantissa (2^-1)
    
    # Percorre os 23 bits da mantissa
    for i in range(23):
        if mantissa & (1 << (22 - i)):  # Verifica se o bit está setado
            valor_mantissa += bit_valor
        bit_valor /= 2.0  # Próximo bit vale metade
    
    # 8. Calcular valor final = mantissa × 2^expoente
    valor = valor_mantissa * (2.0 ** expoente)
    
    # 9. Aplicar sinal
    if sinal == 1:
        valor = -valor
    
    return valor

def float_para_ieee_manual(numero):
    """
    Converte float para 4 bytes IEEE-754 manualmente - NOTA A+
    Retorna 4 bytes no formato IEEE-754
    """
    # 1. Determinar sinal
    if numero >= 0:
        sinal = 0
    else:
        sinal = 1
        numero = -numero
    
    # 2. Casos especiais
    if numero == 0:
        return bytes([0, 0, 0, 0])
    
    # 3. Converter para notação científica binária
    expoente = 0
    
    # Normalizar para obter número entre 1.0 e 2.0
    if numero >= 2.0:
        while numero >= 2.0:
            numero /= 2.0
            expoente += 1
    elif numero < 1.0:
        while numero < 1.0:
            numero *= 2.0
            expoente -= 1
    
    # 4. Remover o 1 implícito e calcular mantissa
    numero -= 1.0  # Agora numero está entre 0.0 and 1.0
    mantissa = 0
    bit_valor = 0.5  # Valor do primeiro bit da mantissa
    
    # Converter a parte fracionária para binário (23 bits)
    for i in range(23):
        if numero >= bit_valor:
            mantissa |= (1 << (22 - i))  # Setar o bit correspondente
            numero -= bit_valor
        bit_valor /= 2.0
    
    # 5. Calcular expoente com bias de 127
    expoente_bias = expoente + 127
    
    # 6. Montar os 32 bits do IEEE-754
    ieee_32bits = (sinal << 31) | (expoente_bias << 23) | mantissa
    
    # 7. Converter para 4 bytes
    byte1 = (ieee_32bits >> 24) & 0xFF
    byte2 = (ieee_32bits >> 16) & 0xFF
    byte3 = (ieee_32bits >> 8) & 0xFF
    byte4 = ieee_32bits & 0xFF
    
    return bytes([byte1, byte2, byte3, byte4])

def main():
    try:
        # Configuração da porta serial
        serialName = "COM9"  # AJUSTAR PARA SUA PORTA
        com1 = enlace(serialName)
        
        # Inicializa comunicação
        com1.enable()
        print("Servidor inicializado - Nota A+")
        print(f"Porta: {serialName}")
        print("Aguardando comunicação...")
        
        # Byte de sacrifício
        print("\nesperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(0.1)
        print("Byte de sacrifício recebido e descartado")
        
        while True:
            print("\nAguardando números (sem cabeçalho, só floats32)...")

            # 1) Drenar bytes até "silêncio" (nenhum novo byte por 1.0 s)
            buf = bytearray()
            ultimo = time.time()
            SILENCIO = 1.0  # ajuste se precisar

            while True:
                if com1.rx.getBufferLen() > 0:
                    chunk = com1.rx.getAllBuffer(0)  # drena tudo disponível
                    buf.extend(chunk)
                    ultimo = time.time()
                    print(f"Recebidos {len(chunk)} bytes, buffer total: {len(buf)} bytes")
                else:
                    if time.time() - ultimo > SILENCIO:
                        break
                    time.sleep(0.01)

            # 2) Validar múltiplo de 4
            if len(buf) == 0:
                print('finalizando aplicacao')
                # print("[SRV] nenhum byte recebido (silêncio). Continuando...")
                # continue
                break

            if (len(buf) % 4) != 0:
                print(f"[SRV][ERRO] {len(buf)} bytes recebidos não é múltiplo de 4. Descartando sobra.")
                # Descartar os bytes finais incompletos
                resto = len(buf) % 4
                if resto != 0:
                    buf = buf[:-resto]
                    print(f"Descartados {resto} bytes, novo tamanho: {len(buf)}")

            # 3) Decodificar floats (manual IEEE-754) e imprimir 1 por linha
            numeros = []
            for i in range(0, len(buf), 4):
                bloco = bytes(buf[i:i+4])
                try:
                    num = ieee_para_float_manual(bloco)   # usa sua função manual (A+)
                    numeros.append(num)
                    print(f"{(i//4)+1:02d}: {num:.6f} (bytes: {bloco.hex()})")
                except Exception as e:
                    print(f"Erro ao decodificar bloco {i//4 + 1}: {e}")
                    print(f"Bytes: {bloco.hex()}")

            if not numeros:
                print("Nenhum número válido decodificado. Continuando...")
                continue

            # 4) Somar e responder em float32 (4 bytes) - manual
            soma = sum(numeros)
            soma_bytes = float_para_ieee_manual(soma)
            com1.sendData(soma_bytes)
            print(f"[SRV] soma enviada: {soma:.6f} (bytes: {soma_bytes.hex()})")
            
    except KeyboardInterrupt:
        print("\nServidor interrompido pelo usuário")
    except Exception as e:
        print(f"Erro geral: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            com1.disable()
            print("Comunicação encerrada")
        except:
            pass

if __name__ == "__main__":
    main()