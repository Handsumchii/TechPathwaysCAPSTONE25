from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import or define generate_charts function
def generate_charts():
    # Placeholder: Replace with actual chart generation logic
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    ax.set_title("Sample Chart")
    return [fig]


def show_charts(self):
    print("[UI] Attempting to generate charts...")
    for canvas in self.chart_canvases:
        canvas.get_tk_widget().destroy()
    self.chart_canvases.clear()

    charts = generate_charts()
    print(f"[UI] {len(charts)} charts returned.")

    if not charts:
        print("[UI] No charts generated.")
        return

    for fig in charts:
        canvas = FigureCanvasTkAgg(fig, master=self.charts_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=5)
        self.chart_canvases.append(canvas)






