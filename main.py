import threaded_main
import Files.interface as interface
import time
import Files.overlayNEW as overlayNEW
import sys
import tkinter as tk
import threading
from PyQt5.QtWidgets import QApplication

# Flag to signal the background thread to terminate
terminate_event = threading.Event()


def background_task():
    while not terminate_event.is_set():
        # Perform background task
        time.sleep(1)
        threaded_main.main()
        time.sleep(1)

    print("Background task is stopped")

global overlay_app

def run_overlay_app():
    print("Running Overlay application...")
    global overlay_app
    overlay_app = overlayNEW.OverlayApp(screen_scaling=1)
    overlay_app.run()
    sys.exit(overlay_app.app.exec_())

def run_tkinter_app():

    print("Running Tkinter application...")

    # Setup and run the Tkinter application
    global root
    root = interface.interface()
    root.protocol("WM_DELETE_WINDOW", quit_application)
    root.mainloop()

def quit_application():
    global overlay_app

    # Signal the background thread to terminate
    terminate_event.set()

    # Close the overlay window
    if overlay_app:
        overlay_app.close_window()

    # Close Tkinter window
    if root:
        root.quit()
        root.destroy()

    sys.exit(0)
    
def main():
    # Thread for the background task
    background_thread = threading.Thread(target=background_task)
    background_thread.start()

    # Thread for the OverlayApp
    overlay_thread = threading.Thread(target=run_overlay_app)
    overlay_thread.start()

    # Run Tkinter app in the main thread
    run_tkinter_app()

    # Wait for threads to complete
    background_thread.join()
    overlay_thread.join()

if __name__ == "__main__":
    main()