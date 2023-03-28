import django.db.models

import catalog.models
import rating.models
import users.models


class RatingManager(django.db.models.Manager):
    def by_users(self):
        statistics_by_users = {}
        active_users_with_ratings = (
            users.models.ProxyUser.objects.active().filter(
                rating__isnull=False
            )
        )
        for user in active_users_with_ratings:
            max_rated_item_data = (
                user.rating.all()
                .order_by(
                    f'-{rating.models.Rating.rating.field.name}',
                    f'-{rating.models.Rating.created_at.field.name}',
                )
                .values(
                    rating.models.Rating.rating.field.name,
                    rating.models.Rating.item.field.name,
                )
                .first()
            )
            min_rated_item_data = (
                user.rating.all()
                .order_by(
                    f'{rating.models.Rating.rating.field.name}',
                    f'-{rating.models.Rating.created_at.field.name}',
                )
                .values(
                    rating.models.Rating.rating.field.name,
                    rating.models.Rating.item.field.name,
                )
                .first()
            )
            statistics_by_users[user.username] = {
                'max': max_rated_item_data,
                'min': min_rated_item_data,
                'average': user.rating.all().aggregate(
                    django.db.models.Avg(
                        rating.models.Rating.rating.field.name
                    )
                )['rating__avg'],
                'amount': len(user.rating.all()),
            }
        return statistics_by_users

    def by_items(self):
        statistics_by_items = {}
        active_items_with_ratings = (
            catalog.models.Item.objects.published().filter(
                rating__isnull=False
            )
        )
        for item in active_items_with_ratings:
            last_max_rating = (
                item.rating.all()
                .order_by(
                    f'-{rating.models.Rating.rating.field.name}',
                    f'-{rating.models.Rating.created_at.field.name}',
                )
                .values(
                    rating.models.Rating.rating.field.name,
                    rating.models.Rating.user.field.name,
                )
                .first()
            )
            last_min_rating = (
                item.rating.all()
                .order_by(
                    f'{rating.models.Rating.rating.field.name}',
                    f'-{rating.models.Rating.created_at.field.name}',
                )
                .values(
                    rating.models.Rating.rating.field.name,
                    rating.models.Rating.user.field.name,
                )
                .first()
            )
            statistics_by_items[item.name] = {
                'max': last_max_rating,
                'min': last_min_rating,
                'average': item.rating.all().aggregate(
                    django.db.models.Avg(
                        rating.models.Rating.rating.field.name
                    )
                )['rating__avg'],
                'amount': len(item.rating.all()),
            }
        return statistics_by_items
