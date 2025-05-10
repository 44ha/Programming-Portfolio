#include <iostream>
#include <string>
#include <vector>
#include <chrono>

using namespace std;

class Task {
public:
    virtual void show() = 0;
    virtual ~Task() {}
};

class RegularTask : public Task {
    string taskDescription;
public:
    RegularTask(string desc) : taskDescription(desc) {}
    void show() {
        cout << "Regular Task: " << taskDescription << endl;
    }
};

class PriorityTask : public Task {
    string taskDescription;
    int priorityLevel;
public:
    PriorityTask(string desc, int priority) : taskDescription(desc), priorityLevel(priority) {}
    void show() {
        cout << "Priority Task: " << taskDescription << " [Priority: " << priorityLevel << "]" << endl;
    }
};

class TimedTask : public Task {
    string taskDescription;
    chrono::system_clock::time_point dueTime;
public:
    TimedTask(string desc, int duration, bool isInHours) : taskDescription(desc) {
        if (isInHours) {
            dueTime = chrono::system_clock::now() + chrono::hours(duration);
        } else {
            dueTime = chrono::system_clock::now() + chrono::hours(duration * 24);
        }
    }

    void show() {
        auto now = chrono::system_clock::now();
        time_t dueT = chrono::system_clock::to_time_t(dueTime);
        struct tm* dueTm = localtime(&dueT);

        cout << "Timed Task: " << taskDescription << " (Due: " 
             << (dueTm->tm_year + 1900) << "-" << (dueTm->tm_mon + 1) << "-" << dueTm->tm_mday << " "
             << dueTm->tm_hour << ":" << dueTm->tm_min << ":" << dueTm->tm_sec << ") ";

        if (now >= dueTime) {
            cout << "[EXPIRED]" << endl;
        } else {
            auto remainingTime = chrono::duration_cast<chrono::seconds>(dueTime - now);
            int totalSeconds = remainingTime.count();
            int days = totalSeconds / 86400;
            totalSeconds %= 86400;
            int hours = totalSeconds / 3600;
            totalSeconds %= 3600;
            int minutes = totalSeconds / 60;
            int seconds = totalSeconds % 60;

            if (days > 0) {
                cout << "[Time Left: " << days << "d " << hours << "h " << minutes << "m " << seconds << "s]" << endl;
            } else {
                cout << "[Time Left: " << hours << "h " << minutes << "m " << seconds << "s]" << endl;
            }
        }
    }
};

class TaskFactory {
public:
    virtual Task* createTask() = 0;
    virtual ~TaskFactory() {}
};

class RegularTaskFactory : public TaskFactory {
public:
    Task* createTask() {
        string desc;
        cout << "Enter task description: ";
        cin.ignore();
        getline(cin, desc);
        return new RegularTask(desc);
    }
};

class PriorityTaskFactory : public TaskFactory {
public:
    Task* createTask() {
        string desc;
        int priority;
        cout << "Enter task description: ";
        cin.ignore();
        getline(cin, desc);
        cout << "Enter priority level (1-5): ";
        cin >> priority;
        return new PriorityTask(desc, priority);
    }
};

class TimedTaskFactory : public TaskFactory {
public:
    Task* createTask() {
        string desc;
        int duration;
        int timeUnit;
        cout << "Enter task description: ";
        cin.ignore();
        getline(cin, desc);
        cout << "Set duration:\n1. In Days\n2. In Hours\nChoose: ";
        cin >> timeUnit;
        cout << "Enter number of " << (timeUnit == 1 ? "days" : "hours") << ": ";
        cin >> duration;
        return new TimedTask(desc, duration, timeUnit == 2);
    }
};

int main() {
    vector<Task*> tasks;
    int userChoice;
    cout << "To-Do App\n";
    do {
        cout << "\n";
        cout << "1. Add Regular Task\n";
        cout << "2. Add Timed Task\n";
        cout << "3. Add Priority Task\n";
        cout << "4. Show All Tasks\n";
        cout << "5. Exit\n";
        cout << "Enter your choice: \n";
        cin >> userChoice;

        TaskFactory* taskCreator = nullptr;

        switch (userChoice) {
            case 1:
                taskCreator = new RegularTaskFactory();
                break;
            case 2:
                taskCreator = new TimedTaskFactory();
                break;
            case 3:
                taskCreator = new PriorityTaskFactory();
                break;
            case 4:
                if (tasks.empty()) {
                    cout << "No tasks available." << endl;
                } else {
                    for (size_t i = 0; i < tasks.size(); i++) {
                        cout << i + 1 << ". ";
                        tasks[i]->show();
                    }
                }
                break;
            case 5:
                cout << "Exiting..." << endl;
                break;
            default:
                cout << "Invalid choice. Try again." << endl;
        }

        if (taskCreator) {
            Task* newTask = taskCreator->createTask();
            tasks.push_back(newTask);
            delete taskCreator;
        }

    } while (userChoice != 5);

    for (Task* t : tasks) {
        delete t;
    }

    return 0;
}
