# To-Do Application 📝

This is a simple C++ console-based To-Do application. The app allows you to manage your tasks by creating regular, priority, and timed tasks. It utilizes Object-Oriented Programming principles like inheritance and the Factory Design Pattern.

## Features 🌟

- **Regular Task**: A basic task with a description.
- **Priority Task**: A task with a description and priority level (1-5).
- **Timed Task**: A task with a description and a due date (in hours or days), displaying remaining time or indicating if the task has expired.

## Technologies Used 💻

- C++
- Object-Oriented Programming (OOP)
- Factory Design Pattern
- Chrono library for time management

## Getting Started 🚀

### 📦 Installation

To set up and run the To-Do App on your local machine:

```bash
git clone https://github.com/44ha/Programming-Portfolio.git
cd portfolio/projects/Project3
g++ -o todoapp ToDo.cpp
./todoapp
```
## How to Use 🛠️

1. When you start the application, you will see the following menu:
   - **1**: Add Regular Task
   - **2**: Add Timed Task
   - **3**: Add Priority Task
   - **4**: Show All Tasks
   - **5**: Exit

2. Select an option by entering the corresponding number.
3. For each task type, the program will prompt you for additional information such as task description, priority level, or due date.
4. You can view all tasks and their status, including the remaining time for timed tasks or their expiration status.

## Code Overview 📚

### Key Classes

- **Task**: An abstract base class for all task types, with a pure virtual function `show()` for displaying task details.
- **RegularTask**: A class for tasks that only have a description.
- **PriorityTask**: A class for tasks that include a priority level.
- **TimedTask**: A class for tasks with a due date and functionality to track time remaining.
- **TaskFactory**: An abstract factory class for creating tasks.
- **RegularTaskFactory, PriorityTaskFactory, TimedTaskFactory**: Concrete factories that implement the `createTask()` method to create the appropriate task type.

### Task Creation

When you choose to add a task, the program asks for the necessary details:
- **Regular Task**: Just enter a description.
- **Priority Task**: Enter a description and priority (from 1 to 5).
- **Timed Task**: Enter a description and a due date in hours or days.

After adding a task, it will be saved in memory, and you can view all tasks at any time.

## Example 💡

**Menu:**
```bash
1. Add Regular Task
2. Add Timed Task
3. Add Priority Task
4. Show All Tasks
5. Exit
```

**Adding a regular task:**
```bash
Enter task description: Buy groceries
Regular Task: Buy groceries
```

**Adding a timed task:**
```bash
Enter task description: Submit project
Set duration:
1. In Days
2. In Hours
Choose: 1
Enter number of days: 2
Timed Task: Submit project (Due: 2025-05-12 14:30:00) [Time Left: 2d 5h 10m 20s]
```
