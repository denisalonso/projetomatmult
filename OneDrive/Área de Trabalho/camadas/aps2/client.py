#!/usr/bin/env python3
# -- coding: utf-8 --
#####################################################
# Camada Física da Computação
# Projeto 2 - Cliente (SEM HEADER)
####################################################

from enlace import *
import time
import struct

def main():
    try:
        # Configuração da porta serial
        serialName = "COM9"  # Porta DIFERENTE do servidor
        com1 = enlace(serialName)
        
        # Inicializa comunicação
        com1.enable()
        print("Cliente inicializado")
        print(f"Porta: {serialName}")
        
        # Byte de sacrifício
        time.sleep(0.2)
        com1.sendData(b'00')
        time.sleep(1.0)
        print("Byte de sacrifício enviado")
        
        # Lista de números para enviar (5 a 15 números) - SEM HEADER
        numeros = [5.0, 11.19, -1.43567, 0.125, 1.235865]
        
        print(f"Enviando {len(numeros)} números (sem header):")
        
        # Envia cada número individualmente (4 bytes cada - float32)
        for i, numero in enumerate(numeros):
            num_bytes = struct.pack('>f', numero)  # Big-endian float32
            com1.sendData(num_bytes)
            print(f"Enviando número {i+1}: {numero:.6f} (bytes: {num_bytes.hex()})")
            time.sleep(0.1)  # Pequena pausa entre números
        
        # Aguarda um pouco para garantir que todos os bytes foram enviados
        time.sleep(0.5)
        
        # Aguarda a resposta do servidor (soma - 4 bytes)
        print("Aguardando soma do servidor (timeout 10s)...")
        start_time = time.time()
        timeout = 10.0
        
        while time.time() - start_time < timeout:
            buffer_len = com1.rx.getBufferLen()
            if buffer_len > 0:
                print(f"Buffer RX: {buffer_len} bytes")
            
            if buffer_len >= 4:
                soma_bytes, nRx = com1.getData(4)
                print(f"Bytes da soma recebidos: {soma_bytes.hex()}")
                
                soma_recebida = struct.unpack('>f', soma_bytes)[0]
                soma_esperada = sum(numeros)
                
                diferenca = abs(soma_recebida - soma_esperada)
                if diferenca < 1e-6:
                    print(f"✓ Soma consistente: {soma_recebida:.6f}")
                else:
                    print(f"✗ INCONSISTÊNCIA!")
                    print(f"  Esperado: {soma_esperada:.6f}")
                    print(f"  Recebido: {soma_recebida:.6f}")
                    print(f"  Diferença: {diferenca:.6e}")
                break
                
            time.sleep(0.1)
        else:
            print(f"✗ TIMEOUT: Nada recebido em {timeout} segundos")
            print(f"Buffer final: {com1.rx.getBufferLen()} bytes")
        
        # Encerra comunicação
        com1.disable()
        print("Comunicação encerrada")

    except Exception as erro:
        print(f"Erro no cliente: {erro}")
        import traceback
        traceback.print_exc()
        try:
            com1.disable()
        except:
            pass

if __name__ == "__main__":
    main()