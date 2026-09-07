# Proyecto incremental — de un hilo de CPU a un LLM en GPU

**Curso:** Programación Concurrente y Paralela (3er año)  
**Modalidad:** grupos de 2–3 estudiantes  
**Formato:** un repositorio Git **por grupo**. Cada hito suma código + un `README` (o sección) con diseño, **benchmarks medidos por ustedes** y aprendizajes.

## Qué van a construir

Cuatro hitos alineados a las unidades. El hito final conecta la teoría de paralelismo con la ejecución de un LLM.

| Hito | Entrega (clase) | Peso (supuesto del programa) | Carpeta |
|---|---|---|---|
| 1 — Concurrencia CPU | Clase 4 | 12 % | [`hito-1/`](hito-1/README.md) |
| 2 — Kernels CUDA | Clase 7 | 15 % | [`hito-2/`](hito-2/README.md) |
| 3 — LLM local + métricas | Clase 9 | 15 % | [`hito-3/`](hito-3/README.md) |
| 4 — Integración y defensa | Clase 12 | 18 % | [`hito-4/`](hito-4/README.md) |

La evaluación integradora de la Clase 12 (examen + oral + demo) es **aparte** (30 %). Participación / entregables cortos de clase: 10 %.

## Estructura de repo esperada

Pueden clonar o copiar estas carpetas como punto de partida. Al final del curso el repo del grupo debería verse así:

```text
README.md                 ← este archivo, adaptado con nombre del grupo
hito-1/                   ← secuencial, paralelo, benchmark, informe
hito-2/                   ← kernels .cu, Makefile, datos Nsight
hito-3/                   ← instalar.md, CSV de mediciones, informe
hito-4/                   ← ruta A o B, bitácora de perfilado, informe global
informes/                 ← opcional: PDFs o Markdown de cada hito
```

Incluí en el README raíz: integrantes, hardware usado (CPU, GPU, `nvidia-smi`), y cómo compilar.

## Hardware y software

GPU NVIDIA + CUDA 12.x (propia, laboratorio o Colab/nube), C++17, Python 3.11, y para el Hito 3 `llama.cpp` **u** Ollama. Si no hay GPU local, Colab cubre CUDA; el Hito 1 es CPU.

## Informes

Hitos 1–3: 1–2 páginas (más tablas/gráficos). Hito 4: informe que consolida los cuatro. En todos: comando exacto, tamaño de problema, número de corridas, mediana o promedio **declarado**.
