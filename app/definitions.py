from app.models import SupportedLanguages, Categories, Genres, Tags

integerFields = ['appid', 'required_age', 'price', 'dlc_count', 'positive', 'negative', 'score_rank']
booleanFields = ['windows', 'mac', 'linux']
m2mFields = ['supported_languages', 'categories', 'genres', 'tags']
stringFields = ['name', 'about_the_game', 'developers', 'publishers']
dateFields = ['release_date']
mapColumnNameToModel = {
    'supported_languages': SupportedLanguages,
    'categories': Categories,
    'genres': Genres,
    'tags': Tags
}
mapColumnNameToSingular = {
    'supported_languages': 'supported_language',
    'categories': 'category',
    'genres': 'genre',
    'tags': 'tag'
}
