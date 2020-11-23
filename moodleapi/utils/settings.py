# TODO: Rewrite settings file

functions = {
    "core_calendar_get_calendar_monthly_view": "monthly",
    "core_calendar_get_calendar_upcoming_view": "upcoming",
    "core_calendar_get_calendar_day_view": "day",
    "core_course_get_contents": "contents",
    "core_enrol_get_users_courses": "courses",
}

db_query = {
    "moodle_events": "moodle_events_query",
    "moodle_assign": "moodle_assign_query",
    "moodle_profile": "moodle_profile_query",
    "moodle_professors": "moodle_professors_query",
    "bot_reminder": "bot_reminder_query",
}

allowed_modules = ("assign", "bigbluebuttonbn")

courses_not_allowed = (
    1,
    87177,
    5368,
    87178,
    87160,
    87161,
)  # TODO: Transform to config by user in DB

SERVICE = "login/"
CONNECTION = "token.php?"
PLATFORM = "service=moodle_mobile_app"

# Month names translated to PT-BR
month = {
    "Jan": "Janeiro",
    "Feb": "Fevereiro",
    "Mar": "Março",
    "Apr": "Abril",
    "May": "Maio",
    "Jun": "Junho",
    "Jul": "Julho",
    "Aug": "Agosto",
    "Sep": "Setembro",
    "Oct": "Outubro",
    "Nov": "Novembro",
    "Dec": "Dezembro",
}

# Week day names translated to PT-BR
week = {
    "Sun": "Domingo",
    "Mon": "Segunda-feira",
    "Tue": "Terça-feira",
    "Wed": "Quarta-feira",
    "Thu": "Quinta-feira",
    "Fri": "Sexta-feira",
    "Sat": "Sábado",
}

# TODO: VER SE TALVEZ SEJA BOM COLOCAR NO INIT DOS PACKAGES
