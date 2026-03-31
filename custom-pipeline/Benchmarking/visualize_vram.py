import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def generate_vram_graph(csv_path):
    csv_file = Path(csv_path)
    if not csv_file.exists():
        print(f"Error: File {csv_path} not found.")
        return

    print(f"Loading data from {csv_file.name}...")
    df = pd.read_csv(csv_file)

    # 2. Clean the data
    # Strip accidental spaces from column headers
    df.columns = [c.strip() for c in df.columns] 
    
    # Find the memory column dynamically
    mem_col = [c for c in df.columns if 'memory' in c.lower()][0]
    time_col = df.columns[0]

    # Remove the ' MiB' string and convert to integer for plotting
    if df[mem_col].dtype == object:
        df[mem_col] = df[mem_col].str.replace(' MiB', '').astype(int)

    # 3. Calculate Relative Time (Seconds from start)
    df[time_col] = pd.to_datetime(df[time_col])
    df['seconds'] = (df[time_col] - df[time_col].iloc[0]).dt.total_seconds()

    # 4. Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(df['seconds'], df[mem_col], color='#007acc', linewidth=2, label='VRAM Usage')
    plt.fill_between(df['seconds'], df[mem_col], color='#007acc', alpha=0.1)

    # 5. Aesthetics & Peak Annotation
    peak_vram = df[mem_col].max()
    plt.title(f"3DGS VRAM Usage Profile: {csv_file.stem}", fontsize=14)
    plt.xlabel("Training Time (Seconds)", fontsize=12)
    plt.ylabel("Memory Used (MiB)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Draw a red dashed line for the peak VRAM
    plt.axhline(y=peak_vram, color='red', linestyle=':', label=f'Peak: {peak_vram} MiB')
    plt.legend()

    # 6. Save the Graph
    output_png = csv_file.with_suffix(".png")
    plt.tight_layout()
    plt.savefig(output_png)
    print(f"Graph successfully saved as: {output_png}")
        