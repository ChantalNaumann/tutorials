
```python
plt.style.use("my_style.mplstyle")
```

`neurodata.py` generates all the data (LIF neuron, Poisson rasters, V1 tuning, GCaMP-like imaging, LFP,
a paired drug experiment), so nobody gets stuck loading files.

| matplotlib default | after notebook 2 |
|---|---|
| ![](reference/previews/before_default.png) | ![](reference/previews/after_basics.png) |

## How to run it

### Option 1: Google Colab (nothing to install)

You only need a browser and a Google account. Click a badge to open the notebook in Colab:

| Notebook | |
|---|---|
| 01 · First plot | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChantalNaumann/tutorials/blob/main/01_first_plot.ipynb) |
| 02 · Style files | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChantalNaumann/tutorials/blob/main/02_style_files.ipynb) |
| 03 · Neuroscience plots | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChantalNaumann/tutorials/blob/main/03_neuroscience_plots.ipynb) |
| 03 · Neuroscience plots, beginner version | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChantalNaumann/tutorials/blob/main/03_neuroscience_plots_beginner.ipynb) |
| 05 · Toolbox | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChantalNaumann/tutorials/blob/main/05_toolbox.ipynb) |

* **Run the first code cell** of every notebook: it downloads the course data.
* **Colab deletes your files when you close a notebook.** At the end of notebook 2, run the last cell to download
  your `my_style.mplstyle`. Notebooks 3 and 5 ask you to upload it (click *Cancel* to use a ready-made style instead).
* **To edit your style file:** click the folder icon 📁 on the left, double-click `my_style.mplstyle`, change it,
  and save with **Ctrl+S**.

### Option 2: on your own computer, with uv

[uv](https://docs.astral.sh/uv/) installs Python and everything the course needs into the course folder, with
one command. Nothing else on your computer changes.

**1. Install uv** (once). Then close and reopen the terminal.

```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**2. Get the course.** Either with git:

```bash
git clone https://github.com/ChantalNaumann/tutorials.git
cd tutorials
```

or on GitHub click **Code → Download ZIP**, unzip it, and open a terminal in that folder.

**3. Install everything** (Python 3.12, NumPy, SciPy, matplotlib, Jupyter) into a `.venv` folder inside the course folder:

```bash
uv sync
```

**4. Open the notebooks**, in your editor or in the browser:

* **VS Code:** *File → Open Folder…* and pick the course folder. Open a notebook, click **Select Kernel** (top
  right) → *Python Environments* → **.venv**. If VS Code asks to install the Python or Jupyter extension, say yes.
* **Browser (JupyterLab):**
  ```bash
  uv run jupyter lab
  ```

Run the notebooks in order: notebook 2 creates `my_style.mplstyle`, and notebooks 3 and 5 use it.
To remove everything again, delete the course folder.

*Prefer conda?* `conda env create -f environment.yml`, `conda activate plotcourse`, `jupyter lab`.
