# AmbienAI

## Demo
![AmbienAI Demo](./assets/demo.gif)

## Overview
AmbienAI is a computer vision system designed to measure advertising engagement by analyzing viewer attention and gaze patterns. The system tracks how long and how intensely viewers look at digital displays, providing valuable metrics for advertising effectiveness.

## Features
- Real-time gaze tracking and attention detection
- Engagement duration measurements
- Multi-face detection and tracking
- Attention metrics dashboard
- Privacy-compliant data collection
- Export capabilities for analytics

## Requirements
- Python 3.8+
- OpenCV
- MediaPipe
- NumPy
- Pandas

## Installation
```bash
git clone https://github.com/yourusername/AmbienAI.git
cd AmbienAI
pip install -r requirements.txt
```

## Usage
```python
from ambienai import AttentionTracker

# Initialize the tracker
tracker = AttentionTracker()

# Start tracking
tracker.start_tracking()
```

## Project Structure
```
AmbienAI/
│
├── src/
│   ├── core/
│   │   ├── tracker.py
│   │   ├── detector.py
│   │   └── analyzer.py
│   │
│   ├── utils/
│   │   ├── visualization.py
│   │   └── data_processing.py
│   │
│   └── gui/
│       └── dashboard.py
│
├── tests/
│   └── test_tracker.py
│
├── docs/
│   └── API.md
│
├── requirements.txt
└── README.md
```

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Privacy Notice
AmbienAI is designed with privacy in mind. All processing is done locally, and no personally identifiable information is stored. The system only tracks anonymous engagement metrics.

## Acknowledgments
- MediaPipe team for face detection models
- OpenCV community
- Contributors and testers

## Contact
- Project Lead: Patrick Menendez Rosado, Nicholas Chen
- Email: patrickmenendez29@gmail.com
- Email: nicholaschen.10@hotmail.com
