def validate_ingredients(ingredients: str) -> str:
    # The import lives INSIDE the function: it runs at call time, when both
    # modules are fully loaded, so no cycle exists while importing.
    from .light_spellbook import light_spell_allowed_ingredients

    lowered: str = ingredients.lower()
    for allowed in light_spell_allowed_ingredients():
        if allowed in lowered:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
