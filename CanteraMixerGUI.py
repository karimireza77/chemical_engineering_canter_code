import tkinter as tk
from tkinter import ttk, messagebox
import cantera as ct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np


class CanteraMixerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cantera Stream Mixer")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configure styles
        self.setup_styles()
        
        # Track simulation state
        self.species_loaded = False
        self.simulation_data = None
        
        self.create_widgets()
        self.setup_bindings()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.colors = {
            'bg': '#f0f0f0',
            'fg': '#333333',
            'accent': '#0078d4',
            'success': '#107c10',
            'error': '#d13438',
            'warning': '#ff8c00',
            'border': '#d1d1d1',
            'stream_a': '#2196F3',
            'stream_b': '#FF5722',
            'mixed': '#4CAF50'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Frame styles
        style.configure(
            'Title.TLabelframe',
            background=self.colors['bg'],
            foreground=self.colors['fg'],
            font=('Segoe UI', 10, 'bold')
        )
        style.configure(
            'Title.TLabelframe.Label',
            background=self.colors['bg'],
            foreground=self.colors['accent'],
            font=('Segoe UI', 11, 'bold')
        )
        
        # Button styles
        style.configure(
            'Primary.TButton',
            background=self.colors['accent'],
            foreground='white',
            font=('Segoe UI', 10, 'bold'),
            padding=(20, 8)
        )
        style.map(
            'Primary.TButton',
            background=[('active', '#106ebe'), ('disabled', '#cccccc')],
            foreground=[('disabled', '#666666')]
        )
        
        # Entry styles
        style.configure(
            'TEntry',
            padding=5,
            font=('Segoe UI', 9)
        )
        
        # Notebook (tab) style
        style.configure(
            'TNotebook',
            background=self.colors['bg']
        )
        style.configure(
            'TNotebook.Tab',
            padding=[10, 5],
            font=('Segoe UI', 9)
        )

    def create_widgets(self):
        # Create main container with paned window for resizable sections
        main_paned = ttk.PanedWindow(self.root, orient='horizontal')
        main_paned.pack(fill='both', expand=True)
        
        # Left panel - Controls
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # Right panel - Results and plots
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)
        
        # Setup scrollable left panel
        self.setup_left_panel(left_frame)
        
        # Setup right panel with tabs
        self.setup_right_panel(right_frame)
        
        # Status Bar
        self.create_status_bar()

    def setup_left_panel(self, parent):
        # Create canvas and scrollbar for left panel
        canvas = tk.Canvas(parent, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        
        self.left_scrollable_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        canvas_window = canvas.create_window((0, 0), window=self.left_scrollable_frame, anchor="nw")
        
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        self.left_scrollable_frame.bind("<Configure>", configure_scroll_region)
        
        def configure_canvas_window(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", configure_canvas_window)
        
        # Create all control sections
        self.create_header()
        self.create_mechanism_section()
        self.create_stream_section()
        self.create_flow_section()
        self.create_species_section()
        self.create_control_section()

    def setup_right_panel(self, parent):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True)
        
        # Text results tab
        self.text_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.text_frame, text='📊 Text Results')
        self.create_text_results_tab()
        
        # Composition plot tab
        self.comp_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.comp_frame, text='🥧 Composition')
        self.create_composition_tab()
        
        # Properties comparison tab
        self.props_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.props_frame, text='📈 Properties')
        self.create_properties_tab()
        
        # Flow diagram tab
        self.flow_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.flow_frame, text='🔀 Flow Diagram')
        self.create_flow_diagram_tab()

    def create_text_results_tab(self):
        # Result text with scrollbar
        result_container = ttk.Frame(self.text_frame)
        result_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.result_box = tk.Text(
            result_container,
            wrap='none',
            font=('Consolas', 10),
            bg='white',
            fg=self.colors['fg'],
            relief='solid',
            borderwidth=1
        )
        
        result_v_scrollbar = ttk.Scrollbar(
            result_container,
            orient='vertical',
            command=self.result_box.yview
        )
        result_h_scrollbar = ttk.Scrollbar(
            result_container,
            orient='horizontal',
            command=self.result_box.xview
        )
        
        self.result_box.configure(
            yscrollcommand=result_v_scrollbar.set,
            xscrollcommand=result_h_scrollbar.set
        )
        
        self.result_box.grid(row=0, column=0, sticky='nsew')
        result_v_scrollbar.grid(row=0, column=1, sticky='ns')
        result_h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        result_container.grid_rowconfigure(0, weight=1)
        result_container.grid_columnconfigure(0, weight=1)

    def create_composition_tab(self):
        self.comp_figure = Figure(figsize=(6, 4), dpi=100)
        self.comp_canvas = FigureCanvasTkAgg(self.comp_figure, self.comp_frame)
        self.comp_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.comp_canvas, self.comp_frame)
        toolbar.update()
        toolbar.pack()

    def create_properties_tab(self):
        self.props_figure = Figure(figsize=(6, 4), dpi=100)
        self.props_canvas = FigureCanvasTkAgg(self.props_figure, self.props_frame)
        self.props_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.props_canvas, self.props_frame)
        toolbar.update()
        toolbar.pack()

    def create_flow_diagram_tab(self):
        self.flow_figure = Figure(figsize=(6, 4), dpi=100)
        self.flow_canvas = FigureCanvasTkAgg(self.flow_figure, self.flow_frame)
        self.flow_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.flow_canvas, self.flow_frame)
        toolbar.update()
        toolbar.pack()

    def create_header(self):
        header_frame = ttk.Frame(self.left_scrollable_frame)
        
        title_label = ttk.Label(
            header_frame,
            text="🔬 Cantera Stream Mixer",
            font=('Segoe UI', 16, 'bold'),
            foreground=self.colors['accent']
        )
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Configure and simulate gas stream mixing",
            font=('Segoe UI', 9),
            foreground='#666666'
        )
        
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        title_label.pack(anchor='w')
        subtitle_label.pack(anchor='w', pady=(5, 0))

    def create_mechanism_section(self):
        mech_frame = ttk.LabelFrame(
            self.left_scrollable_frame,
            text="🔧 Mechanism Configuration",
            style='Title.TLabelframe',
            padding=15
        )
        mech_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        mech_frame.columnconfigure(1, weight=1)
        
        ttk.Label(
            mech_frame,
            text="Air Mechanism:",
            font=('Segoe UI', 9, 'bold')
        ).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        self.air_mech = ttk.Entry(mech_frame, width=40)
        self.air_mech.insert(0, "air.yaml")
        self.air_mech.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=(0, 5))
        
        ttk.Label(
            mech_frame,
            text="Fuel Mechanism:",
            font=('Segoe UI', 9, 'bold')
        ).grid(row=1, column=0, sticky='w', pady=(0, 5))
        
        self.fuel_mech = ttk.Entry(mech_frame, width=40)
        self.fuel_mech.insert(0, "gri30.yaml")
        self.fuel_mech.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=(0, 5))
        
        button_frame = ttk.Frame(mech_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky='w')
        
        self.load_btn = ttk.Button(
            button_frame,
            text="📥 Load Species",
            style='Primary.TButton',
            command=self.load_species
        )
        self.load_btn.pack(side='left')
        
        self.loading_label = ttk.Label(
            button_frame,
            text="  Loading...",
            font=('Segoe UI', 9, 'italic'),
            foreground=self.colors['warning']
        )

    def create_stream_section(self):
        streams_frame = ttk.Frame(self.left_scrollable_frame)
        streams_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        stream_a = ttk.LabelFrame(
            streams_frame,
            text="📥 Stream A (Oxidizer)",
            style='Title.TLabelframe',
            padding=15
        )
        stream_a.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        self.create_stream_inputs(stream_a, 'a')
        
        stream_b = ttk.LabelFrame(
            streams_frame,
            text="📤 Stream B (Fuel)",
            style='Title.TLabelframe',
            padding=15
        )
        stream_b.pack(side='left', fill='both', expand=True, padx=(5, 0))
        
        self.create_stream_inputs(stream_b, 'b')

    def create_stream_inputs(self, parent, stream_id):
        ttk.Label(
            parent,
            text="Temperature (K):",
            font=('Segoe UI', 9)
        ).pack(anchor='w', pady=(0, 3))
        
        temp_var = tk.DoubleVar(value=300)
        setattr(self, f'temp_{stream_id}', temp_var)
        
        temp_entry = ttk.Entry(parent, textvariable=temp_var, width=20)
        temp_entry.pack(fill='x', pady=(0, 10))
        
        ttk.Label(
            parent,
            text="Pressure (Pa):",
            font=('Segoe UI', 9)
        ).pack(anchor='w', pady=(0, 3))
        
        pres_var = tk.DoubleVar(value=ct.one_atm)
        setattr(self, f'pres_{stream_id}', pres_var)
        
        pres_entry = ttk.Entry(parent, textvariable=pres_var, width=20)
        pres_entry.pack(fill='x', pady=(0, 10))
        
        ttk.Label(
            parent,
            text="Composition:",
            font=('Segoe UI', 9)
        ).pack(anchor='w', pady=(0, 3))
        
        comp_entry = ttk.Entry(parent, width=30)
        comp_entry.pack(fill='x', pady=(0, 5))
        setattr(self, f'comp_{stream_id}', comp_entry)
        
        if stream_id == 'a':
            comp_entry.insert(0, "O2:0.21,N2:0.78,AR:0.01")
        else:
            comp_entry.insert(0, "CH4:1")
        
        ttk.Label(
            parent,
            text="Format: SPECIES:FRACTION,...",
            font=('Segoe UI', 7),
            foreground='#888888',
            wraplength=250
        ).pack(anchor='w')

    def create_flow_section(self):
        flow_frame = ttk.LabelFrame(
            self.left_scrollable_frame,
            text="⚡ Mass Flow Rates",
            style='Title.TLabelframe',
            padding=15
        )
        flow_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        flow_grid = ttk.Frame(flow_frame)
        flow_grid.pack(fill='x')
        
        ttk.Label(
            flow_grid,
            text="Stream A (Oxidizer):",
            font=('Segoe UI', 9, 'bold')
        ).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        self.mdot_air = tk.DoubleVar(value=1.0)
        ttk.Entry(
            flow_grid,
            textvariable=self.mdot_air,
            width=20
        ).grid(row=0, column=1, padx=(10, 5), pady=(0, 5))
        
        ttk.Label(
            flow_grid,
            text="kg/s",
            font=('Segoe UI', 9)
        ).grid(row=0, column=2, sticky='w', pady=(0, 5))
        
        ttk.Label(
            flow_grid,
            text="Stream B (Fuel):",
            font=('Segoe UI', 9, 'bold')
        ).grid(row=1, column=0, sticky='w')
        
        self.mdot_fuel = tk.DoubleVar(value=1.0)
        ttk.Entry(
            flow_grid,
            textvariable=self.mdot_fuel,
            width=20
        ).grid(row=1, column=1, padx=(10, 5))
        
        ttk.Label(
            flow_grid,
            text="kg/s",
            font=('Segoe UI', 9)
        ).grid(row=1, column=2, sticky='w')

    def create_species_section(self):
        species_frame = ttk.LabelFrame(
            self.left_scrollable_frame,
            text="🧪 Available Species",
            style='Title.TLabelframe',
            padding=15
        )
        species_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        species_container = ttk.Frame(species_frame)
        species_container.pack(fill='both', expand=True)
        
        self.species_box = tk.Text(
            species_container,
            height=6,
            wrap='word',
            font=('Consolas', 9),
            bg='white',
            fg=self.colors['fg'],
            relief='solid',
            borderwidth=1
        )
        species_scrollbar = ttk.Scrollbar(
            species_container,
            orient='vertical',
            command=self.species_box.yview
        )
        self.species_box.configure(yscrollcommand=species_scrollbar.set)
        
        self.species_box.pack(side='left', fill='both', expand=True)
        species_scrollbar.pack(side='right', fill='y')
        
        self.species_count_label = ttk.Label(
            species_frame,
            text="No species loaded",
            font=('Segoe UI', 8),
            foreground='#888888'
        )
        self.species_count_label.pack(anchor='w', pady=(5, 0))

    def create_control_section(self):
        control_frame = ttk.Frame(self.left_scrollable_frame)
        control_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        self.run_btn = ttk.Button(
            control_frame,
            text="▶ Run Simulation",
            style='Primary.TButton',
            command=self.run_simulation,
            state='disabled'
        )
        self.run_btn.pack(side='left', padx=(0, 10))
        
        self.clear_btn = ttk.Button(
            control_frame,
            text="🗑 Clear Results",
            command=self.clear_results
        )
        self.clear_btn.pack(side='left')
        
        self.progress = ttk.Progressbar(
            control_frame,
            mode='indeterminate',
            length=200
        )

    def create_status_bar(self):
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side='bottom', fill='x')
        
        self.status_label = ttk.Label(
            status_frame,
            text="Ready",
            font=('Segoe UI', 8),
            relief='sunken',
            padding=(5, 2)
        )
        self.status_label.pack(fill='x')

    def setup_bindings(self):
        def bind_mousewheel(event):
            self.root.bind_all("<MouseWheel>", self._on_mousewheel_all)
        
        def unbind_mousewheel(event):
            self.root.unbind_all("<MouseWheel>")
        
        self.left_scrollable_frame.bind("<Enter>", bind_mousewheel)
        self.left_scrollable_frame.bind("<Leave>", unbind_mousewheel)

    def _on_mousewheel_all(self, event):
        self.root.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def load_species(self):
        self.status_label.config(text="Loading species...")
        self.load_btn.config(state='disabled')
        self.loading_label.pack(side='left', padx=(10, 0))
        self.root.update()
        
        try:
            gas = ct.Solution(self.fuel_mech.get())
            species_list = sorted(gas.species_names)
            
            self.species_box.delete("1.0", tk.END)
            
            for i, sp in enumerate(species_list, 1):
                self.species_box.insert(tk.END, f"{sp:30}")
                if i % 3 == 0:
                    self.species_box.insert(tk.END, "\n")
            
            species_count = len(species_list)
            self.species_count_label.config(
                text=f"✅ {species_count} species loaded successfully"
            )
            self.species_loaded = True
            self.run_btn.config(state='normal')
            self.status_label.config(text=f"Loaded {species_count} species")
            
        except Exception as e:
            self.species_count_label.config(
                text=f"❌ Error: {str(e)[:100]}...",
                foreground=self.colors['error']
            )
            self.status_label.config(text="Error loading species")
            messagebox.showerror(
                "Load Error",
                f"Failed to load species:\n{str(e)}"
            )
        finally:
            self.load_btn.config(state='normal')
            self.loading_label.pack_forget()

    def validate_species(self, gas, composition):
        available = set(gas.species_names)
        missing_species = []
        
        for item in composition.split(","):
            if not item.strip():
                continue
            try:
                species = item.split(":")[0].strip()
                if species not in available:
                    missing_species.append(species)
            except:
                raise ValueError(f"Invalid composition format: '{item}'")
        
        if missing_species:
            raise ValueError(
                f"Species not found in mechanism: {', '.join(missing_species)}"
            )
        
        return True

    def clear_results(self):
        self.result_box.delete("1.0", tk.END)
        self.simulation_data = None
        self.clear_all_plots()
        self.status_label.config(text="Results cleared")

    def clear_all_plots(self):
        """Clear all plot figures"""
        for fig in [self.comp_figure, self.props_figure, self.flow_figure]:
            fig.clear()
        
        for canvas in [self.comp_canvas, self.props_canvas, self.flow_canvas]:
            canvas.draw()

    def plot_composition(self, gas_mixed):
        """Create pie chart of mixed gas composition"""
        self.comp_figure.clear()
        
        # Get major species (>1% mole fraction)
        mole_fractions = gas_mixed.X
        species_names = gas_mixed.species_names
        
        # Filter and sort species by mole fraction
        major_indices = np.where(mole_fractions > 0.01)[0]
        other_fraction = 1 - np.sum(mole_fractions[major_indices])
        
        labels = [species_names[i] for i in major_indices]
        sizes = [mole_fractions[i] * 100 for i in major_indices]
        
        if other_fraction > 0.01:
            labels.append('Others')
            sizes.append(other_fraction * 100)
        
        # Create pie chart
        ax = self.comp_figure.add_subplot(111)
        colors = plt.cm.Set3(np.linspace(0, 1, len(sizes)))
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        
        # Style the pie chart
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title('Mixed Gas Composition (Mole Fractions)', fontweight='bold', pad=20)
        
        self.comp_figure.tight_layout()
        self.comp_canvas.draw()

    def plot_properties_comparison(self, gas_a, gas_b, gas_mixed):
        """Create bar charts comparing properties of streams"""
        self.props_figure.clear()
        
        # Properties to compare
        properties = ['Temperature (K)', 'Pressure (Pa)', 'Density (kg/m³)', 
                     'Enthalpy (J/kg)', 'Entropy (J/kg-K)']
        
        values_a = [gas_a.T, gas_a.P, gas_a.density, gas_a.h, gas_a.s]
        values_b = [gas_b.T, gas_b.P, gas_b.density, gas_b.h, gas_b.s]
        values_mixed = [gas_mixed.T, gas_mixed.P, gas_mixed.density, 
                       gas_mixed.h, gas_mixed.s]
        
        # Create subplots
        for i, (prop, val_a, val_b, val_mixed) in enumerate(
            zip(properties, values_a, values_b, values_mixed), 1):
            
            ax = self.props_figure.add_subplot(2, 3, i)
            
            bars = ax.bar(
                ['Stream A', 'Stream B', 'Mixed'],
                [val_a, val_b, val_mixed],
                color=[self.colors['stream_a'], self.colors['stream_b'], 
                      self.colors['mixed']]
            )
            
            # Add value labels on bars
            for bar, val in zip(bars, [val_a, val_b, val_mixed]):
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2., 
                    height,
                    f'{val:.2e}',
                    ha='center', 
                    va='bottom',
                    fontsize=7,
                    rotation=45
                )
            
            ax.set_title(prop, fontsize=9)
            ax.tick_params(axis='x', rotation=45, labelsize=7)
            ax.tick_params(axis='y', labelsize=7)
            ax.grid(axis='y', alpha=0.3)
        
        self.props_figure.suptitle('Stream Properties Comparison', fontweight='bold', fontsize=12)
        self.props_figure.tight_layout()
        self.props_canvas.draw()

    def plot_flow_diagram(self):
        """Create a simple flow diagram of the mixing process"""
        self.flow_figure.clear()
        
        ax = self.flow_figure.add_subplot(111)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis('off')
        
        # Stream A box
        box_a = plt.Rectangle((1, 3), 2, 1.5, fill=True, 
                              facecolor=self.colors['stream_a'], alpha=0.3,
                              edgecolor=self.colors['stream_a'], linewidth=2)
        ax.add_patch(box_a)
        ax.text(2, 4.2, 'Stream A\n(Oxidizer)', ha='center', va='center', 
               fontweight='bold', fontsize=10)
        ax.text(2, 3.5, f'{self.mdot_air.get():.2f} kg/s', ha='center', 
               va='center', fontsize=9)
        ax.text(2, 3.2, f'{self.temp_a.get():.0f} K', ha='center', 
               va='center', fontsize=8, color='gray')
        
        # Stream B box
        box_b = plt.Rectangle((1, 1), 2, 1.5, fill=True,
                              facecolor=self.colors['stream_b'], alpha=0.3,
                              edgecolor=self.colors['stream_b'], linewidth=2)
        ax.add_patch(box_b)
        ax.text(2, 2.2, 'Stream B\n(Fuel)', ha='center', va='center',
               fontweight='bold', fontsize=10)
        ax.text(2, 1.5, f'{self.mdot_fuel.get():.2f} kg/s', ha='center',
               va='center', fontsize=9)
        ax.text(2, 1.2, f'{self.temp_b.get():.0f} K', ha='center',
               va='center', fontsize=8, color='gray')
        
        # Mixer
        mixer_circle = plt.Circle((5.5, 2.5), 0.8, fill=True,
                                 facecolor='lightgray', alpha=0.5,
                                 edgecolor='black', linewidth=2)
        ax.add_patch(mixer_circle)
        ax.text(5.5, 2.5, 'MIXER', ha='center', va='center',
               fontweight='bold', fontsize=10)
        
        # Mixed output box
        box_mixed = plt.Rectangle((7.5, 2), 2, 1.5, fill=True,
                                  facecolor=self.colors['mixed'], alpha=0.3,
                                  edgecolor=self.colors['mixed'], linewidth=2)
        ax.add_patch(box_mixed)
        ax.text(8.5, 3.2, 'Mixed\nOutput', ha='center', va='center',
               fontweight='bold', fontsize=10)
        
        if self.simulation_data:
            ax.text(8.5, 2.5, f'{self.simulation_data["mixed_temp"]:.0f} K',
                   ha='center', va='center', fontsize=9)
        
        # Arrows
        ax.annotate('', xy=(4.7, 3.75), xytext=(3, 3.75),
                   arrowprops=dict(arrowstyle='->', lw=2, color=self.colors['stream_a']))
        ax.annotate('', xy=(4.7, 1.75), xytext=(3, 1.75),
                   arrowprops=dict(arrowstyle='->', lw=2, color=self.colors['stream_b']))
        ax.annotate('', xy=(7.5, 3), xytext=(6.3, 2.5),
                   arrowprops=dict(arrowstyle='->', lw=2, color=self.colors['mixed']))
        
        ax.set_title('Mixing Process Flow Diagram', fontweight='bold', fontsize=12, pad=20)
        
        self.flow_figure.tight_layout()
        self.flow_canvas.draw()

    def run_simulation(self):
        if not self.species_loaded:
            messagebox.showwarning("Warning", "Please load species first.")
            return
        
        self.status_label.config(text="Running simulation...")
        self.run_btn.config(state='disabled')
        self.progress.pack(side='left', padx=(10, 0))
        self.progress.start()
        self.root.update()
        
        try:
            # Validate inputs
            gas_a = ct.Solution(self.air_mech.get())
            gas_b = ct.Solution(self.fuel_mech.get())
            
            self.validate_species(gas_a, self.comp_a.get())
            self.validate_species(gas_b, self.comp_b.get())
            
            # Set states
            gas_a.TPX = (
                self.temp_a.get(),
                self.pres_a.get(),
                self.comp_a.get()
            )
            gas_b.TPX = (
                self.temp_b.get(),
                self.pres_b.get(),
                self.comp_b.get()
            )
            
            # Create reactor network
            res_a = ct.Reservoir(gas_a)
            res_b = ct.Reservoir(gas_b)
            mixer = ct.IdealGasReactor(gas_b)
            downstream = ct.Reservoir(gas_b)
            
            ct.MassFlowController(res_a, mixer, mdot=self.mdot_air.get())
            ct.MassFlowController(res_b, mixer, mdot=self.mdot_fuel.get())
            ct.Valve(mixer, downstream, K=10.0)
            
            # Solve
            sim = ct.ReactorNet([mixer])
            sim.solve_steady()
            
            # Store simulation data
            self.simulation_data = {
                'gas_a': gas_a,
                'gas_b': gas_b,
                'gas_mixed': mixer.phase,
                'mixed_temp': mixer.T,
                'mixed_pres': mixer.phase.P,
                'mass_flow_total': self.mdot_air.get() + self.mdot_fuel.get()
            }
            
            # Update text results
            self.update_text_results()
            
            # Generate plots
            self.plot_composition(mixer.phase)
            self.plot_properties_comparison(gas_a, gas_b, mixer.phase)
            self.plot_flow_diagram()
            
            self.status_label.config(
                text=f"Simulation completed - Mixed temperature: {mixer.T:.1f} K"
            )
            
            # Switch to composition tab
            self.notebook.select(1)
            
        except Exception as e:
            self.status_label.config(text="Simulation failed")
            messagebox.showerror(
                "Simulation Error",
                f"An error occurred:\n{str(e)}"
            )
        finally:
            self.run_btn.config(state='normal')
            self.progress.stop()
            self.progress.pack_forget()

    def update_text_results(self):
        """Update the text results tab"""
        data = self.simulation_data
        
        self.result_box.delete("1.0", tk.END)
        
        self.result_box.insert(tk.END, "="*60 + "\n")
        self.result_box.insert(tk.END, "SIMULATION RESULTS\n")
        self.result_box.insert(tk.END, "="*60 + "\n\n")
        
        # Stream summary
        self.result_box.insert(tk.END, "Input Streams:\n")
        self.result_box.insert(tk.END, "-"*40 + "\n")
        self.result_box.insert(
            tk.END,
            f"Stream A (Oxidizer): {self.mdot_air.get():.3f} kg/s at {self.temp_a.get():.1f} K, "
            f"{self.pres_a.get()/101325:.3f} atm\n"
        )
        self.result_box.insert(
            tk.END,
            f"Stream B (Fuel): {self.mdot_fuel.get():.3f} kg/s at {self.temp_b.get():.1f} K, "
            f"{self.pres_b.get()/101325:.3f} atm\n\n"
        )
        
        # Mixed properties
        self.result_box.insert(tk.END, "Mixed Stream Properties:\n")
        self.result_box.insert(tk.END, "-"*40 + "\n")
        self.result_box.insert(
            tk.END,
            f"Temperature: {data['mixed_temp']:.2f} K\n"
        )
        self.result_box.insert(
            tk.END,
            f"Pressure: {data['mixed_pres']/101325:.3f} atm ({data['mixed_pres']:.1f} Pa)\n"
        )
        self.result_box.insert(
            tk.END,
            f"Total Mass Flow: {data['mass_flow_total']:.3f} kg/s\n"
        )
        self.result_box.insert(
            tk.END,
            f"Density: {data['gas_mixed'].density:.4f} kg/m³\n\n"
        )
        
        # Detailed report
        self.result_box.insert(tk.END, "Detailed Cantera Report:\n")
        self.result_box.insert(tk.END, "-"*40 + "\n")
        self.result_box.insert(tk.END, data['gas_mixed'].report())


if __name__ == "__main__":
    root = tk.Tk()
    app = CanteraMixerGUI(root)
    root.mainloop()