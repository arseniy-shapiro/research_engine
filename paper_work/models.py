from django.db import models

from file_handling.models import PaperVersion
from research_engine.settings import MEDIA_ROOT
from user_management.models import User
from work_space.models import WorkSpace


class Paper(models.Model):

    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="papers")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, unique=True)
    is_archived = models.BooleanField(default=False)


    def __str__(self):
        """Display paper title"""
        return self.title


    def get_path(self):
        """Returns a path to the paper directory"""
        return f"{MEDIA_ROOT}/user_{self.user.pk}/paper_{self.pk}"
    
    
    def get_number_of_files(self):
        """Returns a number of files (PaperVersion objects) related to this papers"""
        return len(PaperVersion.objects.filter(paper=self))
    
    

# Maybe add to Paper class needed number of words etc.

# How to connect work space - paper - and files
