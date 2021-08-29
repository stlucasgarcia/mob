# MoodleV - A Discord bot integrated with the Moodle API

> A Discord multipurpose bot using Moodle API to get users data inside the Discord environment.

[![Latest Release][release]][release] [![license][license]][license]


## ⚠️ This project is being reworked 

The project's main purpose is helping students to organize themselves through Moodle API built in a Discord Bot with more functionalities. IF you wish to use this bot with your Moodle, contact us and we will help you to set it up.

The bot's features include:

* Music
* Moodle
* Reminder
* Profile (with level system)
* Reaction role
* General admin commands
* Fun  

## 📱 Usage Example

On Discord, you can use the following commands to get Moodle assignments on a 14 days range:

```discord
<prefix> get assignments
```

`get` support _events_, _assignments_ and _classes_. However, you can obtain personal information about assignments by using `check`

```discord
<prefix> check
```

_For more examples and usage, please refer to the [Wiki][wiki]._

## 💻 Development Setup

For the firsts dependencies, you need to install all requirements in ```requirements.txt``` and you must have PostgreSQL installed in your machine. For now, you need to create the ```DiscordDB``` in your default public Schema, in the future that will be changed.

```sh
pip install -r requirements.txt  
```
  
## ✅ Release History

* 0.1.0
  * _coming soon_

## 👨🏻‍💻 Meta

Lucas Garcia – [@lsglucass](https://twitter.com/lsglucass) – lsglucas@pm.me

Daniel Kauffmann – [@danieldowombo](https://twitter.com/danieldowombo) – danielvenna2@hotmail.com

## 🤝🏻 Contributing

You are more than welcome to contribute to the project!

## 📑 License  

MIT License

Copyright (c) 2021 Moodle Organizer Bot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[release]: https://img.shields.io/github/v/release/lsglucas/mob
[wiki]: lsglucas.github.io/mob/
[license]: https://img.shields.io/github/license/lsglucas/mob

