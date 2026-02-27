from aiogram.fsm.state import State, StatesGroup


class CatalogState(StatesGroup):
    brand = State()
    product_id = State()


class CartState(StatesGroup):
    items = State()
    current_index = State()
    user_id = State()
