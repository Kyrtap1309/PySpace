import spiceypy

def kernels_load(kernels_path):
    for kernel_path in kernels_path:
        spiceypy.furnsh(kernel_path)