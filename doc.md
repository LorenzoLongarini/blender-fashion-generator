# Blender Fashion Generator

<div align="center">
  <img src="path/to/banner.png" alt="Project Banner">
  
  <p>
    <img src="https://img.shields.io/badge/python-3.8-blue.svg" alt="Python">
    <img src="https://img.shields.io/badge/blender-3.6-orange.svg" alt="Blender">
    <img src="https://img.shields.io/badge/nerfstudio-0.3.4-green.svg" alt="Nerfstudio">
    <img src="https://img.shields.io/badge/license-GPL--3.0-red.svg" alt="License">
  </p>
</div>
---

## 🎯 Obiettivi del Progetto

Questo progetto si propone di esplorare le potenzialità delle tecniche di **Neural Radiance Fields (NeRFs)** e **3D Gaussian Splatting (3DGS)** per la ricostruzione di scene tridimensionali a partire da immagini 2D. Gli obiettivi principali includono:

- **Creazione automatizzata di dataset** strutturati, utilizzando modelli 3D del dataset **DeepFashion3D** tramite l'add-on **BlenderNeRF**.
- Implementazione di pipeline che consentano il rendering di immagini 3D fotorealistiche da punti di vista inediti.
- Addestramento e valutazione di reti basate su **NeRF (Nerfacto)** e **3DGS (Splatfacto)** utilizzando il framework **Nerfstudio**.
- Misurazione della qualità delle reti tramite metriche standard come **PSNR**, **SSIM** e **LPIPS**, con analisi dell’efficienza computazionale.

---

## 📊 Dataset

Il progetto utilizza il dataset **DeepFashion3D**, che contiene modelli 3D di capi d'abbigliamento con texture dettagliate. Questo dataset costituisce una base solida per generare immagini da diverse angolazioni e condizioni di illuminazione.

> **Credits**: [DeepFashion3D Dataset](https://github.com/GAP-LAB-CUHK-SZ/deepFashion3D)

---

## 💡 Ispirazione

Il nostro progetto si basa su due principali componenti:

- [BlenderNeRF](https://github.com/maximeraafat/BlenderNeRF)
- [Camera-On-Sphere (COS)](#camera-on-sphere-cos)
- [Train-Test-Camera (TTC)](#train-test-cameras-ttc)

---

## 🛠 Il Nostro Approccio

### Camera On Sphere (COS)

L'approccio **Camera On Sphere (COS)** estende l'implementazione originale con le seguenti funzionalità:

- **Sfondi personalizzabili**: possibilità di generare immagini con sfondo trasparente o bianco.
- **Generazione automatica dei dataset**: suddivisione in set di _train_, _validation_ e _test_.
- **Illuminazione solare realistica**: configurazioni ottimizzate per garantire immagini realistiche.
- **Ottimizzazione della posizione della camera**: posizionamento automatico della camera sulla sfera per una copertura uniforme.

> **Compatibilità**: Training diretto con **Instant NGP** o **Nerfacto**.

---

### Train Test Cameras (TTC)

L'approccio **Train Test Cameras (TTC)** introduce configurazioni avanzate per dataset dettagliati:

- **Setup automatico delle telecamere**: posizionamento ottimale delle camere.
- **Rotazione a 360°**: acquisizione completa dell'oggetto lungo l'asse Y.
- **Gestione avanzata dell'illuminazione**: simulazione di scenari di luce realistici.
- **Dataset strutturati**: organizzazione standardizzata dei dati per una facile integrazione nei modelli.

> **Compatibilità**: Richiede **COLMAP** per l'allineamento prima del training con **Instant NGP** o **Nerfacto**.

---

## 🆚 Differenze con Instant NGP e Nerfacto

| Approccio | Compatibilità Diretta    | Pre-Processing Necessario | Supporto Sfondi      | Illuminazione Realistica | Dataset Strutturato |
| --------- | ------------------------ | ------------------------- | -------------------- | ------------------------ | ------------------- |
| **COS**   | ✅ Instant NGP, Nerfacto | ✅ Nessun pre-processing  | ✅ Transparent/White | ✅                       | ✅                  |
| **TTC**   | ✅ Instant NGP, Nerfacto | ❌ COLMAP obbligatorio    | ✅ Transparent/White | ✅                       | ✅                  |

---

## 🛠 Prerequisiti

### Per COS:

- Installare le dipendenze per **Instant NGP** o **Nerfacto**.
- Configurare i parametri del modello per iniziare direttamente il training.

### Per TTC:

1. **Installare COLMAP**:

   - **Linux**:
     ```bash
     conda install -c conda-forge colmap
     ```
     oppure:
     ```bash
     sudo apt install colmap
     ```
   - **Windows**:
     - Scaricare l'ultima versione da [COLMAP Releases](https://github.com/colmap/colmap/releases).
     - Estrarre i file e aggiungere il percorso della cartella `bin` alle variabili d'ambiente.

2. **Generare i dati con COLMAP**:

   ```bash
   colmap feature_extractor --database_path <path_to_database> --image_path <path_to_images>

   colmap mapper --database_path <path_to_database> --image_path <path_to_images> --output_path <path_to_output>
   ```

3. **Procedere al training con Instant NGP o Nerfacto.**

---

## 🚀 Getting Started

### Ambiente Virtuale per Blender

1. Creare un ambiente virtuale:

```bash
   python -m venv .venv
```

2. Attivare l'ambiente virtuale:

```bash
   source .venv/bin/activate
```

3. Installare le dipendenze:

```bash
   pip install -r requirements.txt
```

---

### Configurazione in VSCode

1. Installare Blender Development plugin
2. Ctrl+Shift+P -> Blender: Start
3. Navigare a app.py
4. Ctrl+Shift+P -> Blender: Run Script

---

## Setup dell'Ambiente Nerfstudio

**1. Creazione ambiente Conda**

```bash
conda init
conda create --name nerfstudio -y python=3.8
conda activate nerfstudio
```

**2. Installazione dipendenze**

```bash
python -m pip install --upgrade pip
cd "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build"
.\vcvarsall.bat x64 -vcvars_ver=14.29
```

**3. Setup CUDA e PyTorch**

```bash
pip uninstall torch torchvision functorch tinycudann
pip install torch==2.1.2+cu118 torchvision==0.16.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
conda install -c "nvidia/label/cuda-11.8.0" cuda-toolkit
conda install git
```

**4. Installazione Nerfstudio**

```bash
pip install git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch
pip install nerfstudio
```

---

## 🎓 Training del Modello

### Training base

```bash
ns-train nerfacto --data path/to/data blender-data
```

### Training con predizione delle normali

```bash
ns-train nerfacto --data path/train --pipeline.model.predict-normals True blender-data
```

### Ripresa del training da checkpoint

```bash
ns-train nerfacto --data path/train --pipeline.model.predict-normals True --load-dir path/outputs/train/nerfacto/YYYY-MM-DD/nerfstudio_models blender-data
```

### Esportazione del modello

```bash
ns-export format --load-config path_config.yml --output-dir exports
```

---

## 📝 Licenza

Questo progetto è rilasciato sotto licenza **GPL-3.0**. Puoi trovare maggiori dettagli nel file [LICENSE](LICENSE).
