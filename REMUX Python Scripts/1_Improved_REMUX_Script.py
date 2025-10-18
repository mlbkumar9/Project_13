#!/usr/bin/env python3
"""
remux_rich_improved.py
Batch remux MKV files keeping only English audio + English subtitles.
Rich live table UI with improved layout: separate % column, persistent progress bars,
separate result column, and gap before batch row.
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

from rich.console import Console
from rich.table import Table
from rich.live import Live

console = Console()

# ---------- Helpers ----------

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

def shorten(name: str, max_len: int = 40) -> str:
    if len(name) <= max_len:
        return name
    half = (max_len - 3) // 2
    return name[:half] + "..." + name[-half:]

def fmt_time(sec: Optional[float]) -> str:
    if sec is None:
        return "--:--"
    try:
        s = int(round(sec))
        m = s // 60
        ss = s % 60
        return f"{m:02d}:{ss:02d}"
    except Exception:
        return "--:--"

def _start_stdout_reader(stream, q: queue.Queue):
    def _reader():
        try:
            for ln in iter(stream.readline, ""):
                q.put(ln)
        except Exception:
            pass
        finally:
            try:
                stream.close()
            except Exception:
                pass
    t = threading.Thread(target=_reader, daemon=True)
    t.start()
    return t

# ---------- Rendering ----------

def build_table(rows, batch_info):
    """Return a rich.Table based on current rows and batch_info dict."""
    table = Table(show_header=True, header_style="bold magenta", expand=False)
    table.add_column("SL No.", width=6, justify="right")
    table.add_column("Filename", width=40, overflow="fold")
    table.add_column("Progress", width=22)
    table.add_column("%", width=5, justify="right")
    table.add_column("Elapsed", width=8, justify="right")
    table.add_column("Remaining", width=10, justify="right")
    table.add_column("Status", width=12)
    table.add_column("Result", width=8, justify="center")

    for i, r in enumerate(rows):
        # filename (without checkmark/cross - those go in Result column)
        fname_display = f"[cyan]{r['display_name']}[/cyan]"

        # progress bar - always show, regardless of completion status
        pct = int(r.get("pct", 0))
        blocks = pct // 5  # 20 blocks total
        bar = "█" * blocks + "░" * (20 - blocks)
        progress_cell = f"[white]{bar}[/white]"

        # percentage column - green color
        pct_display = f"[green]{pct:3d}%[/green]"

        elapsed = fmt_time(r.get("elapsed"))
        remaining = fmt_time(r.get("remaining")) if r.get("remaining") is not None else "--:--"
        status_text = r.get("status_text", "")

        # result column (checkmark or cross)
        result = ""
        if r.get("finished"):
            if r["success"]:
                result = "[green]✓[/green]"
            else:
                result = "[red]✗[/red]"

        table.add_row(
            str(r["no"]), 
            fname_display, 
            progress_cell, 
            pct_display,
            elapsed, 
            remaining, 
            status_text,
            result
        )
        
        # Add separator row after each file (except the last one)
        if i < len(rows) - 1:
            table.add_row("", "", "", "", "", "", "", "")

    # Add an empty row for separation before batch row
    table.add_row("", "", "", "", "", "", "", "")

    # Batch row
    b = batch_info
    batch_bar_blocks = int((b["pct"] // 5))
    batch_bar = "█" * batch_bar_blocks + "░" * (20 - batch_bar_blocks)
    batch_progress_cell = f"[white]{batch_bar}[/white]"
    batch_pct = f"[green]{b['pct']:3d}%[/green]"

    batch_elapsed = fmt_time(b.get("elapsed"))
    batch_remaining = fmt_time(b.get("remaining")) if b.get("remaining") is not None else "--:--"
    batch_status = f"{b['done']}/{b['total']} done"
    
    batch_result = ""
    if b["finished"]:
        batch_result = "[green]✓[/green]"

    table.add_row(
        "",
        "[bold bright_yellow]Batch Progress[/bold bright_yellow]",
        batch_progress_cell,
        batch_pct,
        batch_elapsed,
        batch_remaining,
        batch_status,
        batch_result
    )
    
    return table

# ---------- Remux function (updates rows in place and refreshes live) ----------

def remux_file_and_update(mkvmerge_path: str, src_path: Path, out_path: Path, row_idx: int,
                          rows, live: Live, batch_start: float, completed_times: list, log_commands: list,
                          skip_if_exists: bool, dry_run: bool, audio_langs: list, sub_langs: list):
    """
    Perform remux and update rows[row_idx] and call live.update(build_table(...)) frequently.
    Returns True/False (success), elapsed_seconds, status_string (for logging).
    """

    # prepare row
    row = rows[row_idx]
    row["status_text"] = "Pending"
    row["pct"] = 0
    row["elapsed"] = 0.0
    row["remaining"] = None
    row["finished"] = False
    row["success"] = False
    row["start_time"] = time.time()
    live.update(build_table(rows, compute_batch(rows, batch_start, completed_times)))

    # skip if exists
    if skip_if_exists and out_path.exists() and out_path.stat().st_size > 0:
        row["pct"] = 100
        row["elapsed"] = 0.0
        row["remaining"] = 0.0
        row["finished"] = True
        row["success"] = True
        row["status_text"] = "Skipped (exists)"
        completed_times.append(0.0)
        live.update(build_table(rows, compute_batch(rows, batch_start, completed_times)))
        return True, 0.0, "Skipped (exists)"

    # identify tracks
    ident = identify_tracks(mkvmerge_path, src_path)
    if not ident["ok"]:
        row["finished"] = True
        row["success"] = False
        row["status_text"] = f"FAILED identify"
        row["pct"] = 0
        row["elapsed"] = 0.0
        row["remaining"] = 0.0
        live.update(build_table(rows, compute_batch(rows, batch_start, completed_times)))
        return False, 0.0, f"identify failed: {ident.get('err')}"

    # pick audio & subtitle ids
    audio_ids = []
    sub_ids = []
    for t in ident["data"].get("tracks", []):
        ttype = (t.get("type") or "").lower()
        props = t.get("properties") or {}
        lang = (props.get("language") or "").lower()
        tid = t.get("id")
        if ttype == "audio" and isinstance(tid, int) and lang in audio_langs:
            audio_ids.append(tid)
        if ttype in ("subtitles", "subtitle") and isinstance(tid, int) and lang in sub_langs:
            sub_ids.append(tid)

    if not audio_ids:
        row["finished"] = True
        row["success"] = False
        row["status_text"] = "No desired audio"
        row["pct"] = 0
        row["elapsed"] = 0.0
        row["remaining"] = 0.0
        live.update(build_table(rows, compute_batch(rows, batch_start, completed_times)))
        return False, 0.0, "no desired audio"

    # build mkvmerge command
    cmd = [mkvmerge_path, "-o", str(out_path), "--audio-tracks", ",".join(map(str, audio_ids))]
    if sub_ids:
        cmd += ["--subtitle-tracks", ",".join(map(str, sub_ids))]
    else:
        cmd += ["--no-subtitles"]
    cmd += ["--ui-language", "en", "--gui-mode", str(src_path)]
    log_commands.append(" ".join(cmd))

    if dry_run:
        row["pct"] = 100
        row["finished"] = True
        row["success"] = True
        row["status_text"] = "Dry-run (skipped)"
        completed_times.append(0.0)
        live.update(build_table(rows, compute_batch(rows, batch_start, completed_times)))
        return True, 0.0, "dry-run"

    # spawn mkvmerge
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, bufsize=1, encoding="utf-8", errors="replace")
    except Exception as e:
        row["finished"] = True
        row["success"] = False
        row["status_text"] = f"Launch failed"
        row["pct"] = 0
        row["elapsed"] = 0.0
        row["remaining"] = 0.0
        live.update(build_table(rows, compute_batch(rows, batch_start, completed_times)))
        return False, 0.0, f"launch error: {e}"

    q = queue.Queue()
    _start_stdout_reader(proc.stdout, q)
    re_progress = re.compile(r"(?:#GUI#progress|Progress:)\s*([0-9]{1,3})")
    src_size = src_path.stat().st_size if src_path.exists() else None
    had_progress = False
    full_lines = []
    start = time.time()

    # live update loop
    while proc.poll() is None or not q.empty():
        try:
            line = q.get(timeout=0.25)
        except queue.Empty:
            line = None

        if line is not None:
            full_lines.append(line.rstrip("\n"))
            m = re_progress.search(line)
            if m:
                pct = int(m.group(1))
                if pct < 0:
                    pct = 0
                if pct > 100:
                    pct = 100
                had_progress = True
                row["pct"] = pct
                now = time.time()
                row["elapsed"] = now - start
                if pct > 0:
                    row["remaining"] = (row["elapsed"] * (100 - pct) / pct)
                else:
                    row["remaining"] = None
                row["status_text"] = "Processing"
                # update batch row and table
                live.update(build_table(rows, compute_batch(rows, batch_start, completed_times)))
        else:
            # fallback filesize based progress (if mkvmerge doesn't emit progress)
            if (not had_progress) and out_path.exists() and src_size:
                try:
                    cur = out_path.stat().st_size
                    pct = int(min(99, (cur / src_size) * 100))
                except Exception:
                    pct = 0
                if pct > row["pct"]:
                    row["pct"] = pct
                    now = time.time()
                    row["elapsed"] = now - start
                    if pct > 0:
                        row["remaining"] = (row["elapsed"] * (100 - pct) / pct)
                    else:
                        row["remaining"] = None
                    row["status_text"] = "Processing"
                    live.update(build_table(rows, compute_batch(rows, batch_start, completed_times)))

    rc = proc.wait()
    elapsed = time.time() - start
    tail = "\n".join(full_lines[-12:]) if full_lines else ""
    if rc == 0 and out_path.exists() and out_path.stat().st_size > 0:
        row["pct"] = 100
        row["elapsed"] = elapsed
        row["remaining"] = 0.0
        row["finished"] = True
        row["success"] = True
        row["status_text"] = "OK"
        completed_times.append(elapsed)
        live.update(build_table(rows, compute_batch(rows, batch_start, completed_times)))
        return True, elapsed, "OK"
    else:
        # Keep the progress as is, don't reset to 0
        row["elapsed"] = elapsed
        row["remaining"] = 0.0
        row["finished"] = True
        row["success"] = False
        reason = f"rc={rc}"
        if "Error" in tail:
            row["status_text"] = "FAILED"
        else:
            row["status_text"] = f"FAILED (rc={rc})"
        live.update(build_table(rows, compute_batch(rows, batch_start, completed_times)))
        return False, elapsed, reason

# ---------- Batch helper ----------

def compute_batch(rows, batch_start, completed_times):
    total = len(rows)
    done = sum(1 for r in rows if r.get("finished") and r.get("success"))
    # batch pct - average of per-file pct
    avg_pct = int(sum(r.get("pct", 0) for r in rows) / total) if total > 0 else 0
    elapsed = time.time() - batch_start
    # estimate remaining: use avg of completed times if available; account for current partial progress
    remaining = None
    if len(completed_times) > 0:
        avg_time = sum(completed_times) / len(completed_times)
        remaining_files = total - sum(1 for r in rows if r.get("finished"))
        # estimate for the currently running file's remaining (if any)
        current_remaining = None
        for r in rows:
            if (not r.get("finished")) and r.get("pct", 0) > 0:
                pct = r["pct"]
                if pct > 0:
                    current_elapsed = r.get("elapsed", 0.0)
                    current_remaining = current_elapsed * (100 - pct) / pct
                break
        if current_remaining is None:
            current_remaining = 0.0
        remaining = current_remaining + max(0, remaining_files - 1) * avg_time
    else:
        # no completed times yet -> try to estimate from current file only
        current_remaining = None
        for r in rows:
            if (not r.get("finished")) and r.get("pct", 0) > 0:
                pct = r["pct"]
                if pct > 0:
                    current_elapsed = r.get("elapsed", 0.0)
                    current_remaining = current_elapsed * (100 - pct) / pct
                break
        remaining = current_remaining
    return {
        "pct": avg_pct, 
        "elapsed": elapsed, 
        "remaining": remaining, 
        "done": sum(1 for r in rows if r.get("finished")), 
        "total": total, 
        "finished": all(r.get("finished") for r in rows)
    }

# ---------- Main ----------

def main():
    console.print("[bold cyan]=== MKVToolNix batch remux ===[/]")

    inp = input("Enter input directory path: ").strip().strip('"')
    if not inp:
        console.print("[red]Input directory required.[/]")
        return
    input_dir = Path(inp)
    if not input_dir.exists() or not input_dir.is_dir():
        console.print(f"[red]Directory not found: {input_dir}[/]")
        return

    outp = input("Enter output directory path (blank = remuxed): ").strip().strip('"')
    output_dir = Path(outp) if outp else input_dir / "remuxed"
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_langs_str = input("Enter desired audio languages (comma-separated, e.g., eng,jpn): ").strip().lower()
    audio_langs = [lang.strip() for lang in audio_langs_str.split(',') if lang.strip()]
    if not audio_langs:
        console.print("[red]At least one audio language is required.[/]")
        return

    sub_langs_str = input("Enter desired subtitle languages (comma-separated, e.g., eng,ger) (blank for none): ").strip().lower()
    sub_langs = [lang.strip() for lang in sub_langs_str.split(',') if lang.strip()]

    skip_if_exists = (input("Skip files if output exists? (Y/n) [Y]: ").strip().lower() != "n")
    dry_run = (input("Dry-run only? (y/N) [N]: ").strip().lower() == "y")

    mkvmerge_path = find_mkvmerge()
    if not mkvmerge_path:
        console.print("[red]✗ mkvmerge not found on PATH. Install MKVToolNix or add mkvmerge to PATH.[/]")
        return

    # collect mkv files
    mkv_files = sorted(input_dir.glob("*.mkv"))
    total = len(mkv_files)
    if total == 0:
        console.print("[yellow]No .mkv files found in the input directory.[/]")
        return

    console.print(f"Found {total} MKV file(s) in: {input_dir}\n")

    # prepare rows
    rows = []
    for i, f in enumerate(mkv_files, start=1):
        rows.append({
            "no": i,
            "fullname": f.name,
            "display_name": shorten(f.name, 40),
            "pct": 0,
            "elapsed": 0.0,
            "remaining": None,
            "status_text": "Pending",
            "finished": False,
            "success": False,
            "start_time": None
        })

    log_path = output_dir / "remux_log.txt"
    with open(log_path, "a", encoding="utf-8") as lf:
        lf.write(f"==== remux run: {time.strftime('%Y-%m-%d %H:%M:%S')} ====\n")
        lf.write(f"Input dir: {input_dir}\nOutput dir: {output_dir}\nFiles: {total}\n\n")

    # store executed commands for debug (optional)
    log_commands = []

    # run live table
    batch_start = time.time()
    completed_times = []

    with Live(build_table(rows, compute_batch(rows, batch_start, completed_times)), refresh_per_second=8, console=console) as live:
        for idx, src in enumerate(mkv_files):
            out_file = output_dir / src.name
            ok, elapsed, reason = remux_file_and_update(
                mkvmerge_path, src, out_file, idx, rows, live, batch_start, completed_times, log_commands,
                skip_if_exists, dry_run, audio_langs, sub_langs
            )
            # status already updated inside function; ensure last render
            live.update(build_table(rows, compute_batch(rows, batch_start, completed_times)))

    # write final plain-text summary table to log
    final_lines = []
    final_lines.append("SL No.\tFilename\tProgress\tElapsed\tRemaining\tStatus\tResult")
    ok_count = 0
    fail_count = 0
    for r in rows:
        status_text = r.get("status_text", "")
        result_text = ""
        if r.get("success"):
            ok_count += 1
            result_text = "OK"
        elif r.get("finished") and not r.get("success"):
            fail_count += 1
            result_text = "FAILED"
        final_lines.append(
            f"{r['no']}\t{r['fullname']}\t{int(r.get('pct',0))}%\t"
            f"{fmt_time(r.get('elapsed'))}\t{fmt_time(r.get('remaining')) if r.get('remaining') is not None else '--:--'}\t"
            f"{status_text}\t{result_text}"
        )

    total_elapsed = time.time() - batch_start

    with open(log_path, "a", encoding="utf-8") as lf:
        lf.write("\n".join(final_lines) + "\n\n")
        lf.write(f"=== Summary ===\nProcessed: {total}, OK: {ok_count}, Failed: {fail_count}\nTotal time: {fmt_time(total_elapsed)}\n")
        if log_commands:
            lf.write("\nCommands executed (sample):\n")
            for c in log_commands[:10]:
                lf.write(c + "\n")
        lf.write("\n")

    console.print(f"\n[green]Completed: {ok_count} OK, {fail_count} failed. Log saved to:[/] {log_path}")

if __name__ == "__main__":
    main()