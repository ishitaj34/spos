#include <iostream>
using namespace std;

struct process {
    string p; 
    int at;
    int bt;
};

class ShortestJob {
    public:
        void WaitingTime(process proc[], int n, int wt[], string gantt_p[], int gantt_t[], int& gantt_size) {
            int rt[n];
            for (int i = 0; i < n; i++)
                rt[i] = proc[i].bt;

            int complete = 0, t = 0, minm = INT_MAX;
            int shortest = 0, finish_time;
            bool check = false;
            gantt_size = 0;

            while (complete != n) {
                for (int j = 0; j < n; j++) {
                    if ((proc[j].at <= t) && (rt[j] < minm) && rt[j] > 0) {
                        minm = rt[j];
                        shortest = j;
                        check = true;
                    }
                }

                if (check == false) {
                    t++;
                    continue;
                }

                // Execute the process for 1 unit time
                rt[shortest]--;
                minm = rt[shortest];
                
                // Add process to Gantt chart if it just started or if it changes from a different process
                if (gantt_size == 0 || gantt_p[gantt_size - 1] != proc[shortest].p) {
                    gantt_p[gantt_size] = proc[shortest].p;
                    gantt_t[gantt_size] = t;  // Start time of the process in Gantt chart
                    gantt_size++;
                }
                
                if (minm == 0)
                    minm = INT_MAX;

                if (rt[shortest] == 0) {
                    complete++;
                    check = false;
                    finish_time = t + 1;

                    wt[shortest] = finish_time - proc[shortest].bt - proc[shortest].at;
                    if (wt[shortest] < 0)
                        wt[shortest] = 0;
                }
                t++;
            }
            
            // Add final time for the last process in the Gantt chart
            gantt_t[gantt_size] = t;  // End time of the last executed process
        }

        void TurnAroundTime(process proc[], int n, int wt[], int tat[]) {
            for (int i = 0; i < n; i++)
                tat[i] = proc[i].bt + wt[i];
        }

        void AvgTime(process proc[], int n) {
            int wt[n], tat[n], total_wt = 0, total_tat = 0;
            string gantt_p[2 * n]; // Gantt chart process names
            int gantt_t[2 * n];    // Gantt chart start times
            int gantt_size = 0;

            WaitingTime(proc, n, wt, gantt_p, gantt_t, gantt_size);
            TurnAroundTime(proc, n, wt, tat);

            cout << " P\t\t" << "BT\t\t" << "WT\t\t" << "TAT\t\t\n";

            for (int i = 0; i < n; i++) {
                total_wt = total_wt + wt[i];
                total_tat = total_tat + tat[i];

                cout << " " << proc[i].p << "\t\t" << proc[i].bt << "\t\t " << wt[i] << "\t\t " << tat[i] << endl;
            }

            cout << "\nAverage waiting time: " << (float)total_wt / (float)n;
            cout << "\nAverage turn around time: " << (float)total_tat / (float)n;

            // Display Gantt chart
            cout << "\n\nGantt Chart:\n";
            for (int i = 0; i < gantt_size; i++) {
                cout << "| " << gantt_p[i] << " ";
            }
            cout << "|\n";
            for (int i = 0; i < gantt_size; i++) {
                cout << "|----";
            }
            cout << "|\n";
            for (int i = 0; i <= gantt_size; i++) {
                cout << gantt_t[i] << "    ";
            }
            cout << "\n";
        }
};

int main() {
    ShortestJob obj;

    int n;
    cout << "\nEnter the number of processes: ";
    cin >> n;

    process* proc = new process[n];

    for(int i = 0; i < n; i++) {
        cout << "\nEnter name of process: ";
        cin >> proc[i].p; 
        cout << "Enter arrival time of process: ";
        cin >> proc[i].at;

        cout << "Enter burst time of process: ";
        cin >> proc[i].bt;
    }

    obj.AvgTime(proc, n);

    delete[] proc;
    return 0;
}
