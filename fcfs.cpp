#include <iostream>
using namespace std;

class fcfs {
    public:
        int n;
        float ct[10], tat[10], wt[10], s1, s2, avg_wt, avg_tat;
        string p[10];
        float at[10], bt[10];
        
        fcfs() {
            cout << "\nEnter the number of processes: ";
            cin >> n;
        
            s1 = 0.0;
            s2 = 0.0;
            avg_wt = 0.0;
            avg_tat = 0.0;
        }
            
        void read() {
            for(int i = 0; i < n; i++) {
                cout << "\nEnter name of process: ";
                cin >> p[i];
            
                cout << "Enter arrival time of process: ";
                cin >> at[i];
            
                cout << "Enter burst time of process: ";
                cin >> bt[i];
            }
        }
        
        void calc() {
        
           for(int i = 0; i < n; i++) {
           	 if(i == 0) {
           	 	ct[i] = bt[i];
           	 }
           	 else {
           	 	ct[i] = ct[i-1] + bt[i];
           	 }
        
                tat[i] = ct[i] - at[i];
                wt[i] = tat[i] - bt[i];
                
                s1 = s1 + tat[i];
                s2 = s2 + wt[i];
                
                cout << "\nFor " << p[i] << ":\n";
                cout << "Arrival time: " << at[i] << endl;
                cout << "Burst time: " << bt[i] << endl;
                cout << "Completion time: " << ct[i] << endl;
                cout << "Turnaround time: " << tat[i] << endl;
                cout << "Waiting time: " << wt[i] << endl;
           }
           
           avg_tat  = s1/n;
           avg_wt = s2/n;
           
           cout << "\nAverage turn around time: " << avg_tat << endl;
           cout << "Average waiting time: " << avg_wt << endl;
           
           // Display Gantt chart
           cout << "\nGantt Chart:\n";
           for(int i = 0; i < n; i++) {
               cout << "| " << p[i] << " ";
           }
           cout << "|\n";
           
           for(int i = 0; i < n; i++) {
               cout << "|----";
           }
           cout << "|\n";
           
           for(int i = 0; i < n; i++) {
               cout << "  " << ct[i] << "  ";
           }
           cout << "\n";
       }
};
          
int main() {
    fcfs obj;
    obj.read();
    obj.calc();
}
