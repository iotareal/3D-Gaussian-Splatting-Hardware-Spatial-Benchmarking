# 3D Gaussian Splatting: Hardware & Spatial Benchmarking

## 📌 Project Overview
This repository contains the codebase, benchmarking telemetry, and documentation for an in-depth performance analysis of Explicit 3D Gaussian Splatting (3DGS). 

The goal of this research project is to evaluate rendering throughput, memory saturation, and quantitative reconstruction quality across two primary axes:
1. **Hardware Constraints:** Consumer-grade GPUs (RTX 3060) vs. Enterprise/Flagship GPUs (RTX 5090).
2. **Spatial Typologies:** Bounded/Subject-centric datasets vs. Unbounded/Environment-centric datasets.

## 🗂️ Repository Anatomy (Core Architecture)
Understanding the pipeline from preprocessing to Differentiable Rasterization:

* **`convert.py`**: The preprocessing wrapper for COLMAP. Converts raw images/video into the required Structure-from-Motion (SfM) format and extracts the initial sparse point cloud.
* **`train.py`**: The core optimization engine. Loads SfM data, initializes the `GaussianModel`, executes the forward/backward passes, calculates loss, and triggers Adaptive Density Control (cloning/splitting).
* **`render.py`**: The inference and evaluation script. Takes the optimized `.ply` model and generates 2D `.png` renders to calculate PSNR, SSIM, and LPIPS metrics.
* **`scene/` folder**: Contains `cameras.py` (viewport logic) and `gaussian_model.py` (defines the mathematical properties of the Gaussian primitives and the densification logic).
* **`gaussian_renderer/` folder**: The bridge connecting the Python training loop to the C++/CUDA backend, pushing the 3D viewport into the custom rasterizer.
* **`utils/loss_utils.py`**: Contains the mathematical definitions for the optimization targets (L1 Loss and D-SSIM).
* **`submodules/`**: Houses the highly optimized compiled CUDA kernels, including the Differentiable Gaussian Rasterizer and the Simple-KNN (K-Nearest Neighbors) algorithm for initialization.

## 🚀 Research Roadmap
- [x] **Phase 1:** Local Implementation & Baseline Environment Setup (CUDA 11.8, Visual Studio 2019, Conda).
- [ ] **Phase 2:** Inject custom telemetry into `train.py` to log VRAM allocation, FPS, and primitive counts over 30k iterations.
- [ ] **Phase 3:** Execute benchmarking on Baseline Hardware (NVIDIA RTX 3060).
- [ ] **Phase 4:** Capture and preprocess custom Subject and Environment datasets.
- [ ] **Phase 5:** Execute benchmarking on Flagship Hardware (NVIDIA RTX 5090).
- [ ] **Phase 6:** Publish comprehensive data visualizations and FYP Research Paper.

## 🛠️ Setup & Installation
**Note:** The versions of all the tools and utils are crucial to run the engine as well as the renderer, if you did not match the version listed under this note you will likely face major errors which could take days to fix.

### Step #0 Download and maintain a directory
**1. Clone this Repository**
```
git clone --recursive https://github.com/iotareal/3D-Gaussian-Splatting-Hardware-Spatial-Benchmarking.git
```

**2. Download [COLMAP v3.8](https://github.com/colmap/colmap/releases/tag/3.8)**\
Download CUDA version, non-CUDA version is not for this project

**3. Download Latest version of [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)**\
If low on space use Miniconda instead of Anaconda

**4. Download Visual Studio 19**\
Version is crucial here we need correct version of MSVC C++ compiler which can couple with CUDA Toolkit, There is no official source for visual studio 19, however you can look up for third-party installer avaliable on various websites, DO NOT INSTALL LATEST VISUAL STUDIO.

**5. Download [CUDA Toolkit 11.8](https://developer.nvidia.com/cuda-11-8-0-download-archive)**\
Exact version **11.8** is required.

**6. Download Latest version of [SIBR Viewer](https://sibr.gitlabpages.inria.fr/download.html)**\
Select Win64, Release under the "Core" section.
