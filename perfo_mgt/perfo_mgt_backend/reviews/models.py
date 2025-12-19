from django.db import models

# Create your models here.from django.db import models

class PerformanceReview(models.Model):
    review_title = models.CharField(max_length=100)
    review_date = models.DateField()
    employee_id = models.IntegerField()
    reviewed_by = models.IntegerField()
    review_period = models.CharField(max_length=100)  # Monthly/Quarterly/Annual
    rating = models.IntegerField()
    comments = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review_title
