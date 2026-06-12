# 🔬 Cantera Stream Mixer GUI

A Python-based graphical user interface for simulating and visualizing gas stream mixing using the Cantera chemical kinetics library.

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Cantera](https://img.shields.io/badge/cantera-2.6%2B-orange)

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Interface Overview](#interface-overview)
- [Visualization Features](#visualization-features)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Intuitive GUI**: Modern, user-friendly interface built with Tkinter
- **Real-time Simulation**: Mix two gas streams with different compositions, temperatures, and pressures
- **Comprehensive Visualization**:
  - 📊 Composition pie charts
  - 📈 Properties comparison bar charts
  - 🔀 Flow process diagrams
  - 📝 Detailed text reports
- **Species Management**: Load and view available chemical species from mechanism files
- **Input Validation**: Robust error checking for compositions and species
- **Responsive Design**: Resizable interface with scrollable content areas
- **Interactive Plots**: Zoom, pan, and save visualization outputs

## 📦 Prerequisites

- Python 3.7 or higher
- Cantera 2.6.0 or higher
- Required Python packages:
  ```
  cantera
  matplotlib
  numpy
  tkinter (usually included with Python)
  ```

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/karimireza77/cantera-stream-mixer.git
cd cantera-stream-mixer
```

### 2. Install Dependencies

#### Using pip
```bash
pip install cantera matplotlib numpy
```

#### Using conda (recommended for Cantera)
```bash
conda create -n cantera-mixer python=3.9
conda activate cantera-mixer
conda install -c cantera cantera
pip install matplotlib numpy
```

### 3. Verify Installation

```bash
python -c "import cantera; print(cantera.__version__)"
```

## 🎯 Quick Start

1. **Run the application**:
   ```bash
   python cantera_mixer_gui.py
   ```

2. **Load species**:
   - Default mechanisms are provided (`air.yaml` and `gri30.yaml`)
   - Click "📥 Load Species" button

3. **Configure streams**:
   - Set temperature, pressure, and composition for Stream A (Oxidizer)
   - Set temperature, pressure, and composition for Stream B (Fuel)

4. **Set flow rates**:
   - Enter mass flow rates for both streams (kg/s)

5. **Run simulation**:
   - Click "▶ Run Simulation"
   - View results in the tabs on the right panel

## 📖 Usage Guide

### Mechanism Files

The application uses Cantera mechanism files (YAML format):

- **Air Mechanism**: Contains species for air/oxidizer (default: `air.yaml`)
- **Fuel Mechanism**: Contains species for fuel mixture (default: `gri30.yaml`)

You can use any valid Cantera mechanism file, such as:
- `gri30.yaml` - GRI-Mech 3.0 (natural gas combustion)
- `air.yaml` - Air mixture definition
- Custom mechanism files

### Composition Format

Specify composition as comma-separated `SPECIES:FRACTION` pairs:
```
O2:0.21,N2:0.78,AR:0.01
CH4:0.9,C2H6:0.1
```

- Fractions should sum to 1.0
- Species names must exist in the loaded mechanism
- Case-sensitive species names

### Example Configurations

#### Methane-Air Combustion
- **Stream A (Air)**:
  - Temperature: 300 K
  - Pressure: 101325 Pa
  - Composition: `O2:0.21,N2:0.78,AR:0.01`
  - Mass Flow: 17.2 kg/s (stoichiometric)

- **Stream B (Fuel)**:
  - Temperature: 300 K
  - Pressure: 101325 Pa
  - Composition: `CH4:1`
  - Mass Flow: 1.0 kg/s

#### Hydrogen-Air Mixture
- **Stream A (Air)**:
  - Temperature: 400 K
  - Pressure: 202650 Pa
  - Composition: `O2:0.21,N2:0.79`
  - Mass Flow: 34.0 kg/s

- **Stream B (Fuel)**:
  - Temperature: 350 K
  - Pressure: 202650 Pa
  - Composition: `H2:1`
  - Mass Flow: 1.0 kg/s

## 🖥️ Interface Overview

### Left Panel - Controls
- **Header**: Application title and description
- **Mechanism Configuration**: Load mechanism files and species
- **Stream Configuration**: Set parameters for both input streams
- **Mass Flow Rates**: Specify flow rates
- **Available Species**: View loaded species list
- **Control Buttons**: Run simulation and clear results

### Right Panel - Results Tabs
- **📊 Text Results**: Detailed numerical output
- **🥧 Composition**: Pie chart of mixed gas composition
- **📈 Properties**: Bar chart comparison of stream properties
- **🔀 Flow Diagram**: Visual process flow representation

### Status Bar
- Real-time status updates
- Error and success messages
- Simulation progress indicators

## 📊 Visualization Features

### Composition Pie Chart
- Shows major species (>1% mole fraction)
- Color-coded segments with percentages
- Interactive legend and labels

### Properties Comparison
Compares across all streams:
- Temperature (K)
- Pressure (Pa)
- Density (kg/m³)
- Enthalpy (J/kg)
- Entropy (J/kg-K)

### Flow Diagram
- Visual representation of mixing process
- Shows stream properties and flow rates
- Color-coded for easy identification

### Interactive Plot Controls
All plots include matplotlib toolbar for:
- 🔍 Zoom and pan
- 💾 Save as image (PNG, SVG, PDF)
- 📏 Adjust plot dimensions
- ↩️ Reset view

## 🔧 Troubleshooting

### Common Issues

1. **"Species not found in mechanism"**
   - Verify species names match exactly (case-sensitive)
   - Check that species exist in loaded mechanism
   - Use the "Available Species" list as reference

2. **"Cannot load mechanism file"**
   - Ensure mechanism files are in the working directory
   - Check file permissions
   - Verify Cantera installation: `python -c "import cantera; print(cantera.__version__)"`

3. **"Composition fractions don't sum to 1"**
   - Verify all fractions sum to 1.0
   - Check for typos in species names
   - Ensure proper format: `SPECIES:FRACTION`

4. **GUI scaling issues**
   - Adjust window size manually
   - Minimum window size is set to 1000x700
   - Use scrollbars for smaller screens

### Performance Tips

- Load mechanism files once before multiple simulations
- Use smaller mechanism files for faster loading
- Reduce species list for quicker simulations

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**:
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**:
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Update documentation for new features
- Test with different mechanism files
- Ensure cross-platform compatibility

## 📝 Technical Details

### Architecture
- **Frontend**: Tkinter with ttk themed widgets
- **Visualization**: Matplotlib with TkAgg backend
- **Simulation Engine**: Cantera reactor network solver
- **Layout**: PanedWindow with scrollable frames

### Simulation Method
The application uses Cantera's reactor network approach:
1. Creates reservoirs for each input stream
2. Configures mass flow controllers
3. Solves steady-state using `ReactorNet.solve_steady()`
4. Extracts mixed stream properties

### Key Classes
- `CanteraMixerGUI`: Main application class
- Manages all UI components and event handling
- Interfaces with Cantera for simulation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Cantera](https://cantera.org/) - Open-source chemical kinetics library
- [Matplotlib](https://matplotlib.org/) - Python plotting library
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Python's standard GUI package

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check Cantera documentation: [https://cantera.org/documentation](https://cantera.org/documentation)
- Review example configurations in the Usage Guide

## 🗺️ Roadmap

Future enhancements planned:
- [ ] Save/Load simulation configurations
- [ ] Batch processing mode
- [ ] Additional property plots (Cp, viscosity, etc.)
- [ ] Export results to CSV/Excel
- [ ] Support for non-ideal gas models
- [ ] Sensitivity analysis tools
- [ ] Real-time parameter variation

---

**Built with ❤️ using Python, Cantera, and Matplotlib**
