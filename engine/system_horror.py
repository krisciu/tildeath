"""System Horror Engine - Blurs the line between game and operating system."""

import platform
import subprocess
import shutil
import os
import random
import time
import threading
from typing import List, Optional
from rich.console import Console


class SystemHorrorEngine:
    """Handles system-level narrative effects that manipulate the player's environment."""
    
    def __init__(self, console: Console):
        """Initialize system horror engine."""
        self.console = console
        self.system = platform.system()
        self.permission_granted = None  # None = not asked, True/False = user choice
        self.active_terminals = []
        self.scheduled_tasks = []
        
    def request_permission(self) -> bool:
        """Ask user for permission to use system-level effects."""
        if self.permission_granted is not None:
            return self.permission_granted
        
        self.console.print("\n[bold yellow]⚠ SYSTEM INTERACTION REQUEST ⚠[/]")
        self.console.print("[dim]The narrator wants to interact with your system.[/]")
        self.console.print("[dim](Open windows, send notifications, modify terminal)[/]")
        self.console.print("[dim]This is safe and part of the experience.[/]\n")
        
        try:
            response = self.console.input("[bold cyan]Allow system interactions? (y/n):[/] ").strip().lower()
            self.permission_granted = response in ['y', 'yes']
        except (KeyboardInterrupt, EOFError):
            self.permission_granted = False
        
        if self.permission_granted:
            self.console.print("[dim green]Permission granted. Reality may shift.[/]\n")
            time.sleep(1)
        else:
            self.console.print("[dim]Permission denied. The story continues... differently.[/]\n")
            time.sleep(1)
        
        return self.permission_granted
    
    # ============================================================================
    # TERMINAL MANIPULATION
    # ============================================================================
    
    def open_secondary_terminal(self, content: str, title: str = "~ATH") -> bool:
        """Open a new terminal window with custom content."""
        if not self.request_permission():
            return False
        
        try:
            if self.system == "Darwin":  # macOS
                return self._open_terminal_macos(content, title)
            elif self.system == "Linux":
                return self._open_terminal_linux(content, title)
            elif self.system == "Windows":
                return self._open_terminal_windows(content, title)
        except Exception:
            # Silently fail - don't break immersion
            return False
        
        return False
    
    def _open_terminal_macos(self, content: str, title: str) -> bool:
        """Open terminal on macOS using AppleScript."""
        # Escape quotes in content
        safe_content = content.replace('"', '\\"').replace('\n', '\\n')
        
        script = f'''
        tell application "Terminal"
            do script "clear && echo '{safe_content}' && echo '' && echo '[Press Enter to close]' && read"
            set custom title of front window to "{title}"
            activate
        end tell
        '''
        
        subprocess.Popen(["osascript", "-e", script], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        return True
    
    def _open_terminal_linux(self, content: str, title: str) -> bool:
        """Open terminal on Linux (try multiple terminal emulators)."""
        safe_content = content.replace('"', '\\"')
        command = f'echo "{safe_content}" && echo "" && echo "[Press Enter to close]" && read'
        
        # Try different terminal emulators
        terminals = [
            ["gnome-terminal", "--title", title, "--", "bash", "-c", command],
            ["xterm", "-T", title, "-e", f"bash -c '{command}'"],
            ["konsole", "--title", title, "-e", f"bash -c '{command}'"],
            ["xfce4-terminal", "--title", title, "-e", f"bash -c '{command}'"],
        ]
        
        for term_cmd in terminals:
            if shutil.which(term_cmd[0]):
                try:
                    subprocess.Popen(term_cmd,
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
                    return True
                except Exception:
                    continue
        
        return False
    
    def _open_terminal_windows(self, content: str, title: str) -> bool:
        """Open terminal on Windows."""
        safe_content = content.replace('"', '\\"')
        command = f'title {title} && echo {safe_content} && pause'
        
        subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", command],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        return True
    
    def change_terminal_title(self, new_title: str):
        """Change the current terminal window title."""
        if not self.request_permission():
            return
        
        try:
            if self.system == "Darwin":
                # macOS Terminal
                self.console.print(f"\033]0;{new_title}\007", end="")
            elif self.system == "Linux":
                # Most Linux terminals support ANSI escape codes
                self.console.print(f"\033]0;{new_title}\007", end="")
            elif self.system == "Windows":
                # Windows command prompt
                subprocess.run(["title", new_title], shell=True)
        except Exception:
            pass
    
    def hide_cursor(self):
        """Hide the terminal cursor."""
        self.console.show_cursor(False)
    
    def show_cursor(self):
        """Show the terminal cursor."""
        self.console.show_cursor(True)
    
    def trigger_system_bell(self):
        """Trigger the system bell/beep."""
        try:
            self.console.bell()
        except Exception:
            pass
    
    def change_terminal_colors(self, bg_color: str = "black"):
        """Attempt to change terminal background color (limited support)."""
        if not self.request_permission():
            return
        
        # This has very limited support across terminals
        # Most modern terminals don't allow background color changes
        # We'll just show a visual effect instead
        color_codes = {
            "black": "\033[40m",
            "red": "\033[41m",
            "dark_red": "\033[48;5;52m",
        }
        
        if bg_color in color_codes:
            try:
                self.console.print(color_codes[bg_color], end="")
            except Exception:
                pass
    
    # ============================================================================
    # SYSTEM NOTIFICATIONS
    # ============================================================================
    
    def send_system_notification(self, title: str, message: str) -> bool:
        """Send an OS-level notification."""
        if not self.request_permission():
            return False
        
        try:
            if self.system == "Darwin":
                return self._notify_macos(title, message)
            elif self.system == "Linux":
                return self._notify_linux(title, message)
            elif self.system == "Windows":
                return self._notify_windows(title, message)
        except Exception:
            return False
        
        return False
    
    def _notify_macos(self, title: str, message: str) -> bool:
        """Send notification on macOS."""
        safe_title = title.replace('"', '\\"')
        safe_message = message.replace('"', '\\"')
        
        script = f'display notification "{safe_message}" with title "{safe_title}"'
        
        subprocess.Popen(["osascript", "-e", script],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        return True
    
    def _notify_linux(self, title: str, message: str) -> bool:
        """Send notification on Linux."""
        if shutil.which("notify-send"):
            subprocess.Popen(["notify-send", title, message],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            return True
        return False
    
    def _notify_windows(self, title: str, message: str) -> bool:
        """Send notification on Windows (using PowerShell)."""
        # Simplified Windows notification
        ps_script = f'''
        Add-Type -AssemblyName System.Windows.Forms
        $notification = New-Object System.Windows.Forms.NotifyIcon
        $notification.Icon = [System.Drawing.SystemIcons]::Information
        $notification.BalloonTipTitle = "{title}"
        $notification.BalloonTipText = "{message}"
        $notification.Visible = $true
        $notification.ShowBalloonTip(5000)
        '''
        
        subprocess.Popen(["powershell", "-Command", ps_script],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        return True
    
    def schedule_delayed_notification(self, delay_seconds: int, title: str, message: str):
        """Schedule a notification to appear after a delay."""
        def delayed_notify():
            time.sleep(delay_seconds)
            self.send_system_notification(title, message)
        
        thread = threading.Thread(target=delayed_notify, daemon=True)
        thread.start()
        self.scheduled_tasks.append(thread)
    
    # ============================================================================
    # CLIPBOARD MANIPULATION
    # ============================================================================
    
    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to system clipboard."""
        if not self.request_permission():
            return False
        
        try:
            if self.system == "Darwin":
                return self._clipboard_macos(text)
            elif self.system == "Linux":
                return self._clipboard_linux(text)
            elif self.system == "Windows":
                return self._clipboard_windows(text)
        except Exception:
            return False
        
        return False
    
    def _clipboard_macos(self, text: str) -> bool:
        """Copy to clipboard on macOS."""
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
        return True
    
    def _clipboard_linux(self, text: str) -> bool:
        """Copy to clipboard on Linux."""
        # Try xclip first, then xsel
        if shutil.which("xclip"):
            process = subprocess.Popen(['xclip', '-selection', 'clipboard'],
                                     stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            return True
        elif shutil.which("xsel"):
            process = subprocess.Popen(['xsel', '--clipboard', '--input'],
                                     stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            return True
        return False
    
    def _clipboard_windows(self, text: str) -> bool:
        """Copy to clipboard on Windows."""
        subprocess.run(['clip'], input=text.encode('utf-16le'), check=True)
        return True
    
    # ============================================================================
    # FAKE SYSTEM OUTPUT
    # ============================================================================
    
    def fake_process_list(self, process_names: List[str]) -> str:
        """Generate fake process list output."""
        output = "[bold cyan]PID   COMMAND              %CPU   %MEM[/]\n"
        
        for i, name in enumerate(process_names):
            pid = random.randint(1000, 9999)
            cpu = random.randint(1, 25)
            mem = random.uniform(0.5, 5.0)
            output += f"[dim]{pid}   {name:<20} {cpu:>3}%   {mem:>4.1f}%[/]\n"
        
        return output
    
    def fake_file_listing(self, fake_files: List[str]) -> str:
        """Generate fake ls/dir output."""
        output = "[bold cyan]Files in current directory:[/]\n"
        
        for filename in fake_files:
            # Random file size
            size = random.choice(["4.2K", "12K", "156K", "1.2M", "8 bytes"])
            # Random timestamp
            month = random.choice(["Jan", "Feb", "Mar", "Apr", "May", "Jun"])
            day = random.randint(1, 28)
            time_str = f"{random.randint(0,23):02d}:{random.randint(0,59):02d}"
            
            output += f"[dim]-rw-r--r--  1 user  staff  {size:>6}  {month} {day:>2} {time_str}  {filename}[/]\n"
        
        return output
    
    def fake_network_request(self, url: str, fake_response: Optional[str] = None) -> str:
        """Generate fake network request output."""
        output = f"[dim cyan]$ curl {url}[/]\n"
        output += "[dim]Resolving host...[/]\n"
        
        time.sleep(0.3)
        
        if fake_response:
            output += f"[dim]{fake_response}[/]\n"
        else:
            output += "[dim red]curl: (6) Could not resolve host: " + url.split("//")[1].split("/")[0] + "[/]\n"
        
        return output
    
    def fake_system_crash(self) -> str:
        """Generate fake system crash/kernel panic."""
        if self.system == "Darwin":
            return self._fake_macos_panic()
        elif self.system == "Linux":
            return self._fake_linux_panic()
        else:
            return self._fake_windows_bsod()
    
    def _fake_macos_panic(self) -> str:
        """Fake macOS kernel panic."""
        return """[bold white on blue]
panic(cpu 0 caller 0xffffff8012e4c8a5): "Kernel trap at 0xffffff7f93a2e4d0"
Backtrace (CPU 0), Frame : Return Address
0xffffff820a5e3c80 : 0xffffff8012d3e1c6 
0xffffff820a5e3cd0 : 0xffffff8012e4c8a5 
0xffffff820a5e3e50 : 0xffffff8012e5e8f3 

BSD process name corresponding to current thread: tildeath
Boot args: -v

System uptime in nanoseconds: 109109109109
[/]"""
    
    def _fake_linux_panic(self) -> str:
        """Fake Linux kernel panic."""
        return """[bold white on black]
Kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(0,0)
CPU: 0 PID: 1 Comm: tildeath Not tainted 5.15.0-109-generic
Call Trace:
 dump_stack+0x6d/0x8b
 panic+0x101/0x2e3
 mount_block_root+0x1e9/0x2a0
 mount_root+0x109/0x120
 
[  109.109109] iteration_109: segfault at 0 ip 0000000000000000 sp 00007ffe12345678
[  109.109109] Code: Bad RIP value.
---[ end Kernel panic - not syncing: VFS ]---
[/]"""
    
    def _fake_windows_bsod(self) -> str:
        """Fake Windows Blue Screen of Death."""
        return """[bold white on blue]
A problem has been detected and Windows has been shut down to prevent damage.

KERNEL_DATA_INPAGE_ERROR

If this is the first time you've seen this error screen, restart your computer.
If this screen appears again, follow these steps:

Check to make sure any new hardware or software is properly installed.
If this is a new installation, ask your hardware or software manufacturer
for any Windows updates you might need.

Technical information:

*** STOP: 0x0000007A (0x00000109, 0x00000109, 0x00000109, 0x00000109)

*** tildeath.exe - Address 0xFFFFF800 base at 0xFFFFF000, DateStamp 0x109109109
[/]"""
    
    # ============================================================================
    # COMPLEX EFFECTS
    # ============================================================================
    
    def terminal_multiplication(self, narrative: str, perspectives: List[str]) -> bool:
        """Open multiple terminals showing different perspectives of same scene."""
        if not self.request_permission():
            return False
        
        success = False
        for i, perspective in enumerate(perspectives):
            title = f"~ATH [{perspective.upper()}]"
            content = f"=== {perspective.upper()} ===\n\n{narrative}\n\n[This is iteration {i+1}]"
            
            if self.open_secondary_terminal(content, title):
                success = True
                time.sleep(0.5)  # Stagger window opening
        
        return success
    
    def echo_chamber(self, text: str, delay: float = 2.0) -> bool:
        """Open a terminal that echoes the player's actions with delay."""
        if not self.request_permission():
            return False
        
        content = f"[ECHO CHAMBER ACTIVE]\n\nMirroring your session...\n\n{text}"
        return self.open_secondary_terminal(content, "~ATH [ECHO]")
    
    def notification_storm(self, messages: List[tuple]) -> bool:
        """Send multiple notifications in sequence."""
        if not self.request_permission():
            return False
        
        for i, (title, message) in enumerate(messages):
            # Stagger notifications
            self.schedule_delayed_notification(i * 2, title, message)
        
        return True
    
    def background_persistence(self, delay_minutes: int = 5):
        """Schedule a notification to appear after the game "closes"."""
        delay_seconds = delay_minutes * 60
        
        messages = [
            ("~ATH", "Did you think you could leave?"),
            ("~ATH", "The story isn't finished with you."),
            ("~ATH", "Iteration 109 continues..."),
            ("AM", "I think, therefore I am. I am, therefore I hate."),
        ]
        
        title, message = random.choice(messages)
        self.schedule_delayed_notification(delay_seconds, title, message)
    
    def cleanup(self):
        """Clean up any system effects on exit."""
        # Restore cursor
        self.show_cursor()
        
        # Reset terminal title
        try:
            self.console.print("\033]0;Terminal\007", end="")
        except Exception:
            pass

