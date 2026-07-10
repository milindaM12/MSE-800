from django.shortcuts import render


def home_page(request):
    name = ""

    if request.method == "POST":
        name = request.POST.get("name", "").strip()

    return render(
        request,
        "home/index.html",
        {
            "name": name,
        },
    )