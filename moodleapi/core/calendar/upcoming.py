from ..course import get_professor
from ..calendar.tools import clean, time, verify


def upcoming_information(*args) -> tuple:
    description = clean(args[2])
    deadline = clean(args[4])

    return (
        args[0],  # course, fullname
        args[1].split(" is ")[0]  # name
        if " is " in args[1]
        else args[1].split(" está ")[0],
        description if description != "" else "Descrição não disponível",  # description
        "Aula ao vivo - BigBlueButton"
        if args[3] == "bigbluebuttonbn"  # modulename
        else "Tarefa para entregar via Moodle",
        deadline[:-7],  # formattedtime
        deadline[-5:],
        args[5],  # url
        get_professor(**args[-1]),
    )


def upcoming_check_information(*args) -> tuple:
    status, date = None, None
    if args[3] == "assign":
        status, date = verify(
            args[-1]["r"],
            args[-1]["url"],
            args[-1]["token"],
            args[6],
            args[7],
        )

    description = clean(args[2])
    deadline = clean(args[4])
    t = time(date)

    return (
        args[0],  # course, fullname
        args[1].split(" is ")[0]  # name
        if " is " in args[1]
        else args[1].split(" está ")[0],
        description  # dar clean antes do description (description)
        if description != ""
        else "Descrição não disponível",
        "Aula ao vivo - BigBlueButton"
        if args[3] == "bigbluebuttonbn"  # modulename
        else "Tarefa para entregar via Moodle",
        deadline[:-7],  # pegar o dead line
        deadline[-5:],
        args[5],  # url
        get_professor(**args[-1]),
        f'Tarefa {"não " if status == 0 or not status else ""}entregue'
        if args[3] == "assign"
        else "",
        t if t != 0 and t else "",
    )
