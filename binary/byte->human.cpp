#include <iostream>
#include <string>

using namespace std;

int main() {
    string num;
    getline(cin, num);
    int remainder = num.length() % 8;
    if (remainder != 0) {
        num.insert(0, 8 - remainder, '0');
    }

    for (size_t i = 0; i < num.length(); i += 8) {
        string byteString = num.substr(i, 8);
        char c = static_cast<char>(stoi(byteString, nullptr, 2));
        cout << c;
    }
    cout << endl;

    return 0;
}