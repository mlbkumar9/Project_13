#!/usr/bin/env python3
"""
remux_gui.py
A GUI for the batch remuxing script with language detection, built with tkinter.
"""

import json
import queue
import shutil
import subprocess
import sys
import threading
import time
import re
from pathlib import Path
from typing import Optional
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# --- Core Remuxing Logic (adapted from the original script) ---

def find_mkvmerge() -> Optional[str]:
    mk = shutil.which("mkvmerge") or shutil.which("mkvmerge.exe")
    if mk:
        return mk
    candidate = r"C:\Program Files\MKVToolNix\mkvmerge.exe"
    return candidate if Path(candidate).exists() else None

def identify_tracks(mkvmerge_path: str, src: Path, timeout: float = 10.0):
    cmd = [mkvmerge_path, "--identify", "--identification-format", "json", str(src)]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout, check=False)
        if res.returncode != 0:
            return {"ok": False, "err": res.stderr.strip() or res.stdout.strip() or f"rc={res.returncode}"}
        return {"ok": True, "data": json.loads(res.stdout)}
    except Exception as e:
        return {"ok": False, "err": str(e)}

def get_available_languages(mkvmerge_path: str, files: list):
    """Scan all files and return available audio and subtitle languages."""
    all_audio_langs = set()
    all_sub_langs = set()
    
    for file in files:
        ident = identify_tracks(mkvmerge_path, file)
        if not ident["ok"]:
            continue
        
        for track in ident["data"].get("tracks", []):
            track_type = track.get("type", "").lower()
            lang = track.get("properties", {}).get("language", "und").lower()
            
            if track_type == "audio":
                all_audio_langs.add(lang)
            elif track_type in ("subtitles", "subtitle"):
                all_sub_langs.add(lang)
    
    return sorted(all_audio_langs), sorted(all_sub_langs)

def fmt_time(sec: Optional[float]) -> str:
    if sec is None:
        return "--:--"
    try:
        s = int(round(sec))
        m, s = divmod(s, 60)
        return f"{m:02d}:{s:02d}"
    except (ValueError, TypeError):
        return "--:--"

def remux_file(mkvmerge_path: str, src_path: Path, out_path: Path, audio_langs: list, sub_langs: list,
               skip_if_exists: bool, dry_run: bool, update_queue: queue.Queue, row_idx: int):
    """
    Performs the remux operation for a single file and sends progress updates to the GUI queue.
    """
    start_time = time.time()
    
    def send_update(data):
        data['row_idx'] = row_idx
        update_queue.put(data)

    send_update({"status": "Pending", "pct": 0, "elapsed": 0, "remaining": None})

    if skip_if_exists and out_path.exists() and out_path.stat().st_size > 0:
        send_update({"status": "Skipped (exists)", "pct": 100, "elapsed": 0, "finished": True, "success": True})
        return

    ident = identify_tracks(mkvmerge_path, src_path)
    if not ident["ok"]:
        send_update({"status": f"ID Failed", "pct": 0, "finished": True, "success": False})
        return

    audio_ids = [
        t["id"] for t in ident["data"].get("tracks", [])
        if t.get("type") == "audio" and (t.get("properties", {}).get("language") or "und").lower() in audio_langs
    ]
    sub_ids = [
        t["id"] for t in ident["data"].get("tracks", [])
        if t.get("type") in ("subtitles", "subtitle") and (t.get("properties", {}).get("language") or "und").lower() in sub_langs
    ]

    if not audio_ids:
        send_update({"status": "No desired audio", "pct": 0, "finished": True, "success": False})
        return

    cmd = [mkvmerge_path, "-o", str(out_path), "--audio-tracks", ",".join(map(str, audio_ids))]
    if sub_ids:
        cmd += ["--subtitle-tracks", ",".join(map(str, sub_ids))]
    else:
        cmd += ["--no-subtitles"]
    cmd += ["--ui-language", "en", "--gui-mode", str(src_path)]

    if dry_run:
        send_update({"status": "Dry-run (skipped)", "pct": 100, "finished": True, "success": True})
        return

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, bufsize=1, encoding="utf-8", errors="replace")
    except Exception as e:
        send_update({"status": "Launch failed", "pct": 0, "finished": True, "success": False})
        return

    re_progress = re.compile(r"(?:#GUI#progress|Progress:)\s*([0-9]{1,3})")
    
    for line in iter(proc.stdout.readline, ""):
        m = re_progress.search(line)
        if m:
            pct = int(m.group(1))
            elapsed = time.time() - start_time
            remaining = (elapsed * (100 - pct) / pct) if pct > 0 else None
            send_update({"status": "Processing", "pct": pct, "elapsed": elapsed, "remaining": remaining})
    
    proc.wait()
    final_elapsed = time.time() - start_time

    if proc.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0:
        send_update({"status": "OK", "pct": 100, "elapsed": final_elapsed, "remaining": 0, "finished": True, "success": True})
    else:
        send_update({"status": f"FAILED (rc={proc.returncode})", "elapsed": final_elapsed, "finished": True, "success": False})


# --- GUI Application ---

class RemuxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MKV Batch Remuxer")
        self.root.geometry("900x650")

        self.mkvmerge_path = find_mkvmerge()
        self.update_queue = queue.Queue()
        self.running = False

        # --- UI Setup ---
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input/Output Frame
        io_frame = ttk.LabelFrame(main_frame, text="Directories", padding="10")
        io_frame.pack(fill=tk.X, pady=5)
        io_frame.columnconfigure(1, weight=1)

        ttk.Label(io_frame, text="Input:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.input_dir = tk.StringVar()
        ttk.Entry(io_frame, textvariable=self.input_dir).grid(row=0, column=1, sticky=tk.EW)
        ttk.Button(io_frame, text="Browse...", command=self.browse_input).grid(row=0, column=2, padx=5)

        ttk.Label(io_frame, text="Output:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.output_dir = tk.StringVar()
        ttk.Entry(io_frame, textvariable=self.output_dir).grid(row=1, column=1, sticky=tk.EW)
        ttk.Button(io_frame, text="Browse...", command=self.browse_output).grid(row=1, column=2, padx=5)

        # Options Frame
        opts_frame = ttk.LabelFrame(main_frame, text="Language Options", padding="10")
        opts_frame.pack(fill=tk.X, pady=5)
        opts_frame.columnconfigure(1, weight=1)
        opts_frame.columnconfigure(3, weight=1)

        ttk.Label(opts_frame, text="Audio Langs:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.audio_langs = tk.StringVar(value="eng")
        ttk.Entry(opts_frame, textvariable=self.audio_langs).grid(row=0, column=1, sticky=tk.EW, padx=5)

        ttk.Label(opts_frame, text="Subtitle Langs:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.sub_langs = tk.StringVar(value="eng")
        ttk.Entry(opts_frame, textvariable=self.sub_langs).grid(row=0, column=3, sticky=tk.EW, padx=5)

        # Scan Languages Button
        scan_frame = ttk.Frame(opts_frame)
        scan_frame.grid(row=1, column=0, columnspan=4, pady=5)
        self.scan_button = ttk.Button(scan_frame, text="🔍 Scan Available Languages", command=self.scan_languages)
        self.scan_button.pack()

        self.skip_exists = tk.BooleanVar(value=True)
        ttk.Checkbutton(opts_frame, text="Skip if output exists", variable=self.skip_exists).grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        self.dry_run = tk.BooleanVar(value=False)
        ttk.Checkbutton(opts_frame, text="Dry-run only", variable=self.dry_run).grid(row=2, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)

        # File List / Progress Table
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.tree = ttk.Treeview(tree_frame, columns=("filename", "progress", "pct", "time", "status"), show="headings")
        self.tree.heading("filename", text="Filename")
        self.tree.heading("progress", text="Progress")
        self.tree.heading("pct", text="%")
        self.tree.heading("time", text="Elapsed/Rem")
        self.tree.heading("status", text="Status")

        self.tree.column("filename", width=300)
        self.tree.column("progress", width=150)
        self.tree.column("pct", width=40, anchor=tk.E)
        self.tree.column("time", width=100, anchor=tk.E)
        self.tree.column("status", width=120)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Control Frame
        control_frame = ttk.Frame(main_frame, padding="5")
        control_frame.pack(fill=tk.X)
        
        self.start_button = ttk.Button(control_frame, text="Start Remux", command=self.start_remux)
        self.start_button.pack(side=tk.RIGHT)

        self.status_label = ttk.Label(control_frame, text="Ready.", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        if not self.mkvmerge_path:
            self.show_error("mkvmerge not found. Please install MKVToolNix and ensure mkvmerge is in your system's PATH.")
            self.start_button.config(state=tk.DISABLED)
            self.scan_button.config(state=tk.DISABLED)

    def browse_input(self):
        path = filedialog.askdirectory()
        if path:
            self.input_dir.set(path)
            if not self.output_dir.get():
                self.output_dir.set(str(Path(path) / "remuxed"))

    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir.set(path)

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def scan_languages(self):
        """Scan MKV files in input directory and display available languages."""
        input_path = Path(self.input_dir.get())
        
        if not input_path.is_dir():
            self.show_error("Please select a valid input directory first.")
            return
        
        mkv_files = sorted(input_path.glob("*.mkv"))
        if not mkv_files:
            messagebox.showwarning("No Files", "No .mkv files found in the input directory.")
            return
        
        self.status_label.config(text=f"Scanning {len(mkv_files)} files for available languages...")
        self.scan_button.config(state=tk.DISABLED)
        self.root.update()
        
        # Run scan in separate thread to avoid freezing GUI
        def scan_thread():
            audio_langs, sub_langs = get_available_languages(self.mkvmerge_path, mkv_files)
            self.root.after(0, lambda: self.display_scan_results(audio_langs, sub_langs))
        
        threading.Thread(target=scan_thread, daemon=True).start()

    def display_scan_results(self, audio_langs, sub_langs):
        """Display the scan results and update the language fields."""
        self.scan_button.config(state=tk.NORMAL)
        self.status_label.config(text="Ready.")
        
        # Create popup window with results
        result_window = tk.Toplevel(self.root)
        result_window.title("Available Languages")
        result_window.geometry("500x400")
        result_window.transient(self.root)
        result_window.grab_set()
        
        main = ttk.Frame(result_window, padding="10")
        main.pack(fill=tk.BOTH, expand=True)
        
        # Audio languages
        ttk.Label(main, text="Available Audio Languages:", font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W, pady=(0,5))
        audio_frame = ttk.Frame(main)
        audio_frame.pack(fill=tk.BOTH, expand=True, pady=(0,10))
        
        audio_text = tk.Text(audio_frame, height=8, wrap=tk.WORD)
        audio_scroll = ttk.Scrollbar(audio_frame, orient="vertical", command=audio_text.yview)
        audio_text.configure(yscrollcommand=audio_scroll.set)
        audio_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        audio_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        if audio_langs:
            audio_text.insert("1.0", ", ".join(audio_langs))
        else:
            audio_text.insert("1.0", "None found")
        audio_text.config(state=tk.DISABLED)
        
        # Subtitle languages
        ttk.Label(main, text="Available Subtitle Languages:", font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W, pady=(0,5))
        sub_frame = ttk.Frame(main)
        sub_frame.pack(fill=tk.BOTH, expand=True, pady=(0,10))
        
        sub_text = tk.Text(sub_frame, height=8, wrap=tk.WORD)
        sub_scroll = ttk.Scrollbar(sub_frame, orient="vertical", command=sub_text.yview)
        sub_text.configure(yscrollcommand=sub_scroll.set)
        sub_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        sub_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        if sub_langs:
            sub_text.insert("1.0", ", ".join(sub_langs))
        else:
            sub_text.insert("1.0", "None found")
        sub_text.config(state=tk.DISABLED)
        
        # Button frame
        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill=tk.X, pady=(10,0))
        
        def use_languages():
            if audio_langs:
                self.audio_langs.set(",".join(audio_langs))
            if sub_langs:
                self.sub_langs.set(",".join(sub_langs))
            result_window.destroy()
        
        ttk.Button(btn_frame, text="Use These Languages", command=use_languages).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Close", command=result_window.destroy).pack(side=tk.RIGHT)

    def start_remux(self):
        if self.running:
            return

        input_path = Path(self.input_dir.get())
        output_path = Path(self.output_dir.get())

        if not input_path.is_dir():
            self.show_error("Invalid input directory.")
            return
        
        audio_langs = [lang.strip() for lang in self.audio_langs.get().lower().split(',') if lang.strip()]
        if not audio_langs:
            self.show_error("At least one audio language is required.")
            return
            
        sub_langs = [lang.strip() for lang in self.sub_langs.get().lower().split(',') if lang.strip()]

        mkv_files = sorted(input_path.glob("*.mkv"))
        if not mkv_files:
            self.status_label.config(text="No .mkv files found in the input directory.")
            return

        output_path.mkdir(parents=True, exist_ok=True)
        
        self.tree.delete(*self.tree.get_children())
        self.file_map = {}
        for i, f in enumerate(mkv_files):
            item_id = self.tree.insert("", "end", values=(f.name, "", "0%", "--:--/--:--", "Pending"))
            self.file_map[i] = {"id": item_id, "path": f}

        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.scan_button.config(state=tk.DISABLED)
        self.status_label.config(text=f"Processing {len(mkv_files)} files...")

        self.worker_thread = threading.Thread(
            target=self.run_batch_thread,
            args=(mkv_files, output_path, audio_langs, sub_langs, self.skip_exists.get(), self.dry_run.get()),
            daemon=True
        )
        self.worker_thread.start()
        self.root.after(100, self.process_queue)

    def run_batch_thread(self, mkv_files, output_path, audio_langs, sub_langs, skip_exists, dry_run):
        for i, src_path in enumerate(mkv_files):
            out_path = output_path / src_path.name
            remux_file(self.mkvmerge_path, src_path, out_path, audio_langs, sub_langs,
                       skip_exists, dry_run, self.update_queue, i)
        self.update_queue.put({"type": "finished"})

    def process_queue(self):
        try:
            while not self.update_queue.empty():
                msg = self.update_queue.get_nowait()

                if msg.get("type") == "finished":
                    self.running = False
                    self.start_button.config(state=tk.NORMAL)
                    self.scan_button.config(state=tk.NORMAL)
                    ok_count = sum(1 for i in self.file_map.values() if self.tree.item(i['id'])['values'][4] == "OK")
                    fail_count = len(self.file_map) - ok_count
                    self.status_label.config(text=f"Completed. OK: {ok_count}, Failed: {fail_count}.")
                    return

                row_idx = msg.get("row_idx")
                if row_idx is None:
                    continue

                item_id = self.file_map[row_idx]["id"]
                
                pct = msg.get("pct", self.tree.set(item_id, "pct"))
                pct_val = int(pct) if isinstance(pct, (int, float)) else int(str(pct).replace('%',''))
                
                bar = "█" * (pct_val // 5) + "░" * (20 - (pct_val // 5))
                
                elapsed = msg.get("elapsed")
                remaining = msg.get("remaining")
                
                time_str = f"{fmt_time(elapsed)}/{fmt_time(remaining)}"
                
                status = msg.get("status", self.tree.set(item_id, "status"))

                self.tree.item(item_id, values=(
                    self.file_map[row_idx]["path"].name,
                    bar,
                    f"{pct_val}%",
                    time_str,
                    status
                ))

        finally:
            if self.running:
                self.root.after(100, self.process_queue)


if __name__ == "__main__":
    root = tk.Tk()
    app = RemuxApp(root)
    root.mainloop()
