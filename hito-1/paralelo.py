import sys
import threading

# Índice compartido para despacho dinámico de bloques
mtx = threading.Lock()
proximo = 0

# Tamaño de bloque de trabajo (2^16 = 65536)
BLOQUE = 1 << 16


def worker(data: list[float], n: int, parciales: list[float], thread_id: int):
    global proximo
    acc = 0.0

    while True:
        lo = 0
        hi = 0

        # Sección crítica: tomamos el rango de forma exclusiva
        with mtx:
            if proximo >= n:
                break  # No hay más trabajo disponible

            lo = proximo
            hi = min(n, proximo + BLOQUE)
            proximo = hi

        # El procesamiento pesado se realiza FUERA del candado
        for i in range(lo, hi):
            acc += data[i]

    # Cada hilo guarda su resultado en su posición dedicada (sin carreras de datos)
    parciales[thread_id] = acc


def main():
    global proximo

    # Lectura de argumentos de la línea de comandos
    n = int(sys.argv[1]) if len(sys.argv) > 1 else (1 << 24)
    t = int(sys.argv[2]) if len(sys.argv) > 2 else 4

    if n < 1 or t < 1:
        print("Error: N >= 1 y T >= 1", file=sys.stderr)
        sys.exit(1)

    # Inicialización del vector de datos y parciales
    a = [1.0] * n
    parciales = [0.0] * t
    hilos: list[threading.Thread] = []

    proximo = 0

    # Creación y lanzamiento de los hilos
    for i in range(t):
        hilo = threading.Thread(target=worker, args=(a, n, parciales, i))
        hilos.append(hilo)
        hilo.start()

    # Esperar a que todos los hilos terminen
    for hilo in hilos:
        hilo.join()

    # Reducción final en el hilo principal
    total = sum(parciales)

    print(f"N={n} T={t} suma={total}")


if __name__ == "__main__":
    main()