import os
import requests
from urllib.parse import urlparse
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
from rich.text import Text
import pyfiglet
from time import sleep

console = Console()

def display_banner():
    try:
        banner_text = pyfiglet.figlet_format("Neer Extractor", font="small")
    except:
        banner_text = "=== Neer Extractor ==="
        
    colored_banner = Text(banner_text, style="bold blue")
    
    console.print(Panel(
        colored_banner, 
        box=box.DOUBLE, 
        border_style="blue",
        title="[bold white] v2.0 [/bold white]",
        subtitle="[bold yellow] 🔔 YouTube: https://youtube.com/@hackerneer [/bold yellow]"
    ))
    
    desc = Text("🌐 URL to Source Code Extractor\nExtract Front-End Source Code with Neer's Technology!", style="bold cyan", justify="center")
    console.print(Panel(desc, box=box.ROUNDED, border_style="blue"))
    console.print()

def get_valid_filename(url):
    # URL se domain name nikal kar usko file name banayenge (e.g. google.com.html)
    domain = urlparse(url).netloc
    if not domain:
        domain = "extracted_page"
    # Remove any special characters that can't be in a filename
    domain = domain.replace("www.", "").replace("/", "_")
    return f"neer_{domain}_source.html"

def extract_source(url):
    # User-Agent dalna zaroori hai warna kuch sites block kar deti hain
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    with Progress(
        SpinnerColumn(spinner_name="dots2"),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("[blue]🌍 Neer Connecting to Server...", total=None)
        sleep(0.5)
        
        try:
            # Website se data fetch kar rahe hain
            progress.update(task, description="[cyan]📦 Downloading Source Code with Neer Engine...")
            response = requests.get(url, headers=headers, timeout=10)
            
            # Agar website ne error diya (like 404 Not Found)
            response.raise_for_status()
            
            progress.update(task, description="[green]📝 Neer Saving to file...")
            sleep(0.5)
            
            filename = get_valid_filename(url)
            
            # File save kar rahe hain
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
                
            return filename, len(response.text)
            
        except requests.exceptions.MissingSchema:
            progress.update(task, description="[red]❌ Error: Invalid URL (Add http:// or https://)[/red]")
            sleep(1)
            return None, 0
        except Exception as e:
            progress.update(task, description=f"[red]❌ Neer Connection Error: {e}[/red]")
            sleep(1)
            return None, 0

def format_size(size):
    for unit in ['B', 'KB', 'MB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} GB"

def main():
    console.clear()
    display_banner()
    
    target_url = Prompt.ask("[bold blue]🔗 Enter Website URL (e.g., https://example.com)[/bold blue]")
    
    if not target_url.startswith("http"):
        target_url = "https://" + target_url
        console.print(f"[dim]Auto-added https:// -> {target_url}[/dim]\n")
    
    console.print()
    filename, size = extract_source(target_url)
    
    if filename:
        console.print(Panel(
            f"🎉 [bold green]Source Code Extracted with Neer![/bold green] 🎉\n\n"
            f"🎯 [bold cyan]Target URL:[/bold cyan] [yellow]{target_url}[/yellow]\n"
            f"💾 [bold cyan]Saved File:[/bold cyan] [yellow]{filename}[/yellow]\n"
            f"📏 [bold cyan]File Size:[/bold cyan]  [yellow]{format_size(size)}[/yellow]\n\n"
            f"💡 [dim]Tip: You can now protect this file using Neer Protect![/dim]\n"
            f"📺 [dim]Subscribe: https://youtube.com/@hackerneer[/dim]",
            box=box.HEAVY,
            border_style="green",
            title="[bold white]✨ Neer Extractor Result ✨[/bold white]"
        ))
    
    another = Prompt.ask("\n[bold blue]🔄 Extract another website with Neer?[/bold blue]", choices=["y", "n"], default="n")
    if another.lower() == 'y':
        main()
    else:
        console.print("\n[bold blue]💧 Thanks for using Neer Extractor! Stay Secure. 🔒[/bold blue]\n")
        console.print("[dim]📺 Subscribe: https://youtube.com/@hackerneer[/dim]\n")
        console.print("[dim]© 2026 Neer Security Labs - All Rights Reserved[/dim]\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]👋 Neer Extractor exited. Stay safe![/yellow]")