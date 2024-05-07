# autopadlet

[![forthebadge](http://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)
[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)

[![Author](https://img.shields.io/badge/author-InsanelyAvner-lightgrey.svg?style=flat&color=%23673ab7)](https://github.com/InsanelyAvner)
[![GitHub LICENSE](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/InsanelyAvner/autopadlet?style=flat&color=%23009688)](releases)

Simple tools for automated liking & commenting on [padlet](https://padlet.com/).

![](https://miro.medium.com/v2/resize:fit:1200/1*MIZ5pbtIwsdCVnhAYu13Hg.jpeg)

## Table of contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

## Requirements

* Python >= 3.6
* Pip
* Python `selenium` library
* Chrome (no restrictions)
    * To remove all Chrome policies/restrictions, run the `kool krome kode.reg` file.

## Installation
1. Clone the repository `git clone https://github.com/InsanelyAvner/autopadlet.git`
    * Alternatively, you may choose to download this project as a `.zip` and unzip it.
2. Install required libraries `pip install -r requirements.txt`

## Usage
1. Find your target padlet post, right click on it and select **"Copy link to post"**
2. Paste the full link into `link.txt`
3. Open `main.py` using a code editor
4. Change the variable `MODE` to:
    * `"comment"` to automate comments
    * `"like"` to automake likes


## Contributing

[(Back to top)](#table-of-contents)

Your contributions are always welcome! Feel free to fork this project and work on it.

## License

[(Back to top)](#table-of-contents)

Copyright © 2024 by InsanelyAvner.

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

Thanks [@p55d2k](https://github.com/p55d2k) for your support :)
