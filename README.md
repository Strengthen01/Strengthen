# AI Traffic Control Demo 🚦

![Traffic Demo](docs/traffic_demo_screenshot.png)

## Project Overview
This project demonstrates an **AI-powered traffic control system** using **YOLOv8** for real-time vehicle detection and adaptive traffic light scheduling.  
It is designed to **improve traffic efficiency, reduce congestion, and support emergency vehicle prioritization** at urban intersections.  

The system supports:
- Multi-direction vehicle queue estimation (NS/EW directions)
- Emergency scenarios (ambulance/firetruck priority)
- Traffic data recording and historical analysis
- Real-time visualization dashboard

---

## Features
1. **Real-Time Vehicle Detection**
   - YOLOv8n model detects cars, motorcycles, buses, and emergency vehicles.
   - Lightweight and fast inference (FPS > 30 on GPU, 15+ on CPU).

2. **Adaptive Traffic Light Scheduling**
   - Dynamic green-light adjustment based on queue length.
   - Queue threshold-based timing: e.g., 30-90 seconds depending on traffic density.
   - Supports multi-directional intersections.

3. **Emergency Response**
   - Detects special vehicles and immediately switches green light in their direction.
   - Weather-adaptive recognition to reduce false detections.

4. **Historical Data Recorder**
   - Stores frame-wise vehicle counts, traffic light phases, and green-light duration.
   - Generates plots for traffic analysis and optimization.

5. **Cross-Platform Deployment**
   - Windows 10+/Ubuntu 20.04
   - Minimum: i3 CPU, 4GB RAM
   - Recommended: i5 CPU, 8GB RAM, dedicated GPU

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-traffic-control.git
cd ai-traffic-control
Technical Details

YOLOv8n chosen for lightweight, high FPS performance.

Vehicles mapped to classes: car=2, motorcycle=3, bus=5.

Queue estimation uses sliding window (window_sec=30, fps=5) with anomaly filtering.

Traffic light phases: NS/EW, green duration 30-90s based on queue length.

Emergency vehicle detection (ambulance=82) overrides normal scheduling.

Innovation

Multi-Direction Queue Estimation: Supports multiple directions independently using bounding box positions.

Emergency Response Mechanism: Special vehicle priority and weather-adaptive detection.

Historical Data Replay: Stores traffic data for optimization and visualization.


After unzipping:
Double-click install_and_run.bat and follow the prompts to install dependencies and run the program (for Windows).
Or perform manual operations:
Run pip install -r requirements.txt (to install dependencies)
Run python visual_panel/app.py
Run python demo_live.py --video sample_video.mp4

