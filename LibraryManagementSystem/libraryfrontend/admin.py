from django.contrib import admin

from .models import (
    AuthorModel,
    BookModel,
    BookRatingModel,
    CategoryModel,
    PublisherModel,
)


@admin.register(AuthorModel, BookModel, CategoryModel, PublisherModel, BookRatingModel)
class BaseAdminModel(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = self.model.all_objects
        # The below is copied from the base implementation in BaseModelAdmin to prevent other changes in behavior
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        # it's safe to hard delete test data
        if obj.is_test_data:
            obj.hard_delete()
        else:
            obj.delete()
