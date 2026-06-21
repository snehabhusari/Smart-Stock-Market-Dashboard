import gradio as gr
from generate_analysis import run_analysis
import os 

def launch_ui():
    # Use Soft theme with indigo primary color
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo"), title="📈 Sneha's Stock Dashboard") as demo:
        
        # Inject custom CSS for animations and styling
        gr.HTML("""
        <style>
        /* Modern Glassmorphism Container */
        .gradio-container { 
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important; 
            color: #ffffff !important;
        }

        /* Animated Heading with Glow Effect */
        .marquee-container {
            width: 100%;
            overflow: hidden;
            background: rgba(255, 255, 255, 0.1);
            padding: 15px 0;
            border-radius: 50px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
        }
        .marquee-text {
            display: inline-block;
            white-space: nowrap;
            animation: move-text 20s linear infinite;
            font-size: 28px;
            font-weight: bold;
            color: #fbbf24; /* Golden color for high visibility */
            text-shadow: 0 0 10px #fbbf24;
        }
        @keyframes move-text {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }

        /* Card and Button Styling */
        .gr-box { background: rgba(255, 255, 255, 0.05) !important; border-radius: 15px !important; }
        button { 
            background: linear-gradient(45deg, #4f46e5, #ec4899) !important;
            color: white !important;
            border: none !important;
            transition: all 0.4s ease !important;
        }
        button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px #ec4899;
        }
        </style>
        """)

        # Animated Header Display
        gr.HTML("""
        <div class="marquee-container">
            <div class="marquee-text">
                📊 SNEHA: SMART STOCK PORTFOLIO DASHBOARD | REAL-TIME ANALYSIS | LIVE MARKET UPDATES 📈
            </div>
        </div>
        """)

        with gr.Tabs():
            with gr.TabItem("💹 Market Analysis"):
                with gr.Row():
                    with gr.Column(scale=1):
                        ticker = gr.Textbox(label="Stock Symbol", value="RVNL", placeholder="e.g. RELIANCE.NS")
                        date_mode = gr.Radio(["Relative Period", "Custom Date Range"], value="Relative Period", label="Select Mode")
                        
                        # Input groups for date selection
                        with gr.Group() as period_group:
                            months = gr.Slider(1, 24, value=6, label="Period (Months)")
                        
                        with gr.Group(visible=False) as date_group:
                            start_date = gr.Textbox(label="Start Date (YYYY-MM-DD)", value="2023-01-01")
                            end_date = gr.Textbox(label="End Date (YYYY-MM-DD)", value="2023-12-31")
                        
                        plot_type = gr.Dropdown(["Price Only", "Price + MA", "RSI Only", "Price + MA + RSI"], value="Price + MA + RSI", label="Analysis Type")
                        run_btn = gr.Button("🚀 Generate Analysis")
                         run_btn.click(
            fn=run_analysis,
            inputs=[company, date_mode, months, start_date, end_date, plot_type],
            outputs=[output_plot, output_df]
                    
                    with gr.Column(scale=2):
                        output_plot = gr.Plot(label="Live Market Chart")
                        output_df = gr.Dataframe(label="Stock Data Preview")

           with gr.TabItem("ℹ️ About"):
    gr.HTML("""
    <div style="
        background: rgba(255, 255, 255, 0.05); 
        padding: 25px; 
        border-radius: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        color: #f1f5f9; /* Light white-ish text */
        backdrop-filter: blur(10px);
    ">
        <h3 style="color: #fbbf24; margin-bottom: 15px; font-weight: 500;">Welcome to your Financial Intelligence Hub! ✨</h3>
        <p style="font-size: 16px; line-height: 1.6; color: #e2e8f0;">
            This dashboard is professionally designed for real-time stock insights.
        </p>
        <ul style="margin-top: 15px; list-style-type: none; padding-left: 0;">
            <li style="margin-bottom: 8px;"><b>Developer:</b> <span style="color: #cbd5e1;">Sneha</span></li>
            <li style="margin-bottom: 8px;"><b>Tech Stack:</b> <span style="color: #cbd5e1;">Python, Gradio, YFinance</span></li>
            <li style="margin-bottom: 8px;"><b>Key Features:</b> <span style="color: #cbd5e1;">RSI, Moving Averages, Interactive Charts, and Live Market Data.</span></li>
        </ul>
    </div>
    """)

        # Visibility Logic to toggle between relative and custom dates
        def toggle(mode):
            return gr.update(visible=(mode == "Relative Period")), gr.update(visible=(mode == "Custom Date Range"))
        
        date_mode.change(toggle, inputs=[date_mode], outputs=[period_group, date_group])
        
        # Link button click to analysis function
        run_btn.click(
            fn=run_analysis,
            inputs=[ticker, date_mode, months, start_date, end_date, plot_type],
            outputs=[output_plot, output_df]
        )

    return demo

if __name__ == "__main__":
    # Use PORT environment variable provided by Render, default to 10000
    port = int(os.environ.get("PORT", 10000))
    launch_ui().launch(server_name="0.0.0.0", server_port=port)
