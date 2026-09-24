# Touchless HCI System Using Real-Time Computer Vision and Hand Gesture Recognition

> **CSE Mini Project** | **Team Size:** 3 Members  
> **One-Line Summary:** A webcam-based touchless Human-Computer Interaction (HCI) system that converts hand movements into system commands using computer vision, gesture recognition algorithms, and OS-level control.

---

## 📌 1. Project Overview

This project implements a touchless Human-Computer Interaction (HCI) interface that enables users to control system actions via hand gestures captured using a standard webcam. By processing video frames in real time, the system detects hand landmarks, recognizes geometric gestures, converts them into unified control commands, and executes corresponding operating system operations.

```
       👋 Hand 
          │
          ▼
      📷 Webcam
          │
   👁️ Hand Detection (Part 1)
          │
   📍 21 Landmarks
          │
  🧠 Gesture Recognition (Part 2)
          │
    📋 Standard Command
          │
     💻 OS Action (Part 3)
```

### Example Workflow
1. User performs a **Pinch** gesture in front of the camera.
2. MediaPipe tracks and extracts 21 key hand landmarks.
3. The Gesture Engine processes landmark vector coordinates and yields `PINCH`.
4. The system translates `PINCH` into the standardized `LEFT_CLICK` command.
5. The OS module triggers a left mouse click on the host operating system.

---

## 🎯 2. Objectives & Scope

The core objective is to build a modular software prototype where:
$$\text{Hand Movement} \longrightarrow \text{Gesture} \longrightarrow \text{Command} \longrightarrow \text{OS Action}$$

### Key Technical Concepts Demonstrated
* **Computer Vision:** Video stream capture, frame manipulation, color space transformations using OpenCV.
* **AI & Vision Models:** 3D hand landmark localization using MediaPipe Hand Tracking.
* **Gesture Recognition:** Geometric feature extraction (distances, angles, vectors) and optional ML classification.
* **Human-Computer Interaction (HCI):** Real-time touchless UI controls, debouncing, coordinate normalization.
* **OS & Systems Programming:** Process handling, signal management (`trap`, `kill`), execution scripting (Bash/Linux).
* **Software Engineering:** Decoupled modular design, Git branching models, independent sub-module unit testing.

---

## 🏗️ 3. Architecture & Modular Boundary

To ensure parallel development among 3 team members, the system strictly separates concerns into three decoupled layers:

```
┌────────────────────────────────────────────────────────┐
│                        USER                            │
│                  ✋ Hand Gesture                       │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                       PART 1                           │
│             👁️ VISION / HAND TRACKING                 │
│                                                        │
│       Webcam ──> OpenCV ──> MediaPipe                  │
│       OUTPUT: 21 (x, y, z) Hand Landmarks              │
└───────────────────────────┬────────────────────────────┘
                            │ [Landmarks Data]
                            ▼
┌────────────────────────────────────────────────────────┐
│                       PART 2                           │
│             🧠 GESTURE RECOGNITION                     │
│                                                        │
│       Landmarks ──> Vector Features ──> Gesture        │
│       OUTPUT: Standard Command (e.g., "LEFT_CLICK")    │
└───────────────────────────┬────────────────────────────┘
                            │ [Standardized Command]
                            ▼
┌────────────────────────────────────────────────────────┐
│                       PART 3                           │
│             💻 OS / SYSTEM INTEGRATION                 │
│                                                        │
│       Command ──> OS Signals / Actions                 │
│       OUTPUT: Mouse/Keyboard Input, Script Execution   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                      HOST OS                           │
│          Mouse / Keyboard / System Process             │
└────────────────────────────────────────────────────────┘
```

### 🔌 Input / Output Interface Contracts

| Component | Responsibility | Standard Input | Standard Output |
| :--- | :--- | :--- | :--- |
| **Part 1 (Vision)** | Capture frame & locate hand keypoints | Video Stream Frame | `List[Tuple[float, float, float]]` (21 Landmarks) |
| **Part 2 (Gesture)** | Compute geometric features & map to intent | 21 Landmark Coordinates | `String` or `Dict` (e.g., `{"command": "MOVE", "x": 0.5, "y": 0.4}`) |
| **Part 3 (System)** | Execute native OS instructions | Standardized Command String / Object | System event (Mouse click, key combination, signal) |

> ⚠️ **Strict Design Rule:** Do not cross module boundaries. Part 1 must not handle gesture logic; Part 2 must not manage Linux processes; Part 3 must operate without MediaPipe dependencies.

---

## 👤 5. Module Breakdown & Specifications

### 👁️ Part 1: Vision / Hand Tracking
* **Owner:** Team Member 1
* **Directory:** `vision/`
* **Technologies:** Python, OpenCV, MediaPipe, NumPy
* **Key Tasks:**
  * Initialize webcam stream via OpenCV.
  * Execute MediaPipe Hands pipeline to extract 21 keypoints per detected hand.
  * Normalize $x, y \in [0.0, 1.0]$ based on frame dimensions, with relative $z$ depth.
  * Render real-time visual feedback and display current FPS.
```
* **Input:**
  
      📷 Camera
          ↓
        Frame
          ↓
      MediaPipe
```
```
Landmark Skeleton Index Reference:
             8 ● (Index Tip)
               │
             7 ●
               │
             6 ●
               │
             5 ● ──── 9 ● ─── 13 ● ─── 17 ●
        4 ●────┘
       /
  0 ● (Wrist)
```

---

### 🧠 Part 2: Gesture Recognition Engine
* **Owner:** Team Member 2
* **Directory:** `gestures/`
* **Technologies:** Python, NumPy, Geometry/Vector Math, Scikit-learn (Optional ML)
* **Key Tasks:**
  * Calculate euclidean distances between fingertip landmarks and palm joints.
  * Derive joint angles using dot product vector formulas:
    $$\theta = \arccos\left(\frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}\right)$$
  * Apply rule-based decision logic or ML classification models (KNN / Random Forest).
  * Package commands with contextual data (e.g., normalized coordinates for movement).

#### Initial Gesture-to-Command Matrix

| Physical Gesture | Target Command | Description |
| :--- | :--- | :--- |
| **Pinch** (Index + Thumb) | `LEFT_CLICK` | Triggers primary click action |
| **Point** (Index extended) | `MOVE` | Passes `(x, y)` coordinate updates |
| **Open Palm** | `PAUSE` | Temporarily halts command execution |
| **Fist** | `STOP` | Signals system process termination |
| **Swipe Left** | `SWIPE_LEFT` | Previous item / browser back |
| **Swipe Right** | `SWIPE_RIGHT` | Next item / browser forward |

---

### 💻 Part 3: OS / System Integration
* **Owner:** Team Member 3
* **Directory:** `system/`, `scripts/`
* **Technologies:** Python, PyAutoGUI / xdotool, Bash, Linux process controls
* **Key Tasks:**
  * Map command strings (`LEFT_CLICK`, `MOVE`, etc.) to OS input events.
  * Handle background process execution, signal management (`SIGINT`, `SIGTERM`), and shell wrappers (`run.sh`).
  * Implement system debouncing (preventing duplicate click firings within $N$ milliseconds).
  * Ensure process cleanup using `trap` directives in shell scripts.

#### Native Command Mapping

| System Command | Executed System Action |
| :--- | :--- |
| `LEFT_CLICK` | Perform native left click |
| `RIGHT_CLICK` | Perform native right click |
| `MOVE` | Set OS cursor position to $(x \cdot \text{screen\_width}, y \cdot \text{screen\_height})$ |
| `SCROLL_UP` / `DOWN` | Send mouse wheel movement signals |
| `SWIPE_LEFT` / `RIGHT` | Execute key bindings (`Alt + Left Arrow` / `Alt + Right Arrow`) |
| `PAUSE` | Toggle system command receiver state |
| `STOP` | Gracefully release hardware resources and exit process |

---

## 📁 14. Repository Structure

```text
touchless-hci/
├── vision/
│   ├── __init__.py
│   └── hand_tracking.py      # Part 1: Webcam capture & MediaPipe tracking
├── gestures/
│   ├── __init__.py
│   └── gesture_classifier.py # Part 2: Feature extraction & gesture logic
├── system/
│   ├── __init__.py
│   └── command_executor.py   # Part 3: Native OS event triggers
├── tests/
│   ├── test_vision.py        # Unit tests for stream and detection
│   ├── test_gestures.py      # Tests using mock landmark inputs
│   └── test_system.py        # OS event execution verification
├── scripts/
│   └── run.sh                # Linux launch & process management script
├── main.py                   # Central pipeline integration loop
├── requirements.txt          # Python dependencies
├── .gitignore                # Git exclusions
└── README.md                 # Project documentation
```

---

## 🚀 Getting Started & Execution

### Prerequisites
* Python 3.8 or higher
* Linux / Ubuntu (or WSL2 with X11/Wayland forwarding on Windows)
* Integrated or USB Webcam

### Installation

1. **Clone the repository:**
   ```bash
   git clone <REPOSITORY_URL>
   cd touchless-hci
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Execution Options

* **Run via Bash Launcher (Recommended for Linux):**
  ```bash
  chmod +x scripts/run.sh
  ./scripts/run.sh
  ```

* **Run Direct Integration Script:**
  ```bash
  python main.py
  ```

* **Run Individual Modules for Testing:**
  ```bash
  python vision/hand_tracking.py      # Test camera & landmarks
  python gestures/gesture_classifier.py # Test gesture detection with mock data
  python system/command_executor.py   # Test direct OS actions
  ```

---

## 🧪 Testing Strategy

Each subsystem can be tested independently without hardware or cross-module dependencies:

1. **Vision Module (`test_vision.py`):** Asserts frame retrieval, checks array shapes, verifies 21 landmark output tuples.
2. **Gesture Module (`test_gestures.py`):** Feeds predefined synthetic landmark matrices to verify that expected gesture strings and parameters are generated correctly.
3. **System Module (`test_system.py`):** Issues isolated commands directly to verify that OS actions (e.g., cursor repositioning, click triggers) perform without exceptions.
4. **End-to-End Integration:** Runs `main.py` to confirm the full pipeline:
   $$\text{Webcam Frame} \xrightarrow{\quad} \text{Landmarks} \xrightarrow{\quad} \text{Gesture} \xrightarrow{\quad} \text{Command} \xrightarrow{\quad} \text{OS Action}$$

---

## 🛠️ Git & Workflow Rules

To maintain repository integrity during multi-developer workflows:

* **Branch Naming Conventions:**
  * Part 1: `feature/vision`
  * Part 2: `feature/gesture`
  * Part 3: `feature/linux`
* **Development Practices:**
  * Always run `git pull origin main` before starting new edits.
  * Work strictly inside your assigned directory module.
  * Write clear, imperative commit messages (e.g., `Add pinch gesture debouncing logic`).
* **Exclusions:** Never commit `.venv/`, `__pycache__/`, `.pyc`, or hardware recording binaries.

---

## 📅 Roadmap & Milestones

- [x] **Phase 1: Architecture & Interface Design** (Decoupled input/output specifications defined)
- [ ] **Phase 2: Subsystem Development** (Independent creation of `vision`, `gestures`, and `system` modules)
- [ ] **Phase 3: Initial Integration** (Single-gesture end-to-end pipeline: `PINCH` $\rightarrow$ `LEFT_CLICK`)
- [ ] **Phase 4: Gesture Set Expansion** (Implementation of `MOVE`, `SWIPE`, `PAUSE`, `STOP`)
- [ ] **Phase 5: System Refinement** (Coordinate smoothing, action debouncing, error handling, `trap` exit signals)
- [ ] **Optional Upgrade:** Replace rule-based gesture detection with a trained machine learning model (KNN / SVM).

---

## ✅ Definition of "Done"

* [ ] Hand landmark tracker outputs 21 normalized coordinates at $\ge 20$ FPS.
* [ ] Gesture classification module correctly resolves at least 3 distinct hand shapes/movements.
* [ ] Command executor translates commands into real-time OS actions.
* [ ] Shell execution script (`run.sh`) successfully manages execution and clean termination.
* [ ] Complete system demo successfully demonstrates touchless interaction through the end-to-end pipeline.
