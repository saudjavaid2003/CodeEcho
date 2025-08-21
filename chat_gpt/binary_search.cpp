#include <iostream>
#include <vector>
using namespace std;

// Function to perform binary search on a sorted vector
int binarySearch(const vector<int>& arr, int target) {
    int left = 0;
    int right = arr.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) {
            return mid;
        }
        if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1; // Target not found
}

int main() {
    vector<int> data = {1, 3, 5, 7, 9, 11, 13};
    int target;
    cout << "Enter the number to search: ";
    cin >> target;
    int result = binarySearch(data, target);
    if (result != -1) {
        cout << "Element found at index: " << result << endl;
    } else {
        cout << "Element not found." << endl;
    }
    return 0;
}
