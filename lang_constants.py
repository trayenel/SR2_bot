from helper_functions import setLanguage

setLanguage("ru")

START_MESSAGE = _(
    f"""
Привет! 👋

Я бот, который поможет вам сгенерировать рабочую ссылку на новость или статью с сайта заблокированного СМИ.

Отправьте мне ссылку, которой хотите поделиться.
"""
)  # noqa: E501

HELP_MESSAGE = _(
    f"""
Данный бот создан для того, чтобы вы могли безпрепятственно делиться ссылками с заблокированных в России сайтов СМИ.

Чтобы получить рабочую ссылку на статью или новость, отправьте боту ссылку на статью с одного из сайтов заблокированного СМИ.

"""
)