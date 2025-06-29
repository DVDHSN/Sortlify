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

## Screenshots
![image](https://github.com/user-attachments/assets/00fcc1f6-58f8-43c6-973c-8c18c958d678)

- 🪶 **Lightweight**: A clean, modern and lightweight UI built with **PyQt6**

![image](https://github.com/user-attachments/assets/219e2d98-d91f-423c-be64-cecc0f791637)

- 🛠️ **Fine tune custom if-then rules**: Fine-tune the organization logic by creating custom "if-then" rules

![image](https://github.com/user-attachments/assets/455a2cb5-5213-4204-951a-d9037bfb407e)

- 🛠️ **Fine tune Categories**: Define new categories with your chosen file extensions. For example, u can make **".xlsx"** files move to a new folder category called **"Graphs"**

![image](https://github.com/user-attachments/assets/4287806f-d003-4547-bd35-65b243e3b19b)

- ✨ **Beautiful UI**: A clean easy to navigate settings page with an extensive number of options

![image](https://github.com/user-attachments/assets/d2777892-de70-4e27-8f83-7096a25a2d34)

- 🤖 **AI**: View AI-suggested categories based on `scikit-learn` ML algorithm and your past organization history all stored and sorted locally on your PC 

![image](https://github.com/user-attachments/assets/790fdefd-d6f2-4bf2-b958-4a8a7fceb6ae)

- ☕ **Intuitive filtering**: Filter between files with the sidebar as well as the ability to preview images, text based documents, etc.

![Screenshot 2025-06-28 101917](https://github.com/user-attachments/assets/71207fbb-6868-423a-b18e-bfe3a8e9a964)
![Screenshot 2025-06-28 102215](https://github.com/user-attachments/assets/25045fa0-fc65-45b8-b9c0-1bf00e4c7732)
![Screenshot 2025-06-28 101958](https://github.com/user-attachments/assets/f0f04e92-fd47-4ba9-99c9-bd0ea89b325a)
![Screenshot 2025-06-28 101947](https://github.com/user-attachments/assets/cc2f1c08-1b3a-40be-b87b-d597052b6bdd)
![Screenshot 2025-06-28 101929](https://github.com/user-attachments/assets/6a8b76f3-e3e4-44ca-af2f-7deb72096113)

- 🎨 **Theming and Customization**: Make **Sortlify** yours with robust customization options

## 📅 Roadmap

- [ ] Batch renaming with patterns and templates
- [ ] File tagging system for more granular organization beyond just categories
- [ ] Full-text search within documents (PDF, Word, etc.)
- [ ] Metadata filtering (EXIF data for images, ID3 tags for audio)
- [ ] Rules engine for complex organization logic
- [ ] Watch folders for automatic organization
- [ ] File thumbnails for more file types (PDFs, documents)
- [ ] File size visualization (pie charts, bar graphs)
- [ ] AI-Powered Smart Sort (Llama 3.2 Integration) Enable automatic file organization based on semantic understanding of file names and content using Llama 3.2.

   - [ ] Use Llama 3.2 to analyze filenames, document text, and propose custom folder structures

   - [ ] Optional pairing with TinyViT or LLaVA for image classification fallback

   - [ ] “Dry Run” mode to preview changes before applying

   - [ ] Natural language interface: “Organize all invoices by year and client”

   - [ ] Trust feedback system to refine future AI decisions


