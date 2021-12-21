import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    release_year = datetime.date.today()
    return {'year': release_year.year}
