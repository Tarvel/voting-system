from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
import csv
import io

from .models import Candidate, Position, User, Vote
from .forms import CsvUploadForm, CandidateCsvUploadForm


admin.site.site_header = "Voting Site Admin"
admin.site.site_title = "Voting Site Admin"
admin.site.index_title = "Welcome to the Admin Panel"



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Voting Status', {'fields': ('has_voted',)}),
    )
    list_display = UserAdmin.list_display + ('has_voted',)

    def get_urls(self):
        """Adds the custom URL for our upload page."""
        urls = super().get_urls()
        custom_urls = [
            path(
                "upload-csv/",
                self.admin_site.admin_view(self.upload_csv_view),
                name="upload_csv",
            ),
        ]
        return custom_urls + urls

    def upload_csv_view(self, request):
        """This view handles the CSV upload page and logic."""
        if request.method == "POST":
            form = CsvUploadForm(request.POST, request.FILES)
            if form.is_valid():

                csv_file = request.FILES["csv_file"]
                decoded_file = csv_file.read().decode("utf-8")
                io_string = io.StringIO(decoded_file)

                reader = csv.DictReader(io_string)
                users_created = 0
                users_skipped = 0

                for row in reader:
                    username = row.get("username", "").strip()
                    first_name = row.get("first_name", "").strip()
                    last_name = row.get("last_name", "").strip()
                    email = row.get("email", "").strip()

                    # Validate required fields
                    if not username or not last_name:
                        messages.error(
                            request,
                            f"Skipping row because of missing username or last name: {row}",
                        )
                        continue

                    # Check if user already exists by username or email
                    if User.objects.filter(username=username).exists():
                        users_skipped += 1
                        continue
                    
                    if email and User.objects.filter(email=email).exists():
                        users_skipped += 1
                        continue

                    try:
                        User.objects.create_user(
                            username=username,
                            email=email if email else "",
                            first_name=first_name,
                            last_name=last_name,
                            password=f"vote-{last_name.upper()}",
                        )
                        users_created += 1
                    except Exception as e:
                        messages.error(request, f"Error creating user {username}: {e}")

                self.message_user(
                    request, f"Successfully created {users_created} new users."
                )
                if users_skipped > 0:
                    self.message_user(
                        request,
                        f"Skipped {users_skipped} users because they already exist.",
                        level=messages.WARNING,
                    )

                return redirect("..")

        form = CsvUploadForm()
        context = {"form": form}
        return render(request, "admin/csv_upload.html", context)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'party')
    list_filter = ('position', 'party')
    search_fields = ('name', 'party', 'bio')

    def get_urls(self):
        """Adds the custom URL for candidate CSV upload page."""
        urls = super().get_urls()
        custom_urls = [
            path(
                "upload-csv/",
                self.admin_site.admin_view(self.upload_csv_view),
                name="upload_candidate_csv",
            ),
        ]
        return custom_urls + urls

    def upload_csv_view(self, request):
        """This view handles the Candidate CSV upload page and logic."""
        if request.method == "POST":
            form = CandidateCsvUploadForm(request.POST, request.FILES)
            if form.is_valid():

                csv_file = request.FILES["csv_file"]
                decoded_file = csv_file.read().decode("utf-8")
                io_string = io.StringIO(decoded_file)

                reader = csv.DictReader(io_string)
                candidates_created = 0
                candidates_skipped = 0

                for row in reader:
                    name = row.get("name", "").strip()
                    party = row.get("party", "").strip()
                    bio = row.get("bio", "").strip()
                    position_name = row.get("position", "").strip()

                    # Validate required fields
                    if not name or not position_name:
                        messages.error(
                            request,
                            f"Skipping row because of missing name or position: {row}",
                        )
                        continue

                    # Get or validate the position
                    try:
                        position = Position.objects.get(name=position_name)
                    except Position.DoesNotExist:
                        messages.error(
                            request,
                            f"Position '{position_name}' does not exist. Please create it first.",
                        )
                        continue

                    # Check if candidate already exists
                    if Candidate.objects.filter(name=name, position=position).exists():
                        candidates_skipped += 1
                        continue

                    try:
                        Candidate.objects.create(
                            name=name,
                            party=party if party else None,
                            bio=bio if bio else None,
                            position=position,
                        )
                        candidates_created += 1
                    except Exception as e:
                        messages.error(request, f"Error creating candidate {name}: {e}")

                self.message_user(
                    request, f"Successfully created {candidates_created} new candidates."
                )
                if candidates_skipped > 0:
                    self.message_user(
                        request,
                        f"Skipped {candidates_skipped} candidates because they already exist.",
                        level=messages.WARNING,
                    )

                return redirect("..")

        form = CandidateCsvUploadForm()
        context = {"form": form}
        return render(request, "admin/candidate_csv_upload.html", context)


admin.site.register(Position)
admin.site.register(Vote)