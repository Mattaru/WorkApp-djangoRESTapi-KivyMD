from kivymd.uix.list import OneLineIconListItem, IconLeftWidget


class OrderLIstItem(OneLineIconListItem):
    """Дополнительно содержит в себе icon и принимает аргументы order_id и
    icon - название/путь к файлу иконки."""
    def __init__(self, order_id, icon, **kwargs):
        super().__init__(**kwargs)
        self.order_id = order_id
        self.icon = icon

        icon = IconLeftWidget(icon=self.icon)
        self.add_widget(icon)
