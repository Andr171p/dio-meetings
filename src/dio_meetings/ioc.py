from dishka import Provider, provide, Scope, from_context, make_container


class AppProvider(Provider):
    ...


container = make_container(AppProvider())
