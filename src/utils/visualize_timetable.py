import math
import matplotlib.pyplot as plt

# Function buat grid dimensions matplotlib
def grid_dims(n):
    if n > 0:
        cols = min(3, n) 
    else:
        cols = 1

    if n > 0:
        rows = math.ceil(n / cols) 
    else:
        rows = 1
    return rows, cols

# Function buat visualisasi time table grid matplotlib
def visualize_state(state, rooms, days=None, hours=None, title="Jadwal Mingguan",
                    save_path=None, show=True):
    days = days or ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]

    # jamlist
    hours = hours or list(range(7, 18))

    n = len(rooms)
    r, c = grid_dims(n)

    fig, axes = plt.subplots(r, c, figsize=(4.5 * c, 3.2 * r), squeeze=False)
    fig.suptitle(title, fontsize=16, y=1)

    bucket = {}
    # bucket and title
    for (h, j, ruang), code in state.items():
        key = (h, j, ruang)
        bucket[key] = (str(code) if key not in bucket else f"{bucket[key]}\n{code}")

    # grid table
    for idx, room in enumerate(rooms):
        ax = axes[idx // c][idx % c]
        ax.axis("off")

        rows_text = []
        for jam in hours:
            row = []
            for day in days:
                row.append(bucket.get((day, jam, room), ""))
            rows_text.append(row)

        tbl = ax.table(
            cellText=rows_text,
            rowLabels=hours,
            colLabels=days,
            loc="center",
            cellLoc="center",
        )
        tbl.scale(1, 1.1)  
        ax.text(
            0.5, 1, f"Kode ruang: {room}",
            fontsize=11, fontweight="bold",
            ha="center", va="bottom", transform=ax.transAxes
        )

    # remove subplot kosong
    for k in range(n, r * c):
        ax = axes[k // c][k % c]
        ax.axis("off")

    plt.subplots_adjust(hspace=0.55, wspace=0.25)
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    if save_path:
        fig.savefig(save_path, dpi=160, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)
