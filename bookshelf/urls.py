from django.urls import path

from . import views

app_name = "bookshelf"

urlpatterns = [
    path("add_source/<int:space_id>", views.add_source, name="add_source"),
    path("upload_source_file/<int:source_id>", views.upload_source_file, name="upload_source_file"),
    path("delete_source/<int:source_id>", views.delete_source, name="delete_source"),
    path("alter_source_info/<int:source_id>", views.alter_source_info, name="alter_source"),
    path("alter_source_endnote/<int:endnote_id>", views.alter_endnote, name="alter_endnote"),
    path("source_space/<int:source_id>", views.source_space, name="source_space"),
    path("add_quote/<int:source_id>", views.add_quote, name="add_quote"),
    path("delete_quote/<int:quote_id>", views.delete_quote, name="delete_quote"),
    path("alter_quote/<int:quote_id>", views.alter_quote, name="alter_quote")
]
