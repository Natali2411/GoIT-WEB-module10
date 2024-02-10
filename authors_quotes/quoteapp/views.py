from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from twisted.internet import reactor

from .forms import TagForm, AuthorForm, QuoteForm
from .models import Quote, Tag, Author
from .scraping.save_data_db import write_to_db, FileInteraction
from .scraping.scrape import crawl


def quotes(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 3)  # Show 5 contacts per page
    page = request.GET.get('page')
    quotes_on_page = paginator.get_page(page)
    return render(request, "quoteapp/index.html", {"quotes": quotes_on_page})


def tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quoteapp:quotes")
        else:
            return render(request, "quoteapp/tag.html", {"form": form})

    return render(request, "quoteapp/tag.html", {"form": TagForm()})


def tag_search(request, tag_id):
    quotes = Quote.objects.filter(tags=tag_id).all()
    paginator = Paginator(quotes, 3)  # Show 5 contacts per page
    page = request.GET.get('page')
    quotes_on_page = paginator.get_page(page)
    return render(request, 'quoteapp/searched_quotes.html', {"quotes": quotes_on_page})


@login_required
def author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quoteapp:quotes")
        else:
            return render(request, "quoteapp/author.html", {"form": form})

    return render(request, "quoteapp/author.html", {"form": AuthorForm()})


@login_required
def quote(request):
    tags = Tag.objects.filter().all()
    authors = Author.objects.filter().all()

    if request.method == "POST":
        form = QuoteForm(request.POST)

        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.author = Author.objects.filter(
                fullname=request.POST.get("authors")
            ).first()
            new_quote.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to="quoteapp:quotes")
        else:
            return render(
                request,
                "quoteapp/quote.html",
                {"form": form, "tags": tags, "authors": authors},
            )

    return render(
        request,
        "quoteapp/quote.html",
        {"form": QuoteForm(), "tags": tags, "authors": authors},
    )


def detail_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quoteapp/detail_author.html', {"author": author})

@login_required
def scrape_info(request):
    try:
        crawl()
        reactor.run()
        write_to_db(authors_file_path="data/authors.json",
                    quotes_file_path="data/quotes.json")
    except Exception as err:
        messages.warning(request, f"Scraping was interrupted due to errors: {str(err)}")
    else:
        messages.success(request, "Scraping completed successfully")
    finally:
        FileInteraction.delete_folder(folder_path="data")
    return redirect(to="quoteapp:quotes")
