#include <iostream>
#include <string>

using namespace std;

int main() {
    float value;
    cin >> value;
    int cents = static_cast<int>(value * 100);
    cout<<"quarters: "<<  cents/25<<endl<<"dimes: "<< (cents%25)/10<<endl<<"nickels: "<< (cents%10)/5<<endl<<"pennies: "<< cents%5<<endl;
    return 0;
}