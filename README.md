# MoodleV - A Discord bot integrated with the Moodle API

> A Discord multipurpose bot using Moodle API to get users data inside the Discord environment.

[![Latest Release][release]][release]

## ⚠️ This project is being reworked at: [github.com/moodleorganizerbot](https://github.com/moodleorganizerbot/discord-bot) 
> This is a read-only repository, we are currently reworking the project at the link above, this repository will not receive any updates.

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

* 4.5.0
  * [Moodle Rewrite Update](https://github.com/lsglucas/moodle-v/releases/tag/4.5.0)
* 3.0.0
  * [Database Update](https://github.com/lsglucas/moodle-v/releases/tag/3.0.0)
* 2.0.0
  * [Assignments Update](https://github.com/lsglucas/moodle-v/releases/tag/2.0.0)
* 1.0.0
  * [Project and initial version release](https://github.com/lsglucas/moodle-v/releases/tag/1.0.0)

## 👨🏻‍💻 Meta

Lucas Garcia – [@lsglucass](https://twitter.com/lsglucass) – lsglucas@pm.me

Daniel Kauffmann – [@danieldowombo](https://twitter.com/danieldowombo) – danielvenna2@hotmail.com

[release]: https://img.shields.io/github/v/release/lsglucas/moodle-v
[wiki]: https://github.com/lsglucas/moodle-v/wiki
