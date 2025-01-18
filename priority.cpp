#include <iostream>
#include <algorithm> // For sort
using namespace std;

#define totalprocess 5

struct process {
    int at, bt, pr, pno;
};

process proc[50];

bool comp(process a, process b) {
    if (a.at == b.at) {
        return a.pr < b.pr;
    } else {
        return a.at < b.at;
    }
}

void WaitingTime(int wt[]) {
    int service[50];
    service[0] = proc[0].at;
    wt[0] = 0;

    for (int i = 1; i < totalprocess; i++) {
        service[i] = proc[i - 1].bt + service[i - 1];
        wt[i] = service[i] - proc[i].at;    
    
        if (wt[i] < 0) {
            wt[i] = 0;
        }
    }
}

void TurnAroundTime(int tat[], int wt[]) {
    for (int i = 0; i < totalprocess; i++) {
        tat[i] = proc[i].bt + wt[i];
    }    
}

void find_GanttChart() {
    int wt[10], tat[10];
    float avg_wt = 0, avg_tat = 0;

    WaitingTime(wt);
    TurnAroundTime(tat, wt);
    
    int stime[10], ct[10];
    stime[0] = proc[0].at;             // Start time of the first process
    ct[0] = stime[0] + proc[0].bt;     // Completion time of the first process

    for (int i = 1; i < totalprocess; i++) {
        stime[i] = ct[i - 1];            // Start time of the current process is the completion time of the previous process
        ct[i] = stime[i] + proc[i].bt; // Completion time of the current process
    }
    
    cout << "Process No.\tStart Time\tCompletion Time\tTurnaround Time\t\tWaiting Time" << endl;
        
    for (int i = 0; i < totalprocess; i++) {
        avg_wt += wt[i];
        avg_tat += tat[i];
        
        cout << proc[i].pno << "\t\t" << stime[i] << "\t\t" << ct[i] << "\t\t" << tat[i] << "\t\t\t" << wt[i] << endl;
    }
    
    cout << "Average waiting time: " << avg_wt / (float)totalprocess << endl;
    cout << "Average turnaround time: " << avg_tat / (float)totalprocess << endl;

    // Display Gantt chart
    cout << "\nGantt Chart:\n";
    for (int i = 0; i < totalprocess; i++) {
        cout << "| P" << proc[i].pno << " ";
    }
    cout << "|\n";
    for (int i = 0; i < totalprocess; i++) {
        cout << "|----";
    }
    cout << "|\n";
    for (int i = 0; i < totalprocess; i++) {
        cout << stime[i] << "    ";
    }
    cout << ct[totalprocess - 1] << "\n"; // End time of the last process
}

int main() {
    int arrival_time[] = { 0, 1, 2, 3, 4 };  // Example arrival times
    int burst_time[] = { 4, 5, 1, 2, 3 };    // Example burst times
    int priority[] = { 2, 1, 4, 3, 5 };      // Example priorities

    for (int i = 0; i < totalprocess; i++) {
        proc[i].at = arrival_time[i];
        proc[i].bt = burst_time[i];
        proc[i].pr = priority[i];
        proc[i].pno = i + 1;
    } 
    
    sort(proc, proc + totalprocess, comp);
        
    find_GanttChart(); 

    return 0;
}
