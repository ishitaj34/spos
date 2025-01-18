#include <iostream>
using namespace std;

void WaitingTime(int processes[], int n, int bt[], int wt[], int quantum, int st[], int et[], int order[], int &index) {
    int rem_bt[n];               // Copy of burst times to store remaining burst times.
    for (int i = 0; i < n; i++)
        rem_bt[i] = bt[i];

    int t = 0;                   // Current time
    
    while (1) {
        bool done = true;

        for (int i = 0; i < n; i++) {
            if (rem_bt[i] > 0) {
                done = false;    // There is a pending process
                
                st[index] = t;   // Start time for this process in this cycle
                order[index] = processes[i]; // Track the process number in the Gantt chart

                if (rem_bt[i] > quantum) {
                    t += quantum;
                    rem_bt[i] -= quantum;
                } else {
                    t = t + rem_bt[i];
                    wt[i] = t - bt[i];
                    rem_bt[i] = 0;
                }

                et[index] = t;   // End time for this process in this cycle
                index++;          // Move to the next index for the next entry in Gantt chart
            }
        }
        if (done == true)
            break;
    }
}

void TurnAroundTime(int processes[], int n, int bt[], int wt[], int tat[]) {
    for (int i = 0; i < n; i++)
        tat[i] = bt[i] + wt[i];
}

void AvgTime(int processes[], int n, int bt[], int quantum) {
    int wt[n], tat[n], total_wt = 0, total_tat = 0;
    int st[50], et[50], order[50], index = 0; // Arrays for Gantt chart start and end times

    WaitingTime(processes, n, bt, wt, quantum, st, et, order, index);
    TurnAroundTime(processes, n, bt, wt, tat);

    cout << "PN" << "\tBT" << "\t WT" << "\t\t TAT \n";
    for (int i = 0; i < n; i++) {
        total_wt = total_wt + wt[i];
        total_tat = total_tat + tat[i];

        cout << " " << processes[i] << "\t" << bt[i] << "\t " << wt[i] << "\t\t " << tat[i] << endl;
    }

    cout << "Average waiting time: " << (float)total_wt / (float)n << endl;
    cout << "Average turn around time: " << (float)total_tat / (float)n << endl;

    // Display Gantt chart
    cout << "\nGantt Chart:\n";
    for (int i = 0; i < index; i++) {
        cout << "| P" << order[i] << " ";
    }
    cout << "|\n";

    for (int i = 0; i < index; i++) {
        cout << st[i] << "\t";
    }
    cout << et[index - 1] << "\n";
}

int main() {
    int processes[] = {1, 2, 3};
    int n = sizeof processes / sizeof processes[0];
    int burst_time[] = {10, 5, 8};
    int quantum = 2;

    AvgTime(processes, n, burst_time, quantum);
    return 0;
}
