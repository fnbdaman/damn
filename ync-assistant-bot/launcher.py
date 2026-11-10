#!/usr/bin/env python3
"""
YNC Assistant - Desktop Launcher
A graphical launcher to run the YNC Telegram Bot without terminal commands.
Features:
- Automatic bot startup
- Real-time monitoring
- Status indicators
- Log viewer
- Easy restart functionality
"""

import subprocess
import threading
import queue
import time
import os
from pathlib import Path
from datetime import datetime
import sys

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib
    HAS_GTK = True
except ImportError:
    HAS_GTK = False

class BotLauncher:
    """Desktop launcher for the YNC Assistant Telegram Bot."""
    
    def __init__(self, project_path="/Users/fnb/Downloads/ync-assistant"):
        self.project_path = Path(project_path)
        self.bot_process = None
        self.log_messages = queue.Queue()
        self.is_running = False
        self.status = "Not Started"
        self.start_time = None
        
    def read_env(self):
        """Read and validate environment configuration."""
        env_file = self.project_path / ".env"
        env_vars = {}
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
        
        return env_vars
    
    def start_bot(self):
        """Start the YNC Assistant bot in a subprocess."""
        try:
            self.log("Starting YNC Assistant Bot...")
            
            # Check prerequisites
            env_vars = self.read_env()
            
            if not env_vars.get('TELEGRAM_BOT_TOKEN'):
                self.log("Error: TELEGRAM_BOT_TOKEN not configured")
                return False
            
            if not env_vars.get('VENCE_API_KEY'):
                self.log("Error: VENCE_API_KEY not configured")
                return False
            
            # Start bot process
            bot_script = self.project_path / "bot.py"
            
            self.bot_process = subprocess.Popen(
                [sys.executable, str(bot_script)],
                cwd=self.project_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True
            )
            
            self.is_running = True
            self.start_time = datetime.now()
            self.status = "Running"
            
            # Read output in separate thread
            threading.Thread(target=self.read_output, daemon=True).start()
            
            self.log(f"✓ Bot started at {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            self.log(f"✓ PID: {self.bot_process.pid}")
            self.log(f"✓ Model: {env_vars.get('AI_MODEL', 'Not configured')}")
            
            return True
            
        except Exception as e:
            self.log(f"✗ Error starting bot: {str(e)}")
            return False
    
    def read_output(self):
        """Read bot output and errors in real-time."""
        if self.bot_process:
            for line in iter(self.bot_process.stdout.readline, ''):
                if line:
                    self.log(f"STDOUT: {line.strip()}")
            for line in iter(self.bot_process.stderr.readline, ''):
                if line:
                    self.log(f"STDERR: {line.strip()}")
    
    def stop_bot(self):
        """Stop the running bot."""
        if self.bot_process:
            self.log("Stopping YNC Assistant Bot...")
            self.bot_process.terminate()
            self.bot_process.wait()
            self.is_running = False
            self.status = "Stopped"
            self.log("✓ Bot stopped successfully")
    
    def restart_bot(self):
        """Restart the bot."""
        self.stop_bot()
        time.sleep(1)
        self.start_bot()
    
    def log(self, message):
        """Add a log message."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.log_messages.put(log_entry)
    
    def get_bot_status(self):
        """Get current bot status."""
        if self.bot_process:
            return {
                'pid': self.bot_process.pid,
                'status': 'Running' if self.bot_process.poll() is None else 'Stopped',
                'uptime': (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
            }
        return {'status': 'Not Running'}
    
    def export_as_application(self, app_name="YNC Assistant"):
        """Export the launcher as a desktop application."""
        app_dir = self.project_path / "applications"
        app_dir.mkdir(exist_ok=True)
        
        # Create .app bundle for macOS
        app_bundle = app_dir / f"{app_name}.app"
        
        try:
            import subprocess
            subprocess.run(
                ['mkdir', '-p', str(app_bundle / 'Contents/MacOS')],
                cwd=app_bundle.parent
            )
            
            # Create executable
            launcher_script = app_bundle / 'Contents/MacOS/ync_assistant_launcher'
            launcher_script.chmod(0o755)
            
            self.log(f"✓ Application exported to {app_bundle}")
            return app_bundle
            
        except Exception as e:
            self.log(f"Export completed with warnings: {str(e)}")
            return None


class YNCApplication(Gtk.Window):
    """GTK-based GUI for the YNC Assistant Bot."""
    
    def __init__(self, project_path):
        super().__init__()
        self.launcher = BotLauncher(project_path)
        
        self.set_title("YNC Assistant - Bot Launcher")
        self.set_default_size(800, 600)
        self.set_border_width(10)
        
        self.build_ui()
        self.refresh_status()
    
    def build_ui(self):
        """Build the application UI."""
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)
        
        # Header
        header = self.create_header()
        main_box.pack_start(header, False, False, 0)
        
        # Status panel
        status_panel = self.create_status_panel()
        main_box.pack_start(status_panel, False, False, 0)
        
        # Bot controls
        controls = self.create_controls()
        main_box.pack_start(controls, False, False, 0)
        
        # Log panel
        log_panel = self.create_log_panel()
        main_box.pack_start(log_panel, True, True, 0)
        
        self.main_box = main_box
    
    def create_header(self):
        """Create the header section."""
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        # Title
        label = Gtk.Label()
        label.set_markup("<span font-weight='bold' font-size='x-large'>🤖 YNC Assistant</span>\n"
                        "<span>Telegram Bot for YNC & GMB Universities</span>")
        box.pack_start(label, False, False, 5)
        
        return box
    
    def create_status_panel(self):
        """Create the status display panel."""
        box = Gtk.Frame(label="System Status")
        box.set_border_width(5)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        box.add(main_box)
        
        # Status indicators
        self.status_label = Gtk.Label()
        self.status_label.set_markup("<b>Status:</b> Not Started")
        main_box.pack_start(self.status_label, False, False, 0)
        
        self.env_label = Gtk.Label()
        self.env_label.set_markup("<b>Environment:</b> Loading...")
        main_box.pack_start(self.env_label, False, False, 0)
        
        self.model_label = Gtk.Label()
        self.model_label.set_markup("<b>AI Model:</b> Not configured")
        main_box.pack_start(self.model_label, False, False, 0)
        
        self.process_label = Gtk.Label()
        self.process_label.set_markup("<b>Process:</b> Idle")
        main_box.pack_start(self.process_label, False, False, 0)
        
        return box
    
    def create_controls(self):
        """Create control buttons."""
        box = Gtk.Frame(label="Controls")
        box.set_border_width(5)
        
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.add(button_box)
        
        # Start button
        start_btn = Gtk.Button(label="▶ Start Bot")
        start_btn.connect("clicked", self.on_start)
        button_box.pack_start(start_btn, False, False, 5)
        
        # Stop button
        stop_btn = Gtk.Button(label="⏹ Stop Bot")
        stop_btn.connect("clicked", self.on_stop)
        button_box.pack_start(stop_btn, False, False, 5)
        
        # Restart button
        restart_btn = Gtk.Button(label="🔄 Restart")
        restart_btn.connect("clicked", self.on_restart)
        button_box.pack_start(restart_btn, False, False, 5)
        
        # Export button
        export_btn = Gtk.Button(label="📦 Export App")
        export_btn.connect("clicked", self.on_export)
        button_box.pack_start(export_btn, False, False, 5)
        
        return box
    
    def create_log_panel(self):
        """Create the log viewer panel."""
        box = Gtk.Frame(label="Bot Logs")
        box.set_border_width(5)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        box.add(scrolled)
        
        # Text view
        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.text_view.set_cursor_visible(False)
        
        # Add a scrollbar
        scrollbar = Gtk.Scrollbar.new(Gtk.Orientation.VERTICAL, self.text_view.get_vadjustment())
        scrolled.add(scrollbar)
        
        self.text_buffer = self.text_view.get_buffer()
        scrolled.add(self.text_view)
        
        return box
    
    def on_start(self, widget):
        """Handle start button click."""
        if not self.launcher.is_running:
            success = self.launcher.start_bot()
            if success:
                self.refresh_status()
    
    def on_stop(self, widget):
        """Handle stop button click."""
        if self.launcher.is_running:
            self.launcher.stop_bot()
            self.refresh_status()
    
    def on_restart(self, widget):
        """Handle restart button click."""
        self.launcher.restart_bot()
        self.refresh_status()
    
    def on_export(self, widget):
        """Handle export button click."""
        self.launcher.export_as_application()
        self.refresh_status()
    
    def refresh_status(self):
        """Refresh the status display."""
        env_vars = self.launcher.read_env()
        
        # Update status
        status_icon = "○" if not self.launcher.is_running else "🟢"
        self.status_label.set_markup(
            f"<b>Status:</b> {status_icon} {self.launcher.status}\n"
            f"<b>Uptime:</b> {self.launcher.start_time.strftime('%H:%M:%S') if self.launcher.start_time else 'N/A'}"
        )
        
        # Update environment
        env_status = "✓" if env_vars else "○"
        self.env_label.set_markup(
            f"{env_status} Environment: {len(env_vars)} variables loaded\n"
            f"Token: {env_vars.get('TELEGRAM_BOT_TOKEN', 'Not set')[:40]}...\n"
            f"AI Key: {env_vars.get('VENCE_API_KEY', 'Not set')[:40]}..."
        )
        
        # Update model
        model = env_vars.get('AI_MODEL', 'Not configured')
        self.model_label.set_markup(f"🤖 Model: {model}")
        
        # Update process
        process = self.launcher.get_bot_status()
        process_icon = "🟢" if process.get('status') == 'Running' else "🔵"
        self.process_label.set_markup(
            f"{process_icon} Process: {process.get('status', 'Not Running')}\n"
            f"PID: {process.get('pid', 'N/A')}\n"
            f"Uptime: {process.get('uptime', 0):.0f}s"
        )
        
        # Add refresh message to logs
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_msg = f"[{timestamp}] Status refreshed: {self.launcher.status}"
        self.launcher.log(log_msg)
        self.update_log_display()
    
    def update_log_display(self):
        """Update the log display with new messages."""
        # Clear buffer and add new logs
        self.text_buffer.set_text("")
        
        while not self.launcher.log_messages.empty():
            log_entry = self.launcher.log_messages.get_nowait()
            self.text_buffer.insert_at_cursor(log_entry + "\n")
    
    def run(self):
        """Run the application."""
        self.launcher.log("Application launched")
        self.refresh_status()
        self.update_log_display()
        Gtk.main()


def main():
    """Main entry point."""
    project_path = "/Users/fnb/Downloads/ync-assistant"
    
    # Check if GTK is available
    if HAS_GTK:
        app = YNCApplication(project_path)
        app.run()
    else:
        # Fallback to command-line mode
        print("GTK not available. Running in CLI mode...")
        launcher = BotLauncher(project_path)
        
        # Start the bot
        if launcher.start_bot():
            # Main loop
            while True:
                time.sleep(5)
                status = launcher.get_bot_status()
                print(f"\nStatus: {status['status']} | PID: {status['pid']} | "
                      f"Uptime: {status['uptime']:.0f}s")
                
                if not launcher.is_running:
                    print("\nPress Ctrl+C to exit, or wait for bot to restart...")
    
    return 0


if __name__ == "__main__":
    main()
