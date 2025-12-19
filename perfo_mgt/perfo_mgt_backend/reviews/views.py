from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import PerformanceReview

# simple home/introduction page
def home(request):
    return render(request, "reviews/home.html")

# manager dashboard – list and filters
def manager_dashboard(request):
    period = request.GET.get("period")
    rating_filter = request.GET.get("rating")

    reviews = PerformanceReview.objects.all().order_by("-review_date")

    if period in ["Monthly", "Quarterly", "Annual"]:
        reviews = reviews.filter(review_period=period)

    if rating_filter == "1-4":
        reviews = reviews.filter(rating__gte=1, rating__lte=4)
    elif rating_filter == "5-8":
        reviews = reviews.filter(rating__gte=5, rating__lte=8)
    elif rating_filter == "9-10":
        reviews = reviews.filter(rating__gte=9, rating__lte=10)

    context = {
        "reviews": reviews,
        "period": period or "",
        "rating_filter": rating_filter or "",
    }
    return render(request, "reviews/manager_dashboard.html", context)

# add review
def add_review(request):
    if request.method == "POST":
        PerformanceReview.objects.create(
            review_title=request.POST.get("review_title"),
            review_date=request.POST.get("review_date"),
            employee_id=request.POST.get("employee_id") or 0,
            reviewed_by=request.POST.get("reviewed_by") or 0,
            review_period=request.POST.get("review_period"),
            rating=request.POST.get("rating") or 0,
            comments=request.POST.get("comments", ""),
        )
        return redirect(reverse("manager_dashboard"))

    return render(request, "reviews/add_review.html")

# edit review
def edit_review(request, pk):
    review = get_object_or_404(PerformanceReview, pk=pk)

    if request.method == "POST":
        review.review_title = request.POST.get("review_title")
        review.review_date = request.POST.get("review_date")
        review.employee_id = request.POST.get("employee_id") or 0
        review.reviewed_by = request.POST.get("reviewed_by") or 0
        review.review_period = request.POST.get("review_period")
        review.rating = request.POST.get("rating") or 0
        review.comments = request.POST.get("comments", "")
        review.save()
        return redirect(reverse("manager_dashboard"))

    return render(request, "reviews/edit_review.html", {"review": review})

# delete review
def delete_review(request, pk):
    review = get_object_or_404(PerformanceReview, pk=pk)
    if request.method == "POST":
        review.delete()
        return redirect(reverse("manager_dashboard"))
    return render(request, "reviews/delete_confirm.html", {"review": review})

# employee dashboard – reviews for one employee
def employee_dashboard(request, employee_id):
    reviews = PerformanceReview.objects.filter(employee_id=employee_id).order_by("-review_date")
    return render(
        request,
        "reviews/employee_dashboard.html",
        {"reviews": reviews, "employee_id": employee_id},
    )
