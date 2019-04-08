from django.forms import ValidationError
from .models import CustomUser, Restaurant, ImagesRestaurant, Food, ImagesFood, Rate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django.db import transaction

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'email', 'phone', 'avatar', 'type']

    def clean_username(self):
        if 'username' in self.cleaned_data:
            username = self.cleaned_data['username']
            try:
                CustomUser.objects.get(username=username)
            except ObjectDoesNotExist:
                return username
            raise ValidationError('Username has already taken')

    def clean_email(self):
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            try:
                CustomUser.objects.get(email=email)
            except ObjectDoesNotExist:
                return email
            raise ValidationError('Email has already taken')

    def clead_phone(self):
        if 'phone' in self.cleaned_data:
            phone = self.clead_data['phone']
            try:
                CustomUser.objects.get(phone=phone)
            except ObjectDoesNotExist:
                return phone
            raise ValidationError('Phone has already taken')

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.type == 'Cu':
            user.is_customer = True
        elif user.type == 'Re':
            user.is_restaurant = True
        user.save()
        return user

class ChangeProfileForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'email', 'phone', 'avatar',)

    def get_old_info(self, username, email, phone):
        self.username = username
        self.email = email
        self.phone = phone

    def clean_username(self):
        if 'username' in self.cleaned_data and self.cleaned_data['username'] != self.username:
            username = self.cleaned_data['username']
            try:
                CustomUser.objects.get(username=username)
            except ObjectDoesNotExist:
                return username
            raise ValidationError('Username has already taken')
        else:
            return self.username

    def clean_email(self):
        if 'email' in self.cleaned_data and self.cleaned_data['email'] != self.email:
            email = self.cleaned_data['email']
            try:
                CustomUser.objects.get(email=email)
            except ObjectDoesNotExist:
                return email
            raise ValidationError('Email has already taken')
        else:
            return self.email

    def clean_phone(self):
        if 'phone' in self.cleaned_data and self.cleaned_data['phone'] != self.phone:
            phone = self.cleand_data['phone']
            try:
                CustomUser.objects.get(phone=phone)
            except ObjectDoesNotExist:
                return phone
            raise ValidationError('Phone has already taken')
        else:
            return self.phone


class AddRestaurantForm(ModelForm):
    class Meta(ModelForm):
        model = Restaurant
        fields = ('name', 'phone', 'address', 'description', 'kind_of_restaurant')

    def get_old_customuser(self, customuser):
        self.customuser = customuser

    def clean_name(self):
        if 'name' in self.cleaned_data:
            name = self.cleaned_data['name']
            try:
                Restaurant.objects.get(name=name)
            except ObjectDoesNotExist:
                return name
            raise ValidationError('This name has already taken')

    def clean_phone(self):
        if 'phone' in self.cleaned_data:
            phone = self.cleaned_data['phone']
            try:
                Restaurant.objects.get(phone=phone)
            except ObjectDoesNotExist:
                return phone
            raise ValidationError('This number of phone has already taken')

    @transaction.atomic
    def save(self, commit=True):
        restaurant = super().save(commit=False)
        restaurant.customuser = self.customuser
        restaurant.save()
        return restaurant


class EditRestaurantForm(ModelForm):
    class Meta(ModelForm):
        model = Restaurant
        fields = ('name', 'phone', 'address', 'description', 'kind_of_restaurant')

    def get_old_customuser(self, customuser):
        self.customuser = customuser

    def get_old_info(self, name, phone):
        self.name = name
        self.phone = phone

    def clean_name(self):
        if 'name' in self.cleaned_data and self.name != self.cleaned_data['name']:
            name = self.cleaned_data['name']
            try:
                Restaurant.objects.get(name=name)
            except ObjectDoesNotExist:
                return name
            raise ValidationError('This name has already taken')
        else:
            return self.name

    def clean_phone(self):
        if 'phone' in self.cleaned_data and self.phone != self.cleaned_data['phone']:
            phone = self.cleaned_data['phone']
            try:
                Restaurant.objects.get(phone=phone)
            except ObjectDoesNotExist:
                return phone
            raise ValidationError('This number of phone has already taken')
        else:
            return self.phone

    @transaction.atomic
    def save(self, commit=True):
        restaurant = super().save(commit=False)
        restaurant.customuser = self.customuser
        restaurant.save()
        return restaurant

class AddImagesRestaurantForm(ModelForm):
    class Meta(ModelForm):
        model = ImagesRestaurant
        fields = ('image',)

    def get_restaurant(self, restaurant):
        self.restaurant = restaurant

    @transaction.atomic
    def save(self, commit=True):
        image = super().save(commit=False)
        image.restaurant = self.restaurant
        image.save()
        return image


class AddFoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ('name', 'detail', 'tags', 'price')

    def get_restaurant(self, restaurant):
        self.restaurant = restaurant

    def save(self, commit=True):
        food = super().save(commit=False)
        food.restaurant = self.restaurant
        food.save()
        for tag in self.cleaned_data['tags']:
            food.tags.add(tag)
        return food


class EditFoodForm(ModelForm):
    class Meta(ModelForm):
        model = Food
        fields = ('name', 'detail', 'tags', 'price')

    def get_restaurant(self, restaurant):
        self.restaurant = restaurant

    def save(self, commit=True):
        food = super().save(commit=False)
        food.restaurant = self.restaurant
        food.save()
        for tag in self.cleaned_data['tags']:
            food.tags.add(tag)
        return food

class AddImagesFoodForm(ModelForm):
    class Meta(ModelForm):
        model = ImagesFood
        fields = ('image',)

    def get_food(self, food):
        self.food = food

    @transaction.atomic
    def save(self, commit=True):
        image = super().save(commit=False)
        image.food = self.food
        image.save()
        return image