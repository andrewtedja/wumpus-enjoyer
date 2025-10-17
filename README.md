<div align="center">
   <img width=100% src="https://capsule-render.vercel.app/api?type=waving&height=300&color=0:1e3a8a,25:3b82f6,75:60a5fa,100:1e3a8a&text=Wumpus%20Enjoyer&fontColor=ffffff&fontSize=60" />
</div>

> **Advanced Course Scheduling System using Local Search Algorithms**

> Developed with ❤️ for **IF3170 Artificial Intelligence** Course

---

<div align="center">

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white)](https://matplotlib.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)

</div>

---

## Table of Contents

-   [About The Project](#-about-the-project)
-   [Features](#-features)
-   [Algorithms Implemented](#-algorithms-implemented)
-   [Project Structure](#-project-structure)
-   [Getting Started](#-getting-started)
    -   [Prerequisites](#prerequisites)
    -   [Installation](#installation)
    -   [Running the Application](#running-the-application)
-   [Input Format](#-input-format)
-   [Output & Visualization](#-output--visualization)
-   [Contributors](#-contributors)
-   [License](#-license)

---

## About The Project

**Wumpus Enjoyer** is an intelligent course scheduling system that optimizes weekly class timetables for universities implemented using Local Search algorithms such as Hill Climbing, Simulated Annealing, and Genetic Algorithm. The system efficiently handles multiple constraints including room capacities, credit hours (SKS), student enrollments, priority-based assignments, and time slot conflicts, both for students and lecturers.

### Key Objectives

-   **Minimize scheduling conflicts** between courses, rooms, and students
-   **Optimize resource utilization** for classrooms and time slots
-   **Handle complex constraints** including student priorities and room capacities
-   **Provide visual feedback** on scheduling optimization progress

---

## Features

### Core Functionality

-   **Multi-constraint Scheduling**: Handles courses, rooms, students, and time slots simultaneously with objective function calculation for conflicts
-   **Input**: JSON-based configuration for easy data management
-   **Plot & Visualization**: Timetable generation and algorithm performance plots
-   **Output**: performance metrics such as objective function values, time taken, number of iterations, and more

### Bonus Done:

<table>
    <tr>
        <th>Variant</th>
        <th>Done</th>
    </tr>
    <tr>
        <td>All Hill Climbing Variants</td>
        <td>✅</td>
    </tr>
    <tr>
        <td>Lecturer Schedule</td>
        <td>✅</td>
    </tr>
</table>

---

## Algorithms Implemented

### Hill Climbing Variants

1. **Steepest Ascent Hill Climbing**

    - Evaluates all neighbors
    - Selects the best improvement

2. **Hill Climbing Sideways Move**

    - Allows lateral moves
    - Escapes plateaus

3. **Random Restart Hill Climbing**

    - Multiple random initializations when stuck
    - Explores diverse solution spaces until convergence

4. **Stochastic Hill Climbing**
    - Probabilistic neighbor selection
    - Search until maximum iteration

### Advanced Algorithms

5. **Simulated Annealing**

    - Temperature-based acceptance
    - Accepts worse solutions probabilistically
    - Gradually cools to converge
    - Count stuck frequencies

6. **Genetic Algorithm**
    - Population-based search
    - Crossover and mutation operators
    - Natural selection mechanism

---

## 📁 Project Structure

```
wumpus-enjoyer/
├── 📂 input/
│   ├── sample_input.json          # Sample input configuration
│   └── jadwal_awal.png            # Initial state visualization
│
├── 📂 output/
│   ├── 📂 ga/                     # Genetic Algorithm results
│   ├── 📂 hc/                     # Hill Climbing results
│   ├── 📂 sa/                     # Simulated Annealing results
│   └── jadwal_final.png           # Final optimized schedule
│
├── 📂 src/
│   ├── 📂 algorithm/
│   │   ├── __init__.py
│   │   ├── genetic_algorithm.py   # GA implementation
│   │   ├── hill_climbing.py       # HC variants implementation
│   │   └── simulated_annealing.py # SA implementation
│   │
│   ├── 📂 utils/
│   │   ├── __init__.py
│   │   ├── GA_utils.py            # Genetic Algorithm utilities
│   │   ├── objective.py           # Objective function & constraints
│   │   ├── plotter.py             # Performance visualization
│   │   ├── state.py               # State representation
│   │   └── visualize_timetable.py # Timetable visualization
│   │
│   ├── __init__.py
│   └── main.py                    # Application entry point
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## How to Run

### Prerequisites

-   Python 3.8 or higher
-   pip package manager
-   Virtual environment (recommended)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/andrewtedja/wumpus-enjoyer.git
cd wumpus-enjoyer
```

2. **Create and activate virtual environment**

```bash
# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
source venv/Scripts/activate

```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python src/main.py
```

> Note: Visualization results will be saved in the `output/` directory

---

## Input Format

The system accepts JSON input files with the following structure:

```json
{
	"kelas_mata_kuliah": [
		{
			"kode": "IF3071_K01",
			"jumlah_mahasiswa": 60,
			"sks": 3
		}
	],
	"ruangan": [
		{
			"kode": "7609",
			"kuota": 60
		}
	],
	"mahasiswa": [
		{
			"nim": "13523601",
			"daftar_mk": ["IF3071_K01", "IF3130_K01"],
			"prioritas": [1, 2]
		}
	]
}
```

Bonus: jadwal dosen

```json
"dosen": [
		{
			"nama": "Dr. Andi",
			"mengajar": ["IF3110", "IF3170"],
			"waktu_sibuk": [
				{ "hari": "Senin", "jam": [9, 11] },
				{ "hari": "Rabu", "jam": [14, 16] }
			]
        },
]
```

### Input Components

| Component             | Description         | Attributes                        |
| --------------------- | ------------------- | --------------------------------- |
| **kelas_mata_kuliah** | Course information  | `kode`, `jumlah_mahasiswa`, `sks` |
| **ruangan**           | Room specifications | `kode`, `kuota`                   |
| **mahasiswa**         | Student enrollments | `nim`, `daftar_mk`, `prioritas`   |
| **dosen**             | Lecturer's schedule | `nama`, `mengajar`, `waktu_sibuk` |

## Output & Visualization

### Timetable Visualization

This project generates an interactive timetable grid for the final schedule after local search:

-   **X-axis**: Weekdays (Monday - Friday)
-   **Y-axis**: Time slots (07:00 - 17:00)
-   **Cells**: Course codes assigned to time slots

<div align="center">
<img src="./test/ga/population/pop-10/pop-10-final-1.png" alt="Final Schedule" width="80%"/>
<p><i>Example: Final optimized schedule using Genetic Algorithm</i></p>
</div>

### Performance Plots

Each algorithm generates performance metrics showing:

-   Objective function value over iterations
-   Convergence behavior
-   Algorithm-specific metrics (temperature, population fitness, etc.)

<div align="center">
<img src="./test/ga/population/pop-10/pop-10-plot-1.png" alt="GA Performance" width="80%"/>
<p><i>Example: Genetic Algorithm performance visualization</i></p>
</div>

---

## Contributors

| NIM          | Nama                      |
| ------------ | ------------------------- |
| **13523148** | **Andrew Tedjapratama**   |
| **13523141** | **Jovandra Otniel P. S.** |
| **13523154** | **Theo Kurniady**         |

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
   <img width=100% src="https://capsule-render.vercel.app/api?type=waving&height=120&color=0:1e3a8a,25:3b82f6,75:60a5fa,100:1e3a8a&section=footer" />
</div>
