import os
import base64
import zlib
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich import box
from rich.text import Text
import pyfiglet
from time import sleep

console = Console()
OUTPUT_PREFIX = "neerprotected_"

def protect_html(html_code):
    compressed = zlib.compress(html_code.encode("utf-8"), level=9)
    encoded = base64.b64encode(compressed).decode()
    
    protected = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Protected by Neer Protect</title>
</head>
<body>
<script>
(function(){{
const data = "{encoded}";
async function decode(){{
    const binary = atob(data);
    const bytes = new Uint8Array(binary.length);
    for(let i = 0; i < binary.length; i++) {{
        bytes[i] = binary.charCodeAt(i);
    }}
    const stream = new DecompressionStream("deflate");
    const writer = stream.writable.getWriter();
    writer.write(bytes);
    writer.close();
    const buffer = await new Response(stream.readable).arrayBuffer();
    return new TextDecoder().decode(buffer);
}}
decode().then(html => {{
    document.open();
    document.write(html);
    document.close();
}});
}})();
</script>
</body>
</html>
"""
    return protected

def get_html_files():
    current_folder = Path(".")
    html_files = [
        f for f in current_folder.glob("*.html")
        if not f.name.startswith(OUTPUT_PREFIX) and not f.name.startswith("protected_")
    ]
    return sorted(html_files, key=lambda x: x.name)

def display_banner():
    try:
        banner_text = pyfiglet.figlet_format("Neer Protect", font="small")
    except:
        banner_text = "=== Neer Protect ==="
        
    colored_banner = Text(banner_text, style="bold blue")
    
    console.print(Panel(
        colored_banner, 
        box=box.DOUBLE, 
        border_style="blue",
        title="[bold white] v2.0 [/bold white]",
        subtitle="[bold yellow] 🔔 YouTube: https://youtube.com/@hackerneer [/bold yellow]"
    ))
    
    desc = Text("🔒 Advanced HTML/CSS/JS Protection Tool\nSecure your source code with Neer's military-grade encryption!", style="bold cyan", justify="center")
    console.print(Panel(desc, box=box.ROUNDED, border_style="blue"))
    console.print()

def display_stats(html_files):
    total_files = len(html_files)
    total_size = sum(f.stat().st_size for f in html_files)
    
    stats_table = Table(box=box.MINIMAL_DOUBLE_HEAD, border_style="cyan", show_header=False)
    stats_table.add_column("Metric", style="bold blue")
    stats_table.add_column("Value", style="bold white")
    
    stats_table.add_row("📁 HTML Files Found :", str(total_files))
    stats_table.add_row("💾 Total Size       :", format_size(total_size))
    stats_table.add_row("🎯 Output Prefix    :", f"[cyan]{OUTPUT_PREFIX}[/cyan]")
    stats_table.add_row("🏷️  Branding         :", "[bold blue]Neer Protect™[/bold blue]")
    
    console.print(Panel(stats_table, title="📊 [bold white]Neer Protect Statistics[/bold white]", box=box.ROUNDED, border_style="cyan", expand=False))
    console.print()

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def display_files_table(html_files):
    if not html_files:
        console.print(Panel("[red]⚠️ No unprotected HTML files found![/red]\n[yellow]Please place your .html files in this directory.[/yellow]", box=box.HEAVY, border_style="red"))
        return False
    
    table = Table(title="[bold cyan]📄 Available HTML Files[/bold cyan]", box=box.SIMPLE_HEAVY, border_style="blue")
    table.add_column("ID", style="bold red", justify="center")
    table.add_column("Filename", style="bold green")
    table.add_column("Size", style="bold yellow", justify="right")
    
    for idx, file in enumerate(html_files, start=1):
        size = format_size(file.stat().st_size)
        table.add_row(f"[{idx}]", file.name, size)
    
    console.print(table)
    console.print()
    return True

def show_file_preview(file_path):
    try:
        content = file_path.read_text(encoding='utf-8')
        preview_length = min(300, len(content))
        
        preview_text = content[:preview_length]
        if len(content) > preview_length:
            preview_text += "\n\n... [dim](Preview truncated)[/dim]"
            
        preview_panel = Panel(
            preview_text,
            title=f"📖 [bold blue]Preview: {file_path.name}[/bold blue]",
            border_style="blue",
            box=box.ROUNDED,
            padding=(1, 2)
        )
        console.print(preview_panel)
        console.print()
    except Exception as e:
        console.print(f"[red]❌ Error loading preview: {e}[/red]")

def protect_with_animation(selected_file):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("[blue]🔒 Neer Protect Initializing...", total=100)
        
        try:
            html_code = selected_file.read_text(encoding='utf-8')
            progress.update(task, advance=20, description="[cyan]📦 Reading Source Code...")
            sleep(0.4)
            
            protected_html = protect_html(html_code)
            progress.update(task, advance=50, description="[blue]🔐 Neer Encryption Engine Active...")
            sleep(0.6)
            
            output_name = OUTPUT_PREFIX + selected_file.stem + ".html"
            Path(output_name).write_text(protected_html, encoding='utf-8')
            progress.update(task, advance=30, description="[green]✅ Protected with Neer Shield!")
            sleep(0.4)
            
            return output_name
            
        except Exception as e:
            progress.update(task, description=f"[red]❌ Neer Error: {e}[/red]")
            sleep(1)
            return None

def display_protection_result(original_file, output_name, original_size, new_size):
    result_table = Table(box=box.SIMPLE, show_header=False)
    result_table.add_column("Property", style="bold cyan")
    result_table.add_column("Value", style="bold white")
    
    result_table.add_row("📄 Original File :", original_file.name)
    result_table.add_row("💾 Output File   :", f"[bold green]{output_name}[/bold green]")
    result_table.add_row("📏 Original Size :", format_size(original_size))
    result_table.add_row("🔒 Protected Size:", format_size(new_size))
    result_table.add_row("🏷️  Protection    :", "[bold blue]Neer Protect™[/bold blue]")
    
    console.print(Panel(
        result_table,
        title="✨ [bold green]Neer Protect Success[/bold green] ✨",
        box=box.HEAVY,
        border_style="green",
        expand=False
    ))
    console.print(f"[bold blue]💧 Neer Shield Active:[/bold blue] [yellow]{Path(output_name).absolute()}[/yellow]\n")
    console.print("[bold cyan]🔒 This file is now protected by Neer's encryption layer.[/bold cyan]")
    console.print("[dim]📺 Subscribe: https://youtube.com/@hackerneer[/dim]\n")

def main():
    console.clear()
    display_banner()
    
    html_files = get_html_files()
    if not display_files_table(html_files):
        return
    
    display_stats(html_files)
    
    while True:
        try:
            choice = IntPrompt.ask(
                "[bold blue]📌 Enter file ID to protect with Neer[/bold blue]",
                choices=[str(i) for i in range(1, len(html_files) + 1)],
                show_choices=False
            )
            if 1 <= choice <= len(html_files):
                selected_file = html_files[choice - 1]
                break
        except Exception:
            console.print("[red]❌ Invalid ID! Try again.[/red]")
    
    console.print(f"\n[bold cyan]➜ Selected:[/bold cyan] [white]{selected_file.name}[/white]")
    
    show_preview = Prompt.ask("[dim]Show file preview?[/dim]", choices=["y", "n"], default="n")
    if show_preview.lower() == 'y':
        console.print()
        show_file_preview(selected_file)
    
    confirm = Prompt.ask("\n[bold yellow]⚡ Protect with Neer Shield?[/bold yellow]", choices=["y", "n"], default="y")
    if confirm.lower() != 'y':
        console.print("[yellow]❌ Operation cancelled.[/yellow]")
        return
    
    original_size = selected_file.stat().st_size
    output_name = protect_with_animation(selected_file)
    
    if output_name:
        new_size = Path(output_name).stat().st_size
        console.print()
        display_protection_result(selected_file, output_name, original_size, new_size)
    else:
        console.print(Panel("[red]❌ Neer Protection Failed![/red]", box=box.HEAVY, border_style="red"))
    
    another = Prompt.ask("[bold blue]🔄 Protect another file?[/bold blue]", choices=["y", "n"], default="n")
    if another.lower() == 'y':
        main()
    else:
        console.print("\n[bold blue]💧 Thanks for choosing Neer Protect! Stay Secure. 🔒[/bold blue]\n")
        console.print("[dim]📺 Subscribe: https://youtube.com/@hackerneer[/dim]\n")
        console.print("[dim]© 2026 Neer Security Labs - All Rights Reserved[/dim]\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]👋 Neer Protect exited. Stay safe![/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Neer Error: {e}[/red]")