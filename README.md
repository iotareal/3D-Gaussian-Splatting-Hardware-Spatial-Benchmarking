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
*(Add your conda environment setup commands and CUDA requirements here so your collaborators can get started).*
