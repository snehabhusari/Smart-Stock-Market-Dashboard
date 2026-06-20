import gradio as gr
from generate_analysis import run_analysis
import os

def launch_ui():
    # Gradio की Soft Theme का उपयोग करें जो बहुत क्लीन लगती है
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="fuchsia"), title="📈 Sneha's Stock Dashboard") as demo:
        
        # --- Custom CSS for High-End Animation ---
        gr.HTML("""
        <style>
        .gradio-container { background: #0f172a !important; }
        h1 { 
            text-align: center; 
            color: #ffffff; 
            font-size: 40px; 
            margin-bottom: 20px;
            background: -webkit-linear-gradient(#ff6ec4, #7873f5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: pulse 2s infinite;
        }
        @keyframes pulse { 0% { opacity: 0.8; } 50% { opacity: 1; } 100% { opacity: 0.8; } }
        .tab-button { font-weight: bold !important; }
        </style>
        """)

        gr.HTML("<h1>📊 SNEHA: Smart Stock Portfolio Dashboard</h1>")

        with gr.Tabs():
            with gr.TabItem("💹 Market Analysis", elem_classes="tab-button"):
                with gr.Row():
                    with gr.Column(scale=1):
                        ticker = gr.Textbox(label="Stock Symbol", value="RVNL", placeholder="e.g. RELIANCE.NS")
                        date_mode = gr.Radio(["Relative Period", "Custom Date Range"], value="Relative Period", label="Select Mode")
                        
                        with gr.Group() as period_group:
                            months = gr.Slider(1, 24, value=6, label="Period (Months)")
                        
                        with gr.Group(visible=False) as date_group:
                            start_date = gr.Textbox(label="Start Date (YYYY-MM-DD)", value="2023-01-01")
                            end_date = gr.Textbox(label="End Date (YYYY-MM-DD)", value="2023-12-31")
                        
                        plot_type = gr.Dropdown(["Price Only", "Price + MA", "RSI Only", "Price + MA + RSI"], value="Price + MA + RSI", label="Analysis Type")
                        run_btn = gr.Button("🚀 Generate Analysis", variant="primary")
                    
                    with gr.Column(scale=2):
                        output_plot = gr.Plot(label="Live Market Chart")
                        output_df = gr.Dataframe(label="Stock Data Preview")

            with gr.TabItem("ℹ️ About", elem_classes="tab-button"):
                gr.Markdown("""
                ### Welcome to your Personal Finance Hub! ✨
                - **Built by:** Sneha
                - **Features:** Real-time stock data analysis, RSI calculation, and Moving Averages.
                - **Technology:** Python, Gradio, YFinance.
                """)

        # Logic for hiding/showing fields
        def toggle(mode):
            return gr.update(visible=(mode == "Relative Period")), gr.update(visible=(mode == "Custom Date Range"))
        
        date_mode.change(toggle, inputs=[date_mode], outputs=[period_group, date_group])
        
        run_btn.click(
            fn=run_analysis,
            inputs=[ticker, date_mode, months, start_date, end_date, plot_type],
            outputs=[output_plot, output_df]
        )

    return demo

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    launch_ui().launch(server_name="0.0.0.0", server_port=port)
