# 📝 Command Pattern Text Editor (C++)

This is a simple **command-line text editor** written in C++ that supports adding, editing, deleting text, and provides **undo/redo functionality** using the **Command design pattern**. You can also **load and save** your work from/to files.

## 🚀 Features

- ✅ Add new lines of text  
- 🛠️ Edit existing lines  
- ❌ Delete specific characters from any line  
- ↩️ Undo and ↪️ Redo any operation  
- 💾 Load and save text from/to a file  
- 📜 Console-based user interface  

## 🧠 Concepts Used

- **Command Design Pattern** — Encapsulates text operations as objects for undo/redo  
- **Stack** — For managing undo and redo functionality  
- **OOP** — Clear separation between responsibilities (`TextManager`, `CommandManager`, etc.)  
- **File I/O** — Load and save text using files  


## 🛠️ How to Build

Make sure you have a C++ compiler installed (e.g. `g++`). Then compile using:

```
g++ -std=c++11 -o text_editor main.cpp
```
Run the editor:

```
./text_editor
```
## 📷 Example Usage


### ▶️ Start the Program

To run the program, compile and execute it. The program will display the available commands and wait for user input.

### ✍️ Adding Text

To add a line of text, use the `add` command followed by the text you want to add:
```
add This is a new line of text.
```

This will add the text to the document, and the program will display the updated text.

### 🗑️ Deleting Text

To delete part of a line of text, use the `delete` command with the line number, starting position, and the number of characters you want to delete:
```
delete 1 5 3
```

This will delete 3 characters starting from position 5 in the first line of text.

### ✏️ Editing Text

To edit a specific line of text, use the `edit` command with the line number and the new text:
```
edit 1 This is the edited line of text.
```

This will replace the entire content of the first line with the new text.

### ⏪ Undoing and Redoing Operations

You can undo or redo the last operation using the `undo` and `redo` commands:
```
undo
```

This will undo the last change, and the program will show the text as it was before the change.

To redo the undone operation, use the `redo` command:
```
redo
```

### 📂 Loading and Saving to/from Files

To load a text file into the program, use the `load` command followed by the file name:
```
load myTextFile.txt
```

This will load the content of the file into the text manager.

To save the current text to a file, use the `save` command followed by the file name:
```
save mySavedText.txt
```

### ❌ Exiting the Program

To exit the application, use the `exit` command:
```
exit
```
