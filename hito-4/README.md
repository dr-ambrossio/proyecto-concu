# Hito 4 — Integración final


**Objetivo:** cerrar el ciclo teoría→práctica con un artefacto propio que combine CUDA y LLM, y defenderlo oralmente.

Elegí **una** de estas dos rutas. La cátedra puede ofrecer equivalentes.

---

## Ruta A — kernel propio

Implementá y optimizá un *kernel* CUDA que corresponda a una operación **real** de inferencia de un Transformer, en versión simplificada. Ejemplos válidos:

- softmax por fila
- *layer norm*
- multiplicación matriz-vector (posiblemente con pesos cuantizados de juguete)

Comparalo contra la implementación de referencia de PyTorch y/o el kernel equivalente de `llama.cpp` (si podés extraerlo o medirlo como caja negra).

El informe de esta ruta tiene que incluir: corrección (tolerancia declarada), tiempos **tuyos**, al menos un dato de Nsight Compute o `cudaEvent` etiquetado, y conexión explícita con las Clases 6–8.

Punto de partida razonable: `../hito-2/kernel_optimizado.cu` o el `matmul.cu` de la Clase 6. Esta carpeta no trae el kernel resuelto: el artefacto es de ustedes.

---

## Ruta B — medición y optimización de sistema

Usando el LLM local del Hito 3, aplicá y **medí** el efecto de al menos **dos** optimizaciones de inferencia. Ejemplos:

- cambio de nivel de cuantización
- *batching* / tamaño de contexto
- efecto de KV-cache (VRAM y *tokens/s* a dos `n_ctx`)
- *threads* CPU / `n_gpu_layers`
- flash-attn o *speculative decoding* **solo si tu build lo expone**

Perfilá con las herramientas de la Clase 11 (`nsys` / `ncu` / `nvidia-smi` / `torch.profiler` según aplique). Bitácora: un cambio por experimento. No copies *speedups* de papers de Hopper.

Plantilla de bitácora (copiala a `bitacora.md` en esta carpeta):

```text
Fecha:
GPU / CPU:
Ruta: B
Comando exacto:

Baseline
- métrica (tokens/s / VRAM / kernel_ms):
- valor (mediana de k corridas, k= ):
- evidencia (ncu / nsys / nvidia-smi / …):

Optimización 1 (una oración de hipótesis):
- cambio:
- re-medición:
- ¿confirmó la hipótesis?

Optimización 2:
- …
```

---

## Entregable

Repositorio **consolidado** (hitos 1–4) + informe completo (todos los hitos, con hilo conductor) + presentación oral de 10–15 min con demo en vivo, defendiendo las decisiones de diseño y respondiendo preguntas individuales.

### Checklist del repositorio final consolidado del grupo

- [ ] `README.md` en la raíz del **repo del grupo** (no solo el de la cátedra): integrantes, hardware (CPU, GPU, salida de `nvidia-smi` si aplica), cómo reproducir la demo (un comando)
- [ ] Hito 1: `secuencial` + `paralelo` con primitiva de sincronización + curva de speedup vs. Amdahl
- [ ] Hito 2: kernel ingenuo vs. optimizado + datos o capturas de Nsight (o fallback de `cudaEvent` declarado)
- [ ] Hito 3: CSV / tabla *tokens/s* vs. configuración + análisis ligado a la Unidad II
- [ ] Hito 4: ruta A **o** B elegida; código o scripts de esa ruta; bitácora de perfilado de la Clase 11
- [ ] Informe global que une los cuatro hitos (no cuatro PDF sueltos sin hilo conductor)
- [ ] Tag o commit `hito-4` en Git
- [ ] Política de IA: cada integrante puede explicar el código que entrega (la defensa incluye preguntas individuales)

### Demo en vivo

Una métrica **medida en el aula**, no solo una captura. Plan B si no hay GPU (CPU del Hito 1, o LLM en CPU del Hito 3).

### Oral individual

2–3 preguntas por persona. Rúbrica: `clases/clase-12/rubrica-en-vivo.md`.

## Rúbrica de este hito (100 pts)

Igual que los anteriores: 30 corrección funcional, 30 análisis con datos reales, 20 informe, 20 conexión teórica (ahora: todo el curso).
