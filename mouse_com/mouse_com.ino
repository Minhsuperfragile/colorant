#include <Mouse.h>

void setup() {
  Mouse.begin();
}

void loop() {
  // Move the mouse to a random position on the screen
  int x = random(0, 1920);
  int y = random(0, 1080);
  Mouse.move(x - Mouse.getX(), y - Mouse.getY());
  
  // Click the mouse button
  if (random(0, 2) == 0) {
    Mouse.click();
  }
  
  delay(500); // Wait for half a second before moving again
}
