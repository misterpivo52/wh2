from django.shortcuts import render, redirect
from django.http import JsonResponse
import random
from datetime import datetime


def get_places_from_session(request):
    return request.session.get('places', [])


def save_places_to_session(request, places):
    request.session['places'] = places


def index(request):
    places = get_places_from_session(request)
    return render(request, 'places/index.html', {'places_count': len(places)})


def places_list(request):
    places = get_places_from_session(request)
    return render(request, 'places/places_list.html', {'places': places})


def place_detail(request, place_id):
    places = get_places_from_session(request)
    place = None
    for p in places:
        if p['id'] == place_id:
            place = p
            break

    if not place:
        return redirect('places:places_list')

    return render(request, 'places/place_detail.html', {'place': place})


def add_place(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        place_type = request.POST.get('place_type', '').strip()
        location = request.POST.get('location', '').strip()
        rating = request.POST.get('rating', '')

        errors = {}

        if not name:
            errors['name'] = 'Назва не може бути порожньою'

        if not description:
            errors['description'] = 'Опис не може бути порожнім'

        if not place_type:
            errors['place_type'] = 'Тип місця не може бути порожнім'

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                errors['rating'] = 'Рейтинг має бути від 1 до 5'
        except (ValueError, TypeError):
            errors['rating'] = 'Рейтинг має бути цілим числом від 1 до 5'

        if not errors:
            places = get_places_from_session(request)
            new_id = max([p['id'] for p in places], default=0) + 1

            new_place = {
                'id': new_id,
                'name': name,
                'description': description,
                'place_type': place_type,
                'location': location,
                'rating': rating,
                'date_created': datetime.now().strftime('%d.%m.%Y'),
            }

            places.append(new_place)
            save_places_to_session(request, places)

            return redirect('places:places_list')
        return render(request, 'places/add_place.html', {
            'errors': errors,
            'form_data': request.POST
        })

    return render(request, 'places/add_place.html')


def random_place(request):
    places = get_places_from_session(request)
    if not places:
        return JsonResponse({'error': 'Немає збережених місць'})
    used_places = request.session.get('used_places', [])
    available_places = [p for p in places if p['id'] not in used_places]

    if not available_places:

        request.session['used_places'] = []
        available_places = places.copy()
    weighted_places = []
    for place in available_places:
        count = place['rating'] * 10
        weighted_places.extend([place] * count)

    selected_place = random.choice(weighted_places)
    used_places.append(selected_place['id'])
    request.session['used_places'] = used_places

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'place': selected_place
        })
    else:
        return render(request, 'places/index.html', {
            'selected_place': selected_place,
            'places_count': len(places)
        })
