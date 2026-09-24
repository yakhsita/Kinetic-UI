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
Input:
  
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
```
Output
  
The module should provide landmark coordinates such as:

[
    (0.52, 0.81, 0.03),
    (0.48, 0.74, 0.01),
    (0.45, 0.67, 0.00),
    ...
]

Each landmark contains approximately:

(x, y, z)

The exact values will change depending on the hand position.
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
```
Input:

Part 2 receives: 21 hand landmarks

For example:
[
    (0.52, 0.81, 0.03),
    (0.48, 0.74, 0.01),
    ...
]
```

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
  * **Windows users**
      * If someone is working on Windows but needs Linux functionality, they can use:
              WSL2 + Ubuntu
        Part 1 and Part 2 can remain on Windows.
```
Input:

"LEFT_CLICK"
"SWIPE_LEFT"
"PAUSE"

```

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

## 🚀 Getting Started w Git & GitHub & Execution

### Prerequisites
* Python 3.8 or higher
* Linux / Ubuntu (or WSL2 with X11/Wayland forwarding on Windows)
* Integrated or USB Webcam

### Git commands

1. **Clone the repository:**
   ```bash
   git clone <REPOSITORY_URL>
   cd touchless-hci
   ```

2. **Get the latest changes**
   Before starting work:
   ```bash
   git pull
   ```

3. **Create your own branch**
      **PART 1**
   ```bash
   git checkout -b feature/vision
   ```
      **PART 2**
   ```bash
   git checkout -b feature/gesture
   ```
      **PART 3**
   ```bash
   git checkout -b feature/linux
   ```

5. **After making changes**
   Check what changed:
   ```bash
   git status
   ```
   Add files:
   ```bash
   git add
   ```
   Commit:
   ```bash
   git commit -m "Add hand landmark detection"
   ```
   Push:
   ```bash
   git push -u origin feature/vision
   ```
Use a meaningful commit message describing what you actually changed.

Examples:
Add MediaPipe hand tracking
Add pinch gesture detection
Add Linux command executor
Add safe shutdown handling

### Git Rules
| **DO** | **DON'T** | 
| :--- | :--- | :--- |
| ✓ Pull before starting work | ✗ Don't use git push --force | 
| ✓ Work mainly inside your assigned folder | ✗ Don't delete someone else's work | 
| ✓ Commit regularly | ✗ Don't commit .venv |
| ✓ Write clear commit messages | ✗ Don't commit __pycache__ |
| ✓ Push your branch | ✗ Don't commit .pyc files | 
| ✓ Tell the team before changing shared files | ✗ Don't commit .env files |
| - | ✗ Don't upload huge videos |
| - | ✗ Don't directly rewrite another person's module |

### Installations

1. **Set up a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
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

## 🛠️ Team Responsibilities

| Team Member | Main Responsibility | Main Output |
|---|---|---|
| Part 1 | Vision / Hand Tracking | 21 landmarks |
| Part 2 | Gesture Recognition | Standard command |
| Part 3 | OS / Linux Integration | Computer action |

* **File Naming Conventions:**
  1. **Vision Module (`test_vision.py`):** Asserts frame retrieval, checks array shapes, verifies 21 landmark output tuples.
  2. **Gesture Module (`test_gestures.py`):** Feeds predefined synthetic landmark matrices to verify that expected gesture strings and parameters are generated correctly.
  3. **System Module (`test_system.py`):** Issues isolated commands directly to verify that OS actions (e.g., cursor repositioning, click triggers) perform without exceptions.
  4. **End-to-End Integration:** Runs `main.py` to confirm the full pipeline:
      $$\text{Webcam Frame} \xrightarrow{\quad} \text{Landmarks} \xrightarrow{\quad} \text{Gesture} \xrightarrow{\quad} \text{Command} \xrightarrow{\quad} \text{OS Action}$$
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

## ✅ Definition of "Done"

## Part 1 is done when:

- [ ] Webcam works
- [ ] Hand is detected
- [ ] 21 landmarks are available
- [ ] Landmarks are displayed
- [ ] Coordinates can be passed to Part 2
- [ ] Code is committed to GitHub

## Part 2 is done when:

- [ ] Landmark input works
- [ ] Finger/hand features can be calculated
- [ ] At least 3 gestures are recognized
- [ ] Gestures produce standardized commands
- [ ] Code works with test/fake landmarks
- [ ] Code is committed to GitHub

## Part 3 is done when:

- [ ] Commands can be received
- [ ] Commands trigger OS actions
- [ ] Linux/Bash integration works
- [ ] Processes can be started/stopped
- [ ] Safe shutdown is implemented
- [ ] `run.sh` works
- [ ] Code is committed to GitHub

## Final project is done when:

- [ ] Webcam → landmarks works
- [ ] Landmarks → gesture works
- [ ] Gesture → command works
- [ ] Command → OS action works
- [ ] At least one gesture works end-to-end
- [ ] Multiple gestures work reliably
- [ ] Project can be demonstrated
- [ ] README/documentation is updated

---

# ⭐ 28. The One-Line Summary

> **We are building a webcam-based touchless HCI system that converts hand movements into computer commands using real-time computer vision, gesture recognition, and OS-level integration.**

---

# 🔑 Remember

Do not try to build everything at once.

Build:

```text
PART 1
Webcam → Landmarks
```

then:

```text
PART 2
Landmarks → Gesture → Command
```

then:

```text
PART 3
Command → OS Action
```

and finally:

```text
PART 1 + PART 2 + PART 3
          ↓
     FINAL SYSTEM
```

**Get one complete gesture working first. Then expand.**
