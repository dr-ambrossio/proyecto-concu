# Instalación — llama.cpp y Ollama

Instalá **los dos** en la Clase 9. Para el informe del Hito 3 alcanza **un** runtime de medición. Seguí siempre el README **oficial vigente** (los flags cambian). Enlaces en `recursos/enlaces.md`.

Elegí un modelo cuyo GGUF / tag **entre** en tu VRAM o RAM. Si OOM: bajá ctx, pasá a Q4, o CPU, y documentalo.

---

## Ollama

1. Instalador oficial: [https://ollama.com](https://ollama.com)
2. Comprobación:

```bash
ollama --version
```

3. Un modelo **chico** de prueba (el tag puede cambiar; buscá uno vigente en la librería):

```bash
ollama pull qwen2:0.5b
ollama run qwen2:0.5b "Hola"
```

API local típica: `http://127.0.0.1:11434`. `medir_inferencia.py --runtime ollama` usa esa vía.

Para variar cuantización con Ollama, en general hace falta **otro tag** (p. ej. un modelo `:q4_0` vs `:q8_0` si existe en la librería), no un flag suelto. Anotá el tag exacto en el CSV.

macOS / Apple Silicon: suele ser Metal, no CUDA. Declaralo: las métricas valen; el puente a SIMT NVIDIA es conceptual.

---

## llama.cpp

Repo: [https://github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
# GPU NVIDIA (CUDA 12.x del curso):
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j
# Solo CPU:
# cmake -B build && cmake --build build --config Release -j
```

Binarios típicos: `build/bin/llama-cli`, `build/bin/llama-bench` (nombres según versión). GGUF: Hugging Face, **del tamaño que entre**.

```bash
./build/bin/llama-cli -h
./build/bin/llama-bench -h
```

Para medir con el script:

```bash
export LLAMA_CLI=/ruta/llama.cpp/build/bin/llama-cli
python3 medir_inferencia.py --runtime llama --model /ruta/modelo-q4.gguf --cuantizacion q4
```

Completá los TODO del script: los flags exactos (`-n`, `-c`, `-b`, `-ngl`, …) salen de `-h`, no de este archivo petrificado. Para Q4 vs Q8 usá **dos GGUF** del mismo modelo base.

---

## Memoria

Con el modelo cargado:

```bash
nvidia-smi
```

Anotá memoria usada, GPU, y si hubo *offload* a CPU (`n_gpu_layers` / equivalente). En macOS sin NVIDIA, Activity Monitor / `os.Process` no reemplazan `nvidia-smi`: declaralo.
