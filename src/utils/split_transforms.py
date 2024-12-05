import json
import random
from pathlib import Path
from typing import Union, Dict, List

def split_transforms_json(
    input_file: Union[str, Path],
    val_ratio: float = 0.1,
    seed: int = 42
) -> None:
    """
    Divide il file transforms_train.json in training e validation set.
    
    Args:
        input_file: Percorso al file transforms_train.json
        val_ratio: Percentuale di immagini da usare per la validazione (default: 0.1)
        seed: Seed per la riproduzione dei risultati (default: 42)
    """
    # Converte il percorso in Path object
    input_path = Path(input_file)
    output_dir = input_path.parent
    
    # Legge il file JSON originale
    with open(input_path, 'r') as f:
        data = json.load(f)
    
    # Estrae i frames
    frames = data['frames']
    n_frames = len(frames)
    n_val = int(n_frames * val_ratio)
    
    # Imposta il seed per la riproducibilità
    random.seed(seed)
    
    # Seleziona casualmente gli indici per la validazione
    val_indices = set(random.sample(range(n_frames), n_val))
    
    # Crea i nuovi dizionari
    train_data = data.copy()
    val_data = data.copy()
    
    # Divide i frame
    train_frames = [f for i, f in enumerate(frames) if i not in val_indices]
    val_frames = [f for i, f in enumerate(frames) if i in val_indices]
    
    train_data['frames'] = train_frames
    val_data['frames'] = val_frames
    
    # Salva i nuovi file
    with open(output_dir / 'transforms_train_new.json', 'w') as f:
        json.dump(train_data, f, indent=4)
    
    with open(output_dir / 'transforms_val.json', 'w') as f:
        json.dump(val_data, f, indent=4)
    
    print(f"File divisi con successo!")
    print(f"Training frames: {len(train_frames)}")
    print(f"Validation frames: {len(val_frames)}")

if __name__ == "__main__":
    # Esempio di utilizzo
    split_transforms_json(
        "C://Users//lollo//Universita//Progetto//trainCOSNerf//transforms_train.json",
        # "../../assets/output/train/transforms_train.json",
        val_ratio=0.1  # 10% per validazione
    )