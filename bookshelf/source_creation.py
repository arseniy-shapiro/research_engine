from typing import Callable
from django import forms
from .dates import validate_date
from .forms import ArticleForm, BookForm, ChapterForm, WebpageForm
from .models import Article, Book, Chapter, Endnote, Source, Webpage
from .quoting_apa import quote_source_apa
from .quoting_mla import quote_source_mla
from user_management.models import User
from utils.verification import check_link
from work_space.models import WorkSpace


def create_source(user: User, space: WorkSpace, form: forms.Form, author: str, chapter_author=None) -> Callable | None:
    """Get future source type and call right func"""

    # Iterate through all fields and clean its data
    cleaned_data: dict = {}
    for field in form.fields:
        info = form.cleaned_data[field]
        if type(info) == str:
            info = clean_text_data(info)
        cleaned_data[field] = info

    match form:
        case BookForm():
            return create_book_obj(user, space, cleaned_data, author)
        case ArticleForm():
            return create_article_obj(user, space, cleaned_data, author)
        case ChapterForm():
            return create_chapter_obj(user, space, cleaned_data, author, chapter_author)
        case WebpageForm():
            return create_webpage_obj(user, space, cleaned_data, author)
        case _:
            return None


#def upload_file(s)



def copy_source(source: Source, new_space: WorkSpace, new_owner: User) -> Source:
    """Copy source and change its work space"""

    # Go down to source child obj
    source_type = source.cast()
    match source_type:
        case Book():
            source = source.book
        case Article():
            source = source.article
        case Chapter():
            source = source.chapter
        case Webpage():
            source = source.webpage
        case _:
            return None

    # Copy the given source and alter its key fields
    source.pk, source.id = None, None
    source.work_space, source.user = new_space, new_owner
    source._state.adding = True
    source.save()

    # Copy file if necessary
    if source.file:
        source.file = copy_source_file(source, new_space, new_owner.pk)
    source.save(update_fields=("file",))

    # Create Endnote obj based on new source
    return save_endnotes(source)


def copy_source_file(source: Source, new_space: WorkSpace, new_owner_id: int) -> str:
    """Returns a new path to the copied file"""
    space_path = new_space.get_base_dir()
    source_id, user_id = source.pk, new_owner_id
    filename = source.file_name()
    return f"{space_path}/books/user_{user_id}/source_{source_id}/{filename}"


def save_endnotes(source: Source):
    """Creates and saves new Endnote obj for given source"""
    endnotes = Endnote(source=source, apa=quote_source_apa(source), mla=quote_source_mla(source))
    return endnotes.save()


def create_book_obj(user: User, space: WorkSpace, cleaned_data: dict, author: str):
    """Validate Bookform and create Book obj"""

    # Create and save new Book obj
    new_book = Book(work_space=space, user=user, author=author, title=cleaned_data["title"], 
                    year=cleaned_data["year"], publishing_house=cleaned_data["publishing_house"])
    new_book.save()
    # Create new Endnote obj with Foreign key to this Book obj
    return save_endnotes(new_book)


def create_article_obj(user: User, space: WorkSpace, cleaned_data: dict, author: str):
    """Validate Articleform and create Article obj"""

    # Create and save new Article obj
    new_article = Article(work_space=space, user=user, author=author, title=cleaned_data["article_title"], 
                          year=cleaned_data["year"], journal_title=cleaned_data["journal_title"], 
                          volume=cleaned_data["volume"], issue=cleaned_data["issue"], 
                          pages=cleaned_data["pages"], link_to_journal=cleaned_data["link_to_journal"])
    new_article.save()
    # Create new Endnote obj with Foreign key to this Article obj
    return save_endnotes(new_article)


def create_chapter_obj(user: User, space: WorkSpace, cleaned_data: dict, book_author: str, chapter_author: str):
    """Validate Chapterform and create Chapter obj"""
    
    # Create and save new Chapter obj
    new_chapter = Chapter(work_space=space, user=user, author=chapter_author, book_author=book_author, 
                          title=cleaned_data["chapter_title"], book_title=cleaned_data["book_title"],
                          publishing_house = cleaned_data["publishing_house"], year=cleaned_data["year"],
                          edition = cleaned_data["edition"], pages=cleaned_data["pages"])
    new_chapter.save()
    # Create new Endnote obj with Foreign key to this Chapter obj
    return save_endnotes(new_chapter)


def create_webpage_obj(user: User, space: WorkSpace, cleaned_data: dict, author: str | None):
    """Validate Webpageform and create Webpage obj"""

    if not author:
        author = "No author"

    # Checks date and if a given page url is indeed a link and gets you to a real webpage
    page_url, date = cleaned_data["page_url"], cleaned_data["date"]
    if not check_link(page_url) or not validate_date(date):
        # TODO
        pass

    # Create and save new Webpage obj
    new_webpage = Webpage(work_space=space, user=user, author=author, 
                          page_url=page_url, date=date, title=cleaned_data["page_title"],
                          website_title=cleaned_data["website_title"])
    new_webpage.save()
    # Create new Endnote obj with Foreign key to this Webpage obj
    return save_endnotes(new_webpage)


def clean_text_data(data: str) -> str:
    """Cleans given str-field"""
    return data.strip(""".,'" """)


def clean_author_data(data, chapter_author=False) -> str | bool:
    """Get, clean and validate all author-related form-field"""
    try:
        # Get number of authors
        if chapter_author:
            number_of_authors = int(data.get("number_of_chapter_authors"))
        else:
            number_of_authors = int(data.get("number_of_authors"))
    except ValueError:
        return False
    
    authors: list = []
    for i in range(number_of_authors):
        if chapter_author:
            last_name = data.get(f"chapter_last_name_{i}")
            first_name = data.get(f"chapter_first_name_{i}")
            second_name = data.get(f"chapter_second_name_{i}")
        else:
            last_name = data.get(f"last_name_{i}")
            first_name = data.get(f"first_name_{i}")
            second_name = data.get(f"second_name_{i}")

        # Return if last_name field was somehow left blank
        if not last_name:
            return False

        last_name = clean_text_data(last_name)
        if not first_name:
            # If there is only last name
            author = last_name
        else:
            first_name = clean_text_data(first_name)
            if second_name:
                second_name = clean_text_data(second_name)
                # Case with multiple names
                author = f"{last_name} {first_name} {second_name}"
            else:
                # Case without second names
                author = f"{last_name} {first_name}"
            
        authors.append(author)
    # Make str from authors list, separating authors by comma
    return ", ".join(authors)
