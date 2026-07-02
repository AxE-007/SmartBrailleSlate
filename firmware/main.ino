// firmware/main.ino
// Smart Braille Slate - Core Matrix Scanner for ESP32

const int numRows = 10;
const int numCols = 12;

// GPIO assignments for rows and columns (Mapped for standard ESP32)
int rowPins[numRows] = {13, 14, 27, 26, 25, 33, 32, 35, 34, 39};
int colPins[numCols] = {15, 2, 0, 4, 16, 17, 5, 18, 19, 21, 22, 23};

// 2D Arrays to store current and previous button states
bool currentMatrix[numRows][numCols];
bool previousMatrix[numRows][numCols];

// Debounce timing arrays to prevent false double-clicks
unsigned long lastDebounceTime[numRows][numCols];
unsigned long debounceDelay = 50;

void setup() {
    Serial.begin(115200);
    
    // Initialize columns as outputs and set them HIGH
    for (int i = 0; i < numCols; i++) {
        pinMode(colPins[i], OUTPUT);
        digitalWrite(colPins[i], HIGH);
    }
    
    // Initialize rows as inputs with internal pull-up resistors
    for (int i = 0; i < numRows; i++) {
        pinMode(rowPins[i], INPUT_PULLUP);
    }
    
    // Initialize default state arrays
    for (int r = 0; r < numRows; r++) {
        for (int c = 0; c < numCols; c++) {
            currentMatrix[r][c] = HIGH; // HIGH means unpressed due to pull-up
            previousMatrix[r][c] = HIGH;
            lastDebounceTime[r][c] = 0;
        }
    }
    Serial.println("Smart Braille Slate - ESP32 Matrix Scanner Initialized");
}

void loop() {
    scanMatrix();
}

void scanMatrix() {
    for (int c = 0; c < numCols; c++) {
        // Pull the current column LOW to read it
        digitalWrite(colPins[c], LOW);
        
        for (int r = 0; r < numRows; r++) {
            bool reading = digitalRead(rowPins[r]);
            
            // Check for state change to handle debouncing
            if (reading != previousMatrix[r][c]) {
                lastDebounceTime[r][c] = millis();
            }
            
            if ((millis() - lastDebounceTime[r][c]) > debounceDelay) {
                if (reading != currentMatrix[r][c]) {
                    currentMatrix[r][c] = reading;
                    
                    // LOW means the button is actively pressed by the stylus
                    if (currentMatrix[r][c] == LOW) {
                        Serial.print("Stylus press detected at Row: ");
                        Serial.print(r);
                        Serial.print(" Col: ");
                        Serial.println(c);
                        
                        // This is where the coordinate is mapped to a specific Braille cell bitmask
                    }
                }
            }
            previousMatrix[r][c] = reading;
        }
        
        // Reset the column HIGH before moving to the next column
        digitalWrite(colPins[c], HIGH);
    }
}