import gradio as gr
from generate_analysis import run_analysis
import os

def launch_ui():
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="fuchsia"), title="📈 Sneha's Stock Dashboard") as demo:
        
        # --- Advanced CSS for Animations ---
        gr.HTML("""
        <style>
        .gradio-container { background: #0f172a !important; color: #ffffff !important; }
        
        /* Animated Marquee Heading */
        .marquee {
            width: 100%;
            overflow: hidden;
            white-space: nowrap;
            background: rgba(255, 255, 255, 0.05);
            padding: 10px 0;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .marquee h1 {
            display: inline-block;
            padding-left: 100%;
            animation: marquee 15s linear infinite;
            font-size: 30px;
            color: #ff6ec4;
            margin: 0;
        }
        @keyframes marquee {
            0% { transform: translate(0, 0); }
            100% { transform: translate(-100%, 0); }
        }

        /* Button hover animation */
        button:hover {
            transform: scale(1.05);
            transition: 0.3s ease-in-out;
            box-shadow: 0 0 15px #7873f5;
        }
        </style>
        """)

        # --- Animated Header Section ---
        gr.HTML("""
        <div class="marquee">
            <h1>📊 SNEHA: Smart Stock Portfolio Dashboard | Real-Time Market Analysis 📈</h1>
        </div>
        """)

        with gr.Tabs():
            with gr.TabItem("💹 Market Analysis"):
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

            with gr.TabItem("ℹ️ About"):
                gr.Markdown("""
                ### Welcome! 👋
                This dashboard provides real-time stock insights using Python, Gradio, and YFinance.
                - **Developer:** Sneha
                - **Core Features:** Technical Indicators, Price History, and Relative Analysis.
                """)

        # Visibility logic
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
