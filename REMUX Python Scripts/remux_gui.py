#!/usr/bin/env python3
"""
remux_gui.py
A GUI for the batch remuxing script with automatic language detection, built with tkinter.
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
        self.root.geometry("950x700")

        self.mkvmerge_path = find_mkvmerge()
        self.update_queue = queue.Queue()
        self.running = False
        self.available_audio_langs = []
        self.available_sub_langs = []

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

        # Available Languages Display Frame
        avail_frame = ttk.LabelFrame(main_frame, text="Available Languages in MKV Files", padding="10")
        avail_frame.pack(fill=tk.X, pady=5)
        
        # Audio languages display
        ttk.Label(avail_frame, text="Audio:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.avail_audio_label = ttk.Label(avail_frame, text="Select input directory to scan...", 
                                           foreground="gray", relief=tk.SUNKEN, padding=5)
        self.avail_audio_label.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        
        # Subtitle languages display
        ttk.Label(avail_frame, text="Subtitles:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.avail_sub_label = ttk.Label(avail_frame, text="Select input directory to scan...", 
                                         foreground="gray", relief=tk.SUNKEN, padding=5)
        self.avail_sub_label.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)
        
        avail_frame.columnconfigure(1, weight=1)

        # Options Frame
        opts_frame = ttk.LabelFrame(main_frame, text="Language Selection", padding="10")
        opts_frame.pack(fill=tk.X, pady=5)
        opts_frame.columnconfigure(1, weight=1)
        opts_frame.columnconfigure(3, weight=1)

        ttk.Label(opts_frame, text="Audio Langs:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.audio_langs = tk.StringVar(value="eng")
        audio_entry = ttk.Entry(opts_frame, textvariable=self.audio_langs)
        audio_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        ttk.Label(opts_frame, text="(comma-separated, e.g., eng,jpn)", foreground="gray", font=("TkDefaultFont", 8)).grid(row=1, column=1, sticky=tk.W, padx=5)

        ttk.Label(opts_frame, text="Subtitle Langs:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.sub_langs = tk.StringVar(value="eng")
        sub_entry = ttk.Entry(opts_frame, textvariable=self.sub_langs)
        sub_entry.grid(row=0, column=3, sticky=tk.EW, padx=5)
        ttk.Label(opts_frame, text="(comma-separated, e.g., eng,ger)", foreground="gray", font=("TkDefaultFont", 8)).grid(row=1, column=3, sticky=tk.W, padx=5)

        # Quick select buttons
        btn_frame = ttk.Frame(opts_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Select All Audio", command=self.select_all_audio).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Select All Subtitles", command=self.select_all_subs).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Audio", command=lambda: self.audio_langs.set("")).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Subtitles", command=lambda: self.sub_langs.set("")).pack(side=tk.LEFT, padx=5)

        self.skip_exists = tk.BooleanVar(value=True)
        ttk.Checkbutton(opts_frame, text="Skip if output exists", variable=self.skip_exists).grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        self.dry_run = tk.BooleanVar(value=False)
        ttk.Checkbutton(opts_frame, text="Dry-run only", variable=self.dry_run).grid(row=3, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)

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

        self.status_label = ttk.Label(control_frame, text="Ready. Select an input directory to begin.", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        if not self.mkvmerge_path:
            self.show_error("mkvmerge not found. Please install MKVToolNix and ensure mkvmerge is in your system's PATH.")
            self.start_button.config(state=tk.DISABLED)

    def browse_input(self):
        path = filedialog.askdirectory()
        if path:
            self.input_dir.set(path)
            if not self.output_dir.get():
                self.output_dir.set(str(Path(path) / "remuxed"))
            # Automatically scan for languages
            self.scan_languages()

    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir.set(path)

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def scan_languages(self):
        """Automatically scan MKV files and display available languages."""
        input_path = Path(self.input_dir.get())
        
        if not input_path.is_dir():
            return
        
        mkv_files = sorted(input_path.glob("*.mkv"))
        if not mkv_files:
            self.avail_audio_label.config(text="No MKV files found", foreground="red")
            self.avail_sub_label.config(text="No MKV files found", foreground="red")
            self.status_label.config(text="No .mkv files found in the input directory.")
            return
        
        self.avail_audio_label.config(text=f"Scanning {len(mkv_files)} files...", foreground="blue")
        self.avail_sub_label.config(text=f"Scanning {len(mkv_files)} files...", foreground="blue")
        self.status_label.config(text=f"Scanning {len(mkv_files)} files for available languages...")
        self.root.update()
        
        # Run scan in separate thread to avoid freezing GUI
        def scan_thread():
            audio_langs, sub_langs = get_available_languages(self.mkvmerge_path, mkv_files)
            self.root.after(0, lambda: self.update_available_languages(audio_langs, sub_langs))
        
        threading.Thread(target=scan_thread, daemon=True).start()

    def update_available_languages(self, audio_langs, sub_langs):
        """Update the display with scanned languages."""
        self.available_audio_langs = audio_langs
        self.available_sub_langs = sub_langs
        
        if audio_langs:
            audio_text = ", ".join(audio_langs)
            self.avail_audio_label.config(text=audio_text, foreground="green")
        else:
            self.avail_audio_label.config(text="None found", foreground="orange")
        
        if sub_langs:
            sub_text = ", ".join(sub_langs)
            self.avail_sub_label.config(text=sub_text, foreground="green")
        else:
            self.avail_sub_label.config(text="None found", foreground="orange")
        
        self.status_label.config(text=f"Scan complete. Found {len(audio_langs)} audio and {len(sub_langs)} subtitle languages.")

    def select_all_audio(self):
        """Select all available audio languages."""
        if self.available_audio_langs:
            self.audio_langs.set(",".join(self.available_audio_langs))
        else:
            messagebox.showinfo("No Languages", "No audio languages available. Please scan files first.")

    def select_all_subs(self):
        """Select all available subtitle languages."""
        if self.available_sub_langs:
            self.sub_langs.set(",".join(self.available_sub_langs))
        else:
            messagebox.showinfo("No Languages", "No subtitle languages available. Please scan files first.")

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
