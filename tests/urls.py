def reverse_url(loc: str, **kwargs) -> str:
    menu_pref = '/'
    submenu_pref = menu_pref + str(kwargs.get('menu_id', '')) + '/submenus/'
    dish_pref = submenu_pref + str(kwargs.get('submenu_id', '')) + '/dishes/'

    match loc:
        case 'menus':
            return menu_pref

        case 'menu':
            return menu_pref + str(kwargs.get('menu_id', ''))

        case 'submenus':
            return submenu_pref

        case 'submenu':
            return submenu_pref + str(kwargs.get('submenu_id', ''))

        case 'dishes':
            return dish_pref

        case 'dish':
            return dish_pref + str(kwargs.get('dish_id', ''))

    return menu_pref
