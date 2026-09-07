# Makefile Hito 2 — kernels CUDA del mismo problema que el Hito 1 (suma).
# Ajustá la arquitectura a tu GPU si hace falta, p. ej.:
#   make NVCCFLAGS="-std=c++17 -O2 -arch=sm_86"
NVCC      ?= nvcc
NVCCFLAGS ?= -std=c++17 -O2

all: kernel_ingenuo kernel_optimizado

kernel_ingenuo: kernel_ingenuo.cu
	$(NVCC) $(NVCCFLAGS) -o $@ $<

kernel_optimizado: kernel_optimizado.cu
	$(NVCC) $(NVCCFLAGS) -o $@ $<

clean:
	rm -f kernel_ingenuo kernel_optimizado

.PHONY: all clean
