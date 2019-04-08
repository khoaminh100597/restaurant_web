from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from .models import CustomUser, Restaurant, ImagesRestaurant, Food, ImagesFood, Rate
from django.views.generic import CreateView
from .forms import SignUpForm, ChangeProfileForm, AddRestaurantForm, EditRestaurantForm, AddImagesRestaurantForm, AddFoodForm, EditFoodForm, AddImagesFoodForm
from .decorators import customer_required, restaurant_required

# Create your views here.
class CustomUserView(CreateView):
    model = CreateView
    form_class = SignUpForm
    template_name = 'signup.html'


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

@login_required
def EditProfile(request, slug):
    profile = get_object_or_404(CustomUser, username=slug)
    username = profile.username
    email = profile.email
    phone = profile.phone
    if request.method == 'POST':
        form = ChangeProfileForm(request.POST, instance=profile)
        form.get_old_info(username, email, phone)
        if form.is_valid():
            profile.save()
            return redirect('myprofile')
    else:
        form = ChangeProfileForm(instance=profile)
    return render(request, 'editmyprofile.html', {'form': form})


@login_required
def DeleteProfile(request, slug):
    profile = get_object_or_404(CustomUser, username=slug)
    profile.delete()
    return redirect('home')


@login_required
def AddRestaurant(request, slug):
    try:
        CustomUser.objects.get(username=slug)
    except ObjectDoesNotExist:
        raise Http404("This page doens't exist")
    if CustomUser.objects.get(username=slug).is_customer:
        raise Http404("This page doesn't exist")
    customuser = get_object_or_404(CustomUser, username=slug)
    if request.method == 'POST':
        form = AddRestaurantForm(request.POST)
        form.get_old_customuser(customuser=customuser)
        if form.is_valid():
            restaurant = form.save()
            return redirect('myprofile')
    else:
        form = AddRestaurantForm()
    return render(request, 'addrestaurant.html', {'form': form})


@login_required
def ManageRestaurants(request, slug):
    try:
        CustomUser.objects.get(username=slug)
    except ObjectDoesNotExist:
        raise Http404("This page doens't exist")
    if CustomUser.objects.get(username=slug).is_customer:
        raise Http404("This page doesn't exist")
    my_restaurants = Restaurant.objects.filter(customuser_id=CustomUser.objects.get(username=slug).pk)
    host = slug
    return render(request, 'managerestaurants.html', {'restaurants': my_restaurants, 'host': host})


@login_required
def EditRestaurant(request, slug, pk):
    try:
        CustomUser.objects.get(username=slug)
    except ObjectDoesNotExist:
        raise Http404("This page doens't exist")
    if CustomUser.objects.get(username=slug).is_customer:
        raise Http404("This page doesn't exist")
    restaurant = Restaurant.objects.get(pk = pk)
    customuser = CustomUser.objects.get(username=slug)
    name = restaurant.name
    phone = restaurant.phone
    if request.method == 'POST' and 'edit_res' in request.POST:
        form = EditRestaurantForm(request.POST, instance=restaurant)
        form.get_old_customuser(customuser)
        form.get_old_info(name, phone)
        if form.is_valid():
            restaurant.save()
            my_restaurants = Restaurant.objects.filter(customuser_id=CustomUser.objects.get(username=slug).pk)
            return render(request, 'managerestaurants.html', {'restaurants': my_restaurants, 'host': slug})
    if request.method == 'POST' and 'add_img' in request.POST:
        form_img = AddImagesRestaurantForm(request.POST, request.FILES)
        form_img.get_restaurant(restaurant)
        form_img.save()
        return HttpResponseRedirect(reverse('editrestaurant', kwargs={'slug': slug, 'pk': restaurant.pk}))
    else:
        form = EditRestaurantForm(instance=restaurant)
        form_img = AddImagesRestaurantForm()
        img_restaurants = ImagesRestaurant.objects.filter(restaurant = restaurant)
    return render(request, 'editrestaurant.html', {'form': form, 'form_img': form_img, 'host': slug, 'img_res': img_restaurants})

@login_required
@restaurant_required
def DeleteRestaurant(request, slug, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    if CustomUser.objects.get(pk=restaurant.customuser_id).username != slug:
        raise Http404("You don't have permission to do this")
    restaurant.delete()
    my_restaurants = Restaurant.objects.filter(customuser_id=CustomUser.objects.get(username=slug).pk)
    return render(request, 'managerestaurants.html', {'restaurants': my_restaurants, 'host': slug})

@login_required
@restaurant_required
def DeleteImgRestaurant(request, slug, pk):
    if request.user.username != slug:
        raise Http404("You dont' have permission to do this")
    restaurant = Restaurant.objects.get(imagesrestaurant__pk=pk)
    ImagesRestaurant.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('editrestaurant', kwargs={'slug': slug, 'pk': restaurant.pk}))

def ListRestaurants(request):
    restaurants = Restaurant.objects.all()
    res = []
    for restaurant in restaurants:
        info_res = {}
        info_res['customuser'] = restaurant.customuser
        info_res['id'] = restaurant.id
        info_res['name'] = restaurant.name
        info_res['kind'] = restaurant.kind_of_restaurant
        info_res['phone'] = restaurant.phone
        try:
            info_res['avatar'] = ImagesRestaurant.objects.filter(restaurant=restaurant)[0].image
        except ObjectDoesNotExist:
            info_res['avatar'] = None
        is_liked = False
        if restaurant.likes.filter(id=request.user.id).exists():
            is_liked = True
        info_res['is_liked'] = is_liked
        info_res['likes'] = restaurant.likes.count()
        res.append(info_res)
    return render(request, 'listrestaurants.html', {'res': res})

@login_required
def LikeRestaurant(request):
    restaurant = get_object_or_404(Restaurant, id=request.POST.get('restaurant_id'))
    is_liked = False
    if restaurant.likes.filter(id=request.user.id).exists():
        restaurant.likes.remove(request.user)
        is_liked = True
    else:
        restaurant.likes.add(request.user)
        is_liked = False
    return redirect('listrestaurants')


def ViewRestaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, id=pk)
    host = restaurant.customuser
    images = ImagesRestaurant.objects.filter(restaurant=restaurant)
    likes = restaurant.likes.count()
    is_liked = False
    if restaurant.likes.filter(id=request.user.id).exists():
        is_liked = True
    try:
        foods = Food.objects.filter(restaurant=restaurant)
    except ObjectDoesNotExist:
        foods = None
    return render(request, 'viewrestaurant.html', {'restaurant': restaurant, 'host': host, 'images': images, 'likes': likes, 'is_liked': is_liked, 'foods': foods})

@login_required
def LikeRestaurantFromRestaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, id=request.POST.get('restaurant_id'))
    is_liked = False
    if restaurant.likes.filter(id=request.user.id).exists():
        restaurant.likes.remove(request.user)
        is_liked = True
    else:
        print('haha')
        restaurant.likes.add(request.user)
        is_liked = False
    return HttpResponseRedirect(reverse('viewrestaurant', kwargs={'pk': restaurant.id}))


@login_required
@restaurant_required
def AddFood(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    if request.user != restaurant.customuser:
        raise Http404("You don't have permission to see this")
    if request.method == 'POST':
        form = AddFoodForm(request.POST)
        form.get_restaurant(restaurant)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('viewrestaurant', kwargs={'pk': restaurant.id}))
    else:
        form = AddFoodForm()
    return render(request, 'addfood.html', {'form': form})


@login_required
@restaurant_required
def EditFood(request, pk1, pk2):
    restaurant = Restaurant.objects.get(pk=pk1)
    if request.user != restaurant.customuser:
        raise Http404("You don't have permission to see this")
    food = Food.objects.get(pk=pk2)
    if request.method == 'POST' and 'edit_food' in request.POST:
        form = EditFoodForm(request.POST, instance=restaurant)
        form.get_restaurant(restaurant)
        if form.is_valid():
            restaurant.save()
            return HttpResponseRedirect(reverse('viewrestaurant', kwargs={'pk': restaurant.id}))
    if request.method == 'POST' and 'add_img' in request.POST:
        form_img = AddImagesFoodForm(request.POST, request.FILES)
        form_img.get_food(food)
        form_img.save()
        pk1 = restaurant.pk
        pk2 = food.pk
        return HttpResponseRedirect(reverse('editfood', kwargs={'pk1': pk1, 'pk2': pk2}))
    else:
        form = EditFoodForm(instance=food)
        form_img = AddImagesFoodForm()
        try:
            img_foods = ImagesFood.objects.filter(food = food)
        except ObjectDoesNotExist:
            img_foods = None
    return render(request, 'editfood.html', {'form': form, 'form_img': form_img, 'host': restaurant.customuser, 'img_res': img_foods})


@login_required
@restaurant_required
def DeleteFood(request, pk1, pk2):
    restaurant = Restaurant.objects.get(pk=pk1)
    if request.user != restaurant.customuser:
        raise Http404("You don't have permission to see this")
    food = Food.objects.get(pk=pk2)
    food.delete()
    return HttpResponseRedirect(reverse('viewsrestaurant', kwargs={'pk': restaurant.id}))


@login_required
@restaurant_required
def DelteImgFood(request, pk):
    img_food = ImagesFood.objects.get(pk=pk)
    food = img_food.food
    if request.user != food.restaurant.customuser:
        raise Http404("You don't have permission to do this")
    img_food.delete()
    pk1 = food.restaurant.pk
    pk2 = food.pk
    return HttpResponseRedirect(reverse('editfood', kwargs={'pk1': pk1, 'pk2': pk2}))


def ViewFood(request, pk):
    food = Food.objects.get(id=pk)
    try:
        img_food = ImagesFood.objects.filter(food=food)
    except ObjectDoesNotExist:
        img_food = None
    tags = food.tags.names()
    point = {}
    for p in range(1, 6):
        point[p] = Rate.objects.filter(food=food, point=p).count()
    return render(request, 'viewfood.html', {'food': food, 'img_food': img_food, 'tags': tags, 'point': point})


@login_required
def RatingFood(request, pk):
    food = get_object_or_404(Food, pk=pk)
    is_rated = False
    try:
        rate = Rate.objects.get(customuser=request.user, food=food)
        rate.point = request.POST.get('rating')
        rate.save()
        num = Rate.objects.filter(food=food).count()
        rates = Rate.objects.filter(food=food)
        food.score = 0
        for r in rates:
            food.score += r.point / num
        food.save()
    except ObjectDoesNotExist:
        Rate.objects.create(customuser=request.user, food=food, point=request.POST.get('rating'))
    return HttpResponseRedirect(reverse('viewfood', kwargs={'pk': pk}))