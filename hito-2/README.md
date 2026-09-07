# Hito 2 — Kernels CUDA optimizados


**Objetivo:** portar el problema del Hito 1 (suma de vector, o equivalente) a GPU e **optimizar** con una técnica de las Clases 6–7.

## Enunciado

1. `kernel_ingenuo.cu` — ya está: cada hilo hace `atomicAdd` sobre un acumulador en global. Compila con `nvcc`. Es correcto y suele ser **lento**: sirve de baseline.
2. `kernel_optimizado.cu` — esqueleto de reducción con memoria compartida. Completá los `TODO`. Compila desde el día uno; no es la solución hasta que los TODO sean una reducción paralela de verdad (un `for` serial en el hilo 0 no cuenta).
3. Perfilar **ambas** versiones con Nsight Compute (ocupación, *throughput* de memoria, tiempo). Si `ncu` no está, `cudaEvent` + declaración de limitación (Clase 7).
4. Informe: CPU (Hito 1) vs. GPU ingenua vs. GPU optimizada, con **tus** *ms* y capturas/CSV de perfilado.

Técnica mínima: memoria compartida / *tiling* / coalescencia. No copies GB/s de un tutorial.

## Compilación

```bash
make
./kernel_ingenuo 16777216
./kernel_optimizado 16777216
```

Si `nvcc` se queja de la arquitectura, pasá la de tu GPU (`nvidia-smi` + tabla de *compute capability*):

```bash
make NVCCFLAGS="-std=c++17 -O2 -arch=sm_75"
```

Colab: compilá con `nvcc` en una celda; `ncu` a menudo no está → fallback de eventos.

Hasta completar los `TODO`, `./kernel_optimizado` imprime `FAIL` (el placeholder escribe ceros). Eso es esperado.

## Perfilar con Nsight Compute

Instalá el CUDA Toolkit (incluye `ncu`) o Nsight Compute por separado. En el laboratorio / máquina con GPU NVIDIA:

```bash
# ¿está ncu en el PATH?
ncu --version

# Corrida completa (genera ingenuo.ncu-rep). Puede tardar varios minutos.
ncu --set full -o ingenuo ./kernel_ingenuo 16777216
ncu --set full -o opt     ./kernel_optimizado 16777216
```

Abrí los `.ncu-rep` en Nsight Compute (GUI) o listá métricas en texto:

```bash
ncu --import ingenuo.ncu-rep --page details
ncu --import opt.ncu-rep --page details
```

Si `--set full` es demasiado pesado, un subconjunto útil para este hito:

```bash
ncu --metrics sm__warps_active.avg.pct_of_peak_sustained_active,\
gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed,\
gpu__time_duration.avg \
    -o ingenuo-rapido ./kernel_ingenuo 16777216
```

Anotá en el informe, para **las dos** versiones:

| Dato | Dónde suele aparecer |
|---|---|
| Tiempo del kernel | `gpu__time_duration` o la sección Duration |
| Ocupación | *Occupancy* / `sm__warps_active` |
| Throughput de memoria | *Memory Workload Analysis* |

Compará con los `kernel_ms` de `cudaEvent` del propio binario. Si `ncu` no corre (Colab, driver viejo, falta de permisos), medí con eventos, pegá el error de `ncu` y explicá la limitación.

## Criterio de “listo”

- [ ] ambas versiones `ok` vs. referencia (tolerancia: usá `double` en CPU)
- [ ] una técnica visible en el código optimizado (no solo el nombre en el informe)
- [ ] tabla de tiempos propia
- [ ] dato de perfilado o fallback explícito

## Archivos

| Archivo | Rol |
|---|---|
| `kernel_ingenuo.cu` | baseline compilable |
| `kernel_optimizado.cu` | *shared* + TODOs |
| `Makefile` | `nvcc -std=c++17` |
