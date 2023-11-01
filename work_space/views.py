from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

import shutil
import os

from .forms import NewWorkSpaceForm, RenameWorkSpaceForm, ReceiveInvitationForm
from .invitation_generator import generate_invitation
from .models import WorkSpace
from paper_work.forms import NewPaperForm
from research_engine.settings import MEDIA_ROOT
from utils.verification import check_work_space, check_invitation, space_ownership_required


@login_required(redirect_field_name=None)
def index(request):

    return render(request, "work_space/index.html", {"form": NewWorkSpaceForm, "spaces": WorkSpace.objects.all()})


@login_required(redirect_field_name=None)
def create_work_space(request):
    # TODO

    form = NewWorkSpaceForm(request.POST)

    if form.is_valid():

        # Save new work space to the db and create its directory
        title = form.cleaned_data["title"]
        new_space = WorkSpace(owner=request.user, title=title)
        new_space.save()
        new_space.create_directory()

        # Redirect user to the new work space
        new_space_id = WorkSpace.objects.get(owner=request.user, title=title).pk
        link_to_work_space = reverse("work_space:space", args=(new_space_id,))
        return redirect(link_to_work_space)

    # TODO
    print(form.errors)
    return redirect(reverse("user_management:error_page"))


@space_ownership_required
@login_required(redirect_field_name=None)
def delete_work_space(request, space_id):

    # Check if user has right to delete this paper
    space = check_work_space(space_id, request.user)

    # Delete work pace directory with all files inside
    shutil.rmtree(space.get_path())

    # Delete work s[ace] from the db
    space.delete()

    return JsonResponse({"message": "ok"})


@space_ownership_required
@login_required(redirect_field_name=None)
def archive_work_space(request, space_id):
    """Mark given work space as archived"""

    space = check_work_space(space_id, request.user)

    space.is_archived = True
    space.save(update_fields=("is_archived",))

    return JsonResponse({"message": "ok"})


@login_required(redirect_field_name=None)
def download_work_space(request, space_id):
    """Download archived (zip) file of the whole work space directory"""

    # Check if user has right to download the work space
    space = check_work_space(space_id, request.user)

    # Create zip file of the directory
    zip_file = shutil.make_archive(space.title, "zip", root_dir=MEDIA_ROOT, base_dir=space.get_base_dir())

    # Open and send it
    return FileResponse(open(zip_file, "rb"))


@login_required(redirect_field_name=None)
def work_space(request, space_id):
    # TODO

    space = check_work_space(space_id, request.user)

    return render(request, "work_space/work_space.html", {"space": space, "papers": space.papers.all(), "form": NewPaperForm()})


@space_ownership_required
@login_required(redirect_field_name=None)
def rename_work_space(request, space_id):
    # TODO

    form = RenameWorkSpaceForm(request.POST)

    if form.is_valid():

        space = check_work_space(space_id, request.user)

        new_title = form.cleaned_data["new_title"]
        space.title = new_title
        space.save(update_fields=("title",))

        return JsonResponse({"message": "ok"})

    else:
        print(form.errors)
        # TODO
        pass

    return JsonResponse({"message": "error"})


@space_ownership_required
@login_required(redirect_field_name=None)
def invite_to_work_space(request, space_id):
    """Create an invitation to work space for another user"""
    # TODO

    # Check if user has right to invite to the work space
    space = check_work_space(space_id, request.user)

    invitation_code = generate_invitation(space)

    return JsonResponse({"invitation code": invitation_code})


@login_required(redirect_field_name=None)
def receive_invitation(request):
    '''Adds user as guest to the new work space if they were invited'''

    form = ReceiveInvitationForm(request.POST)

    if form.is_valid():

        # Check invitation code
        invitation_code = form.cleaned_data["code"]
        invitation = check_invitation(invitation_code)

        # Add user as guest to the new work space
        new_work_space = invitation.work_space
        new_work_space.guests.add(request.user)

        return JsonResponse({"message": "ok"})

    else:
        print(form.errors)
        # TODO
        pass

    return JsonResponse({"message": "error"})


@login_required(redirect_field_name=None)
def leave_work_space(request, space_id):
    """Remove guest from a work space"""

    # Check if user was indeed a guest in a given work space
    space = check_work_space(space_id, request.user)
    if request.user not in space.guests.all():
        return JsonResponse({"message": "error"})

    # Remove user
    space.guests.remove(request.user)
    return JsonResponse({"message": "ok"})


@login_required(redirect_field_name=None)
def test_restructure_dir(request, space_id):

    space = check_work_space(space_id, request.user)

    papers = space.papers.all()
    books = space.books.all()

    if not papers and not books:
        return JsonResponse({"message": "Empty Work Space"})

    space.create_friendly_dir()
    root_path = space.get_friendly_path()


    if papers:

        papers_root = f"{root_path}/papers"

        os.mkdir(papers_root)

        authors = [paper.user for paper in papers]

        for author in authors:

            author_name = f"{author.last_name} {author.first_name}"

            os.makedirs(os.path.join(papers_root, author_name), exist_ok=True)

            author_papers = papers.filter(user=author)

            for author_paper in author_papers:

                path_to_paper = f"{papers_root}/{author_name}/{author_paper}"

                os.makedirs(path_to_paper, exist_ok=True)

                versions = author_paper.versions.all()

                for version in versions:

                    path_to_paper_version = f"{path_to_paper}/{version.get_saving_time()}"
                    os.makedirs(path_to_paper_version, exist_ok=True)
                    file_name = version.file_name()


                    original_file = version.get_full_path()
                    destination = os.path.join(path_to_paper_version, file_name)

                    shutil.copyfile(original_file, destination)
    
    if books:

        # TODO
        # Create a txt/exel etc. file for all books (not book files)?
        pass

    return JsonResponse({"message": "ok"})





# Is there a way to send request without forms in create and rename workspace functions?

# Comments? Each one has only one version of paper?

# Resctructure work space diretory efore sending its version to the user?
# Mkdir - restructure and then (probably using some decorator) - delete it after it's been sent
