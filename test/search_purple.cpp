#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

// Function to filter out all colors except purple and return a binary mask
Mat filterPurpleToBinaryMask(const Mat& image) {
    Mat hsv, mask;

    // Convert the image to HSV color space
    cvtColor(image, hsv, COLOR_BGR2HSV);

    // Define the range for purple color in HSV
    Scalar lower_purple(120, 50, 50); // Lower bound for purple
    Scalar upper_purple(160, 255, 255); // Upper bound for purple

    // Create a binary mask where purple regions are white (255) and others are black (0)
    inRange(hsv, lower_purple, upper_purple, mask);

    // Convert the binary mask to a 0/1 matrix
    mask = mask / 255;

    return mask;
}

// Function to search for purple pixels from the center to the edges
void searchPurpleFromCenter(const Mat& binaryMask) {
    int height = binaryMask.rows;
    int width = binaryMask.cols;

    // Center pixel coordinates
    int centerY = height / 2;
    int centerX = width / 2;

    // Directions to search: (dy, dx)
    vector<pair<string, Point>> directions = {
        {"up", Point(-1, 0)},    // Move upward
        {"down", Point(1, 0)},   // Move downward
        {"left", Point(0, -1)},  // Move left
        {"right", Point(0, 1)}   // Move right
    };

    for (const auto& dir : directions) {
        string direction = dir.first;
        Point delta = dir.second;

        int y = centerY;
        int x = centerX;
        int distance = 0;

        // Search along the direction until the edge of the image
        while (y >= 0 && y < height && x >= 0 && x < width) {
            if (binaryMask.at<uchar>(y, x) == 1) {
                cout << "Purple pixel found " << direction << " at distance " << distance << "." << endl;
                break;
            }

            // Move in the specified direction
            y += delta.y;
            x += delta.x;
            distance++;
        }

        if (y < 0 || y >= height || x < 0 || x >= width) {
            cout << "No purple pixel found " << direction << "." << endl;
        }
    }
}

int main() {
    // Input and output file paths
    string inputImagePath = "input_image.jpg"; // Replace with your input image path
    string outputImagePath = "output.png";     // Replace with your desired output path

    // Read the input image
    Mat image = imread(inputImagePath);

    if (image.empty()) {
        cerr << "Error: Could not open or find the image!" << endl;
        return -1;
    }

    // Filter the image to create a binary mask
    Mat binaryMask = filterPurpleToBinaryMask(image);

    // Save the binary mask as an output image (scaled to 0-255 for visibility)
    Mat outputMask;
    binaryMask.convertTo(outputMask, CV_8U, 255); // Scale 0/1 to 0/255
    imwrite(outputImagePath, outputMask);

    // Search for purple pixels from the center to the edges
    searchPurpleFromCenter(binaryMask);

    cout << "Filtered binary mask saved as " << outputImagePath << endl;

    return 0;
}
