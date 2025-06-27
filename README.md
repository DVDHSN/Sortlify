# 📁 Sortlify

**Sortlify** is a modern, AI-powered file organizer built with **Python** and **PyQt6**. It's designed to bring smart, recursive, and elegant automation to your workspace, allowing you to clean up entire directory trees with a single click.

---

## 🌟 Core Features

- 📂 **Recursive Folder Scanning**  
  Select a parent folder, and Sortlify will scan through all subfolders to find and organize every file within(WIP)

- 📝 **Interactive Preview & Organize Workflow**  
  Browse and select a folder to see an interactive preview of how your files will be organized. You can change the target category for any file before committing. No files are moved until you click "Organize".

- 🤖 **AI-Powered Category Suggestions**  
  Sortlify uses a `scikit-learn` model to suggest categories for your files based on their name and content, helping you make smarter organization decisions.

- 🎨 **Themed UI**  
  Switch between several modern themes (blue, green, orange, purple, red) to customize the app's appearance.

- 🛠 **Custom Rules & Categories**  
  Fine-tune the organization logic by creating custom "if-then" rules and defining new categories with your chosen file extensions.

---

## 🧬 Cross-Platform Compatibility

Powered by **PyQt6**, Sortlify runs smoothly across major platforms with a native feel:

- **Windows**: Optimized with native dialogs and controls.
- **macOS**: Retina-ready UI with macOS-style behavior.
- **Linux**: Supports KDE/GNOME with system theme integration.

> All core features work seamlessly across platforms.
> - To run on Windows, download the `.exe` file from the latest release.
> - For macOS/Linux users, follow the installation instructions below.

---

## 🚀 Getting Started

### 📦 Prerequisites

- Python **3.10+**
- `pip` for package installation

### 🧰 Installation & Usage

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/DVDHSN/sortlify.git
    cd sortlify
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```bash
    python sortlify.py
    ```

### 🏗 Build an Executable (Optional)

You can bundle Sortlify into a single executable using PyInstaller.

```bash
# Example for building on any platform
pyinstaller --onefile --windowed --name Sortlify sortlify.py
```

Your executable will be created in the `dist/` folder.

---

## 🪪 License

This project is licensed under the MIT License. See the `LICENSE` file for full details.
