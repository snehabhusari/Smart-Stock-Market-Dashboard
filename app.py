from main import launch_ui
import os

if __name__ == "__main__":
   
    port = int(os.environ.get("PORT", 10000))
    launch_ui().launch(server_name="0.0.0.0", server_port=port)
