import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time


# Simulate sensor network with progress updates
def generate_sensor_network(num_sensors=20, progress_callback=None):
    sensors = np.empty((num_sensors, 3))
    start_time = time.time()
    for i in range(num_sensors):
        # Simulate sensor generation (coordinates + energy)
        sensors[i, :2] = np.random.uniform(0, 100, 2)  # Random coordinates
        sensors[i, 2] = np.random.uniform(50, 100)  # Random residual energy

        # Update progress dynamically
        if progress_callback:
            elapsed = time.time() - start_time
            estimated_total_time = elapsed / (i + 1) * num_sensors
            remaining_time = estimated_total_time - elapsed
            progress_callback(i + 1, num_sensors, remaining_time)

        # Simulate a small delay to mimic real computation
        time.sleep(0.0001)  # Adjust this for better responsiveness
    return sensors


# Visualize network with simplified patterns
def visualize_network(sensors, base_station, cluster_heads):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot sensors without labels to reduce clutter
    ax.scatter(sensors[:, 0], sensors[:, 1], c='blue', label='Sensors', s=10, alpha=0.5)

    # Plot cluster heads as larger dots
    unique_ch = np.unique(cluster_heads)
    for ch in unique_ch:
        ax.scatter(sensors[ch, 0], sensors[ch, 1], c='red', s=50, edgecolor='black',
                   label='Cluster Head' if ch == unique_ch[0] else "")

    # Plot connections only for cluster heads to base station
    for ch in unique_ch:
        ax.plot([sensors[ch, 0], base_station[0]], [sensors[ch, 1], base_station[1]],
                'gray', linestyle='--', linewidth=1.5)

    # Plot base station
    ax.scatter(base_station[0], base_station[1], c='green', s=100, marker='X', label='Base Station')

    ax.set_title("Wireless Sensor Network Visualization")
    ax.set_xlabel("X-coordinate")
    ax.set_ylabel("Y-coordinate")
    ax.legend()
    ax.grid(True)
    return fig


# Progress callback
def update_progress(current, total, remaining_time):
    progress_var.set((current / total) * 100)  # Update progress bar
    minutes, seconds = divmod(int(remaining_time), 60)
    progress_label.config(text=f"Progress: {current}/{total} sensors")
    estimated_time_label.config(text=f"Estimated Finish Time: {minutes} min {seconds} sec")
    root.update_idletasks()  # Force GUI update dynamically


# Event to update visualization
def update_visualization():
    # Disable buttons while processing
    update_button.config(state=tk.DISABLED, bg="gray")
    end_button.config(state=tk.DISABLED, bg="gray")
    progress_var.set(0)
    progress_label.config(text="Progress: 0%")
    estimated_time_label.config(text="Estimated Finish Time: Calculating...")

    num_sensors = int(num_sensors_entry.get())
    base_station = np.array([50, 50])  # Fixed base station at the center

    # Generate sensors with progress callback
    sensors = generate_sensor_network(num_sensors, progress_callback=update_progress)

    # Simulate cluster head selection
    cluster_heads = np.random.randint(0, num_sensors, size=num_sensors)

    # Clear and redraw the plot
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    fig = visualize_network(sensors, base_station, cluster_heads)
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Re-enable buttons
    update_button.config(state=tk.NORMAL, bg="blue")
    end_button.config(state=tk.NORMAL, bg="red")
    progress_label.config(text="Done!")
    estimated_time_label.config(text="Job Completed!")


# End session (close the program)
def end_session():
    root.destroy()


# GUI Setup
root = tk.Tk()
root.title("Wireless Sensor Network GUI")

# GUI Layout
control_frame = ttk.Frame(root)
control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

canvas_frame = ttk.Frame(root)
canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Program Description
description_label = ttk.Label(
    control_frame,
    text=("This program simulates and visualizes a Wireless Sensor Network (WSN). \n"
          "Features:\n"
          "- Generate a network with a specified number of sensors.\n"
          "- Simulate cluster head selection and communication paths.\n"
          "- Estimate processing time for large networks.\n\n"
          "Use Cases:\n"
          "- Optimize sensor network design.\n"
          "- Analyze clustering and communication strategies.\n"
          "- Test real-world IoT and WSN configurations."),
    justify=tk.LEFT,
    wraplength=200
)
description_label.pack(pady=10)

# Control Panel
ttk.Label(control_frame, text="Number of Sensors:").pack(pady=5)
num_sensors_entry = ttk.Entry(control_frame)
num_sensors_entry.insert(0, "20")
num_sensors_entry.pack(pady=5)

update_button = tk.Button(control_frame, text="Update Visualization", command=update_visualization, bg="blue",
                          fg="white")
update_button.pack(pady=10)

end_button = tk.Button(control_frame, text="End Session", command=end_session, bg="red", fg="white")
end_button.pack(pady=10)

# Progress Bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(control_frame, variable=progress_var, maximum=100)
progress_bar.pack(fill=tk.X, pady=5)

progress_label = ttk.Label(control_frame, text="Progress: 0%")
progress_label.pack(pady=5)

estimated_time_label = ttk.Label(control_frame, text="Estimated Finish Time: N/A")
estimated_time_label.pack(pady=5)

# Author Info
author_label = ttk.Label(
    control_frame,
    text=("Author: Erick Wilfred\nEmail: erickwilfreddaniel@gmail.com\nPhone: +255753587561"),
    justify=tk.LEFT
)
author_label.pack(pady=20)

# Run the GUI
update_visualization()  # Initial visualization
root.mainloop()
