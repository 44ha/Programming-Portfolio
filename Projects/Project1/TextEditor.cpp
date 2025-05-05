#include <iostream>
#include <vector>
#include <string>
#include <stack>
#include <fstream>
#include <sstream>

using namespace std;

class TextManager {
private:
    vector<string> lines;

public:
    void addText(const string& line) {
        lines.push_back(line);
    }

    void deleteLine(int lineIndex, int startPos, int numChars) {
        if (lineIndex >= 0 && lineIndex < lines.size()) {
            string& line = lines[lineIndex];
            if (startPos >= 0 && startPos < line.length()) {
                line.erase(startPos, min(numChars, static_cast<int>(line.length()) - startPos));
            }
        }
    }

    void editLine(int lineIndex, const string& newText) {
        if (lineIndex >= 0 && lineIndex < lines.size()) {
            lines[lineIndex] = newText;
        }
    }

    void showText() const {
        cout << "-------------\n";
        for (int i = 0; i < lines.size(); ++i) {
            cout << i + 1 << ". " << lines[i] << endl;
        }
        cout << "-------------\n";
    }

    vector<string>& getLines() {
        return lines;
    }

    int getLineCount() const {
        return lines.size();
    }
};

class FileManager {
public:
    void saveToFile(const string& filename, const vector<string>& lines) {
        ofstream file(filename);
        if (file.is_open()) {
            for (const string& line : lines) {
                file << line << endl;
            }
            file.close();
        } else {
            cout << "Unable to save file.\n";
        }
    }

    void loadFromFile(const string& filename, vector<string>& lines) {
        ifstream file(filename);
        if (file.is_open()) {
            string line;
            while (getline(file, line)) {
                lines.push_back(line);
            }
            file.close();
        } else {
            cout << "Unable to open file.\n";
        }
    }
};

class ICommand {
public:
    virtual void execute() = 0;
    virtual void undo() = 0;
    virtual ~ICommand() = default;
};

class AddCommand : public ICommand {
private:
    TextManager& textManager;
    string text;

public:
    AddCommand(TextManager& tm, const string& line) : textManager(tm), text(line) {}

    void execute() override {
        textManager.addText(text);
    }

    void undo() override {
        if (textManager.getLineCount() > 0) {
            textManager.deleteLine(textManager.getLineCount() - 1, 0, text.length());
        }
    }
};

class DeleteCommand : public ICommand {
private:
    TextManager& textManager;
    int lineIndex;
    int startPos;
    int numChars;
    string deletedText;

public:
    DeleteCommand(TextManager& tm, int lineIdx, int start, int num)
        : textManager(tm), lineIndex(lineIdx), startPos(start), numChars(num) {}

    void execute() override {
        if (lineIndex >= 0 && lineIndex < textManager.getLineCount()) {
            string& line = textManager.getLines()[lineIndex];
            if (startPos >= 0 && startPos < line.length()) {
                deletedText = line.substr(startPos, min(numChars, static_cast<int>(line.length()) - startPos));
                textManager.deleteLine(lineIndex, startPos, numChars);
            }
        }
    }

    void undo() override {
        if (!deletedText.empty() && lineIndex >= 0 && lineIndex < textManager.getLineCount()) {
            textManager.getLines()[lineIndex].insert(startPos, deletedText);
        }
    }
};

class EditCommand : public ICommand {
private:
    TextManager& textManager;
    int lineIndex;
    string oldText;
    string newText;

public:
    EditCommand(TextManager& tm, int lineIdx, const string& newLine)
        : textManager(tm), lineIndex(lineIdx), newText(newLine) {}

    void execute() override {
        if (lineIndex >= 0 && lineIndex < textManager.getLineCount()) {
            oldText = textManager.getLines()[lineIndex];
            textManager.editLine(lineIndex, newText);
        }
    }

    void undo() override {
        if (!oldText.empty() && lineIndex >= 0 && lineIndex < textManager.getLineCount()) {
            textManager.editLine(lineIndex, oldText);
        }
    }
};

class CommandManager {
private:
    stack<ICommand*> undoStack;
    stack<ICommand*> redoStack;

public:
    void executeCommand(ICommand* command) {
        command->execute();
        undoStack.push(command);
        while (!redoStack.empty()) redoStack.pop();
    }

    void undo() {
        if (!undoStack.empty()) {
            ICommand* command = undoStack.top();
            undoStack.pop();
            command->undo();
            redoStack.push(command);
        } else {
            cout << "Nothing to undo.\n";
        }
    }

    void redo() {
        if (!redoStack.empty()) {
            ICommand* command = redoStack.top();
            redoStack.pop();
            command->execute();
            undoStack.push(command);
        } else {
            cout << "Nothing to redo.\n";
        }
    }

    ~CommandManager() {
        while (!undoStack.empty()) {
            delete undoStack.top();
            undoStack.pop();
        }
        while (!redoStack.empty()) {
            delete redoStack.top();
            redoStack.pop();
        }
    }
};

int main() {
    TextManager textManager;
    FileManager fileManager;
    CommandManager commandManager;
    string command;
    bool showInstructions = true;

    while (true) {
        if (showInstructions) {
            cout << "Commands:\nadd <text>\ndelete <line> <start> <length>\nedit <line> <new text>\nshow\nundo\nredo\nload <file>\nsave <file>\nexit\n";
            showInstructions = false;
        }

        cout << "Enter command: ";
        getline(cin, command);

        if (command.substr(0, 3) == "add") {
            if (command.length() > 4) {
                string text = command.substr(4);
                commandManager.executeCommand(new AddCommand(textManager, text));
                textManager.showText();
            } else {
                cout << "No text provided for add.\n";
            }
        } else if (command.substr(0, 6) == "delete") {
            stringstream ss(command.substr(7));
            int lineIndex, start, length;
            if (ss >> lineIndex >> start >> length) {
                commandManager.executeCommand(new DeleteCommand(textManager, lineIndex - 1, start, length));
                textManager.showText();
            } else {
                cout << "Invalid input for delete. Example: delete 2 4 5\n";
            }
        } else if (command.substr(0, 4) == "edit") {
            size_t space = command.find(' ', 5);
            if (space != string::npos) {
                int lineIndex = stoi(command.substr(5, space - 5));
                string newText = command.substr(space + 1);
                commandManager.executeCommand(new EditCommand(textManager, lineIndex - 1, newText));
                textManager.showText();
            } else {
                cout << "Invalid input for edit. Example: edit 1 new text here\n";
            }
        } else if (command == "show") {
            textManager.showText();
        } else if (command == "undo") {
            commandManager.undo();
            textManager.showText();
        } else if (command == "redo") {
            commandManager.redo();
            textManager.showText();
        } else if (command.substr(0, 4) == "load") {
            fileManager.loadFromFile(command.substr(5), textManager.getLines());
        } else if (command.substr(0, 4) == "save") {
            fileManager.saveToFile(command.substr(5), textManager.getLines());
        } else if (command == "exit") {
            break;
        } else {
            cout << "Unknown command.\n";
        }
    }

    return 0;
}    
