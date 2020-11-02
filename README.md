# MoodleV - A Discord bot integrated with the Moodle API

> A Discord multipurpose bot using Moodle API to get users data inside the Discord environment.

[![Latest Release][release]][release]

The project's main purpose is helping students to organize themselves through Moodle API built in a Discord Bot with more functionalities.

The bot's features include:

* Music
* Moodle
* Reminder (currently being reworked)
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

* 3.0.0
  * [Database Update](https://github.com/lsglucas/DiscordMackBot/releases/tag/3.0.0)
* 2.0.0
  * [Assignments Update](https://github.com/lsglucas/DiscordMackBot/releases/tag/2.0.0)
* 1.0.0
  * [Project and initial version release](https://github.com/lsglucas/DiscordMackBot/releases/tag/1.0.0)

## 👨🏻‍💻 Meta

Lucas Garcia – [@lsglucass](https://twitter.com/lsglucass) – lsglucas@pm.me

Daniel Kauffmann – [@danieldowombo](https://twitter.com/danieldowombo) – danielvenna2@hotmail.com

## 📑 License  

There is no license, hence you are not allowed to use, modify, merge, publish, distribute, sublicense, and/or sell copies of the software. The reproduction or distribution without written permission of the owners is prohibited. If you are interested in using this software, contact one of the creators.

## 🤝🏻 Contributing

You are more than welcome to contribute to the project, if you feel like helping us, you must contact any of the project creators ~~(We will try not to bite you)~~

[release]: https://img.shields.io/github/v/release/lsglucas/DiscordMackBot
[wiki]: https://github.com/lsglucas/DiscordMackBot/wiki
