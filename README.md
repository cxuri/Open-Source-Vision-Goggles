# Open Source Vision Goggles v0.01

Open Source Vision Goggles (OVG) is a project aimed at leveraging the capabilities of the ESP32-CAM module to create affordable and accessible vision-enhancing goggles. These goggles are designed to provide users with a hands-free way to stream video footage and perform computer vision tasks in real-time.

## Description

The OVG project utilizes the ESP32-CAM module to capture and stream live video feeds, which can then be processed for various computer vision applications. These applications could include object detection, facial recognition, motion tracking, and more. By harnessing the power of open-source software and hardware, OVG aims to democratize access to advanced vision technologies.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

1. **Clone the repository:**
   ```bash
   git clone http://github.com/cxuri/ovg
   ```

2. **Navigate to the project directory:**
   ```bash
   cd ovg
   ```

3. **Create a Virtual Environment:**
   ```bash
   python -m venv env
   ```

4. **Activate the virtual environment:**
   - On Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source env/bin/activate
     ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Copy XML files:**
   After installation, copy the XML files to `Core/lib/cv2/data` folder respectively.

7. **Run the project:**
   ```bash
   python main.py
   ```

8. **Provide stream URL:**
   When prompted, enter the URL obtained from the ESP32-CAM module's web server.

## Usage

Once the project is running, the OVG goggles will start streaming video from the ESP32-CAM module. Users can then perform various computer vision tasks by interfacing with the provided functionalities. Additionally, developers can extend the capabilities of OVG by contributing to the open-source project.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT), allowing for free use, modification, and distribution of the software.
