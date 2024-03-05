# OVG
Open source vision goggles using ESP32-cam module.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Description

A brief description of what your project does and its purpose.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

1. Clone the repository:

```
git clone http://github.com/cxuri/ovg
 ```
 
2. Navigate to the project directory:

   cd to directory

3. Create a VirtualEnvironment

```
python -m venv Core
```

4. Activate virtual Environment

- On Windows:
  ```
  .\env\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source env/bin/activate
  ```

5. Install dependencies

```
pip install -r requirements.txt
 ```

6. After the install, copy the xml files to Core/lib/cv2/data folder respectively

7.Run the project

```
Python main.py
```

8. When asked stream url, give your url that you got from esp32 Cam module's web server


