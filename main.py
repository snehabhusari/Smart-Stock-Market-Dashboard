import gradio as gr
from generate_analysis import run_analysis

def launch_ui():
    with gr.Blocks(title="📈 Stock Portfolio Dashboard") as demo:
        gr.Markdown("# 📊 ARTHA : Stock Portfolio Dashboard")

        # --- Input Section ---
        with gr.Row():
            ticker = gr.Textbox(label="Stock Symbol", placeholder="e.g., RVNL.NS", value="RVNL")

            date_mode = gr.Radio(
                choices=["Relative Period", "Custom Date Range"],
                value="Relative Period",
                label="Select Date Mode"
            )

        with gr.Row(visible=True) as relative_period_inputs:
            months = gr.Slider(1, 24, value=6, label="Period (in months)")

        with gr.Row(visible=False) as custom_date_inputs:
            start_date = gr.Textbox(label="Start Date (YYYY-MM-DD)", placeholder="2023-01-01")
            end_date = gr.Textbox(label="End Date (YYYY-MM-DD)", placeholder="2023-12-31")

        plot_type = gr.Dropdown(
            label="Plot Type",
            choices=["Price Only", "Price + MA", "RSI Only", "Price + MA + RSI"],
            value="Price + MA + RSI"
        )

        run_btn = gr.Button("Analyze")

        # --- Output Section ---
        output_plot = gr.Plot()
        output_df = gr.Dataframe()

        # --- Dynamic Display Logic ---
        def toggle_inputs(mode):
            return (
                gr.update(visible=(mode == "Relative Period")),
                gr.update(visible=(mode == "Custom Date Range"))
            )

        date_mode.change(fn=toggle_inputs, inputs=[date_mode], outputs=[relative_period_inputs, custom_date_inputs])

        # --- Run Analysis ---
        run_btn.click(
            fn=run_analysis,
            inputs=[ticker, date_mode, months, start_date, end_date, plot_type],
            outputs=[output_plot, output_df]
        )

    return demo

