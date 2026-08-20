#include <iostream>
#include <string>
#include <bitset>

using namespace std;

int main(){
    string text;
    getline(cin, text);
    for (char c : text){
        cout<<bitset<8>(static_cast<int>(c));
    }
}