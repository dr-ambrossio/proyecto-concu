# Hito 3 — LLM local y métricas de inferencia


**Objetivo:** instalar un runtime local, correr un modelo **cuantizado que entre en tu hardware**, y explicar los números con la Unidad II (SIMT, jerarquía de memoria).

## Enunciado

1. Instalá `llama.cpp` **u** Ollama (en clase se piden **ambos** instalados; el informe usa uno para medir). Pasos: [`instalar.md`](instalar.md).
2. Al menos un modelo abierto cuantizado (familias Llama, Mistral, Qwen, u otra vigente en Hugging Face / librería Ollama). **El tamaño tiene que caber** en GPU o RAM. Ctx grande puede OOM aunque el GGUF entre (KV-cache).
3. Medí *tokens/segundo* y memoria variando:
   - (a) nivel de cuantización (p. ej. Q4 vs. Q8 del **mismo** modelo)
   - (b) *batch* y/o contexto
4. Análisis: por qué cuantización y *batching* mueven (o no) el rendimiento, con tus datos y conceptos de las Clases 5–7.

## Entregable

- Informe con tabla/gráfico *tokens/s* vs. configuración
- Sección de análisis → Unidad II
- CSV generado o completado a partir de `medir_inferencia.py`

## Script

```bash
python3 medir_inferencia.py --help
# Completá los TODO del archivo (runtime, modelo, grilla de configs).
python3 medir_inferencia.py --runtime ollama --model qwen2:0.5b --cuantizacion q4 --batch-size 1 --ctx 2048 --out resultados.csv
```

Parámetros configurables del esqueleto: `--cuantizacion` (etiqueta), `--batch-size`, `--ctx`, `--model`. Para Q4 vs Q8 cambiá el `--model` (otro tag u otro GGUF) y corré de nuevo, o expandí la lista `configs` del script.

Los *tokens/s* son **tuyos**. No copies un benchmark público a la tabla.

## Criterio de “listo”

- [ ] comando de corrida reproducible en el informe
- [ ] ≥ 3 filas (cuantización y batch/ctx)
- [ ] memoria anotada (`nvidia-smi` u otra)
- [ ] párrafo SIMT / global / memory-bound vs. compute-bound
