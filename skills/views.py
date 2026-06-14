from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.db.models import Q
from .models import Listing, Booking, Profile, Review, Skill, Notification

def index(request):
    """Landing page for the site."""
    return render(request, 'skills/index.html')

# Create your views here.

def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create the associated profile
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful! Welcome to SkillSwap.")
            return redirect('index')
    else:
        form = UserCreationForm()

    # Remove help text from all fields to ensure a clean registration UI
    for field in form.fields.values():
        field.help_text = None

    return render(request, 'skills/register.html', {'form': form})

def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('index')

@login_required
def listing_list(request):
    """Display all available skill listings."""
    query = request.GET.get('q')
    listings = Listing.objects.all().order_by('-created_at')

    if query:
        listings = listings.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(teacher__username__icontains=query)
        )

    # Exclude listings that have a completed booking
    listings = listings.exclude(bookings__status='completed')
    listings = listings.exclude(teacher=request.user)
    return render(request, 'skills/listing_list.html', {'listings': listings})

@login_required
def listing_detail(request, pk):
    """Display details for a specific listing."""
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'skills/listing_detail.html', {'listing': listing})

@login_required
def booking_detail(request, pk):
    """Display details for a specific booking."""
    booking = get_object_or_404(Booking, pk=pk)
    # Security check: Only teacher or student involved can see this
    if request.user != booking.student and request.user != booking.listing.teacher:
        messages.error(request, "You do not have permission to view this booking.")
        return redirect('index')
    return render(request, 'skills/booking_detail.html', {'booking': booking})

@login_required
def create_listing(request):
    """Allow a user to create a new skill listing."""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        
        Listing.objects.create(
            teacher=request.user,
            title=title,
            description=description,
            price=price
        )
        messages.success(request, "Your listing has been created!")
        return redirect('listing_list')
    return render(request, 'skills/create_listing.html')

@login_required
def create_booking(request, listing_id):
    """Handle the booking request for a listing."""
    listing = get_object_or_404(Listing, id=listing_id)
    
    if listing.teacher == request.user:
        messages.error(request, "You cannot book your own listing.")
        return redirect('listing_detail', pk=listing_id)

    if request.method == 'POST':
        date = request.POST.get('date')
        if date:
            booking = Booking.objects.create(
                student=request.user,
                listing=listing,
                date=date
            )
            Notification.objects.create(
                user=listing.teacher,
                message=f"New booking request from {request.user.username} for '{listing.title}'.",
                link=reverse('booking_detail', kwargs={'pk': booking.id})
            )
            messages.success(request, f"Booking for {listing.title} requested!")
            return redirect('my_bookings')
            
    return render(request, 'skills/book_listing.html', {'listing': listing})

@login_required
def my_bookings(request):
    """Show bookings for both students and teachers."""
    # Filter to show only pending and confirmed bookings, sorted by date (upcoming first)
    unfinished_statuses = ['pending', 'confirmed']
    as_student = Booking.objects.filter(student=request.user, status__in=unfinished_statuses).order_by('date')
    as_teacher = Booking.objects.filter(listing__teacher=request.user, status__in=unfinished_statuses).order_by('date')
    return render(request, 'skills/my_bookings.html', {
        'as_student': as_student,
        'as_teacher': as_teacher
    })

@login_required
def add_review(request, booking_id):
    """Submit a review for a completed booking."""
    booking = get_object_or_404(Booking, id=booking_id, student=request.user)
    
    if booking.status != 'completed':
        messages.error(request, "You can only review completed sessions.")
        return redirect('my_bookings')

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(booking=booking, rating=rating, comment=comment)
        messages.success(request, "Review submitted!")
        return redirect('booking_detail', pk=booking.id)

    return render(request, 'skills/add_review.html', {'booking': booking})

@login_required
def profile_view(request):
    """Display and update user profile."""
    profile = get_object_or_404(Profile, user=request.user)
    
    # Filter listings to only show those that are not associated with any completed bookings
    # This ensures only 'active' listings appear on the profile
    user_listings = request.user.listings.all().exclude(bookings__status='completed').order_by('-created_at')

    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        messages.success(request, "Your profile has been updated!")
        return redirect('profile')
        
    return render(request, 'skills/profile.html', {
        'profile': profile,
        'user_listings': user_listings
    })

@login_required
def user_profile(request, username):
    """Display a public profile for any user."""
    profile = get_object_or_404(Profile, user__username=username)
    
    # Ensure the public profile also shows the user's active listings
    user_listings = profile.user.listings.all().exclude(bookings__status='completed').order_by('-created_at')
    
    return render(request, 'skills/profile.html', {
        'profile': profile,
        'user_listings': user_listings
    })

@login_required
def notifications_view(request):
    """Display all notifications for the user."""
    # Convert to a list to capture the 'unread' status before updating the database
    notifications = list(request.user.notifications.all().order_by('-created_at'))
    
    # Mark all as read so they won't be highlighted on the next visit
    request.user.notifications.filter(is_read=False).update(is_read=True)
        
    return render(request, 'skills/notifications.html', {
        'notifications': notifications
    })

@login_required
def notification_count(request):
    """API endpoint to get unread notification count."""
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'unread_count': count})

@login_required
def update_booking_status(request, booking_id):
    """Allow teachers to update the status of a booking."""
    booking = get_object_or_404(Booking, id=booking_id, listing__teacher=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.save()
            Notification.objects.create(
                user=booking.student,
                message=f"The status of your booking for '{booking.listing.title}' has been updated to '{booking.get_status_display()}'.",
                link=reverse('booking_detail', kwargs={'pk': booking.pk})
            )
            messages.success(request, f"Booking status updated to {booking.get_status_display()}.")
    return redirect('my_bookings')

@login_required
def cancel_booking(request, booking_id):
    """Allow students to cancel their own pending booking requests."""
    booking = get_object_or_404(Booking, id=booking_id, student=request.user, status='pending')
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        Notification.objects.create(
            user=booking.listing.teacher,
            message=f"{request.user.username} cancelled their booking request for '{booking.listing.title}'.",
            link=reverse('booking_detail', kwargs={'pk': booking.pk})
        )
        messages.success(request, "Your booking request has been cancelled.")
    return redirect('my_bookings')

@login_required
def delete_listing(request, pk):
    """Allow teachers to delete their own listings."""
    listing = get_object_or_404(Listing, pk=pk, teacher=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, "Listing deleted successfully.")
    return redirect('profile')
